from asyncpgsa.connection import get_dialect
from guillotina.component import get_utility
from guillotina_pgfield.interfaces import IPGFieldUtility
import logging
from guillotina.exceptions import Unauthorized
import json
import asyncpgsa
import asyncio
import contextvars
from sqlalchemy import Column, MetaData, String, Table, DateTime
from sqlalchemy.schema import CreateTable
from asyncpgsa.pgsingleton import QueryContextManager
import sqlalchemy as sa


logger = logging.getLogger("guillotina_pgfield")

pgfield_statements_var = contextvars.ContextVar("statements")


class PGFieldFuture(object):
    async def __call__(self):
        utility = get_utility(IPGFieldUtility)

        for statement in utility.get_statements():
            await utility.pgfield_db.fetch(statement)


class PGFieldUtility(object):
    def __init__(self, settings={}, loop=None):
        self.loop = loop
        self.db_config = settings
        self.pgfield_db = None
        self._exists = []
        self._schemas = {}

    async def initialize(self, app):
        dialect = get_dialect(json_serializer=json.dumps, json_deserializer=json.loads)

        if "dsn" not in self.db_config:
            return

        if isinstance(self.db_config["dsn"], dict):
            self.pgfield_db = await asyncpgsa.create_pool(
                dialect=dialect,
                loop=self.loop,
                max_size=self.db_config.get("pool_size", 10),
                min_size=2,
                **self.db_config["dsn"],
            )

        else:
            self.pgfield_db = await asyncpgsa.create_pool(
                dialect=dialect,
                dsn=self.db_config["dsn"],
                loop=self.loop,
                max_size=self.db_config.get("pool_size", 10),
                min_size=2,
            )

    async def finalize(self):
        if self.pgfield_db:
            self.pgfield_db.terminate()

    def get_statements(self):
        try:
            return pgfield_statements_var.get()
        except LookupError:
            statements = []
            pgfield_statements_var.set(statements)
            return statements

    async def check(self):
        count = 0
        while self.pgfield_db is None and count < 5:
            await asyncio.sleep(1)
            count += 1
        if self.pgfield_db is None:
            raise Exception("Not connected")

    async def exist(self, table_name):
        await self.check()
        if table_name in self._exists:
            return True

        statement = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE  table_schema = 'public' AND table_name = '{table_name}');"  # noqa
        result = await self.pgfield_db.fetchrow(statement)
        if result["exists"] is True:
            self._exists.append(table_name)
            return True
        return False

    def get_table(self, table_name, db_schema):
        if table_name in self._schemas:
            return self._schemas[table_name]
        
        copied_schema = [x.copy() for x in db_schema]

        metadata = MetaData()
        pgfield_table = Table(
            table_name,
            metadata,
            Column("zoid", String, index=True),
            Column("ts", DateTime(timezone=True), index=True),
            *copied_schema,
        )
        self._schemas[table_name] = pgfield_table
        return pgfield_table

    async def create(self, table_name, db_schema):
        await self.check()
        table = self.get_table(table_name, db_schema)
        sts = CreateTable(table)
        statement = str(sts).replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS")
        statement = str(statement).replace("DATETIME", "timestamp with time zone")
        await self.pgfield_db.fetch(statement)
        self._exists.append(table_name)

    async def add_statement(self, request, statement):
        await self.check()
        # If request is not writable fail
        if hasattr(request, "_db_write_enabled") and not request._db_write_enabled:
            raise Unauthorized("Adding content not permited")
        # add statement to process
        statements = self.get_statements()
        statements.append(statement)
        fut = request.get_future("pgfield")
        if fut is None:
            fut = PGFieldFuture()
            request.add_future("pgfield", fut)

    async def query(self, statement):
        query_string, params = asyncpgsa.compile_query(statement)
        return await self.pgfield_db.fetch(query_string, *params)

    async def batch_query(self, statement):
        await self.check()
        query_string, params = asyncpgsa.compile_query(statement)
        cm = QueryContextManager(self.pgfield_db, query_string, params, prefetch=None, timeout=None)
        async with cm as cursor:
            async for row in cursor:
                yield row

    async def get(self, table, item_index, zoid):
        await self.check()

        statement = (
            sa.select(["*"])
            .select_from(sa.text(table.name))
            .order_by(sa.text("ts desc"))
            .where(table.c.zoid == zoid)
        )
        return await self.query(statement)

    async def get_last(self, table, zoid, order_by=None):
        await self.check()

        if order_by is not None:
            order = sa.text(table.name + "." + order_by + " desc")
        else:
            order = sa.text("ts desc")
        statement = sa.select("*").order_by(order).where(table.c.zoid == zoid).limit(1)
        return await self.pgfield_db.fetchrow(statement)

    async def get_all(self, table, zoid, from_=None, to_=None):
        await self.check()

        statement = sa.select("*").order_by(sa.text("ts desc")).where(table.c.zoid == zoid)
        if from_ is not None:
            statement = statement.where(table.c.ts >= from_)
        if to_ is not None:
            statement = statement.where(table.c.ts <= to_)
        async for item in self.batch_query(statement):
            yield item
