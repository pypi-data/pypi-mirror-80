from guillotina import configure
from guillotina import schema
from guillotina.component import get_adapter
from guillotina.interfaces import IJSONToValue
from zope.interface import Interface, Attribute
from zope.interface import implementer
from guillotina.schema.interfaces import IField
from guillotina.fields.interfaces import IPatchFieldOperation
from guillotina.interfaces import ISchemaFieldSerializeToJson
from guillotina.json.serialize_schema_field import DefaultSchemaFieldSerializer
from guillotina.fields import patch
from guillotina.component import get_utility
from guillotina_pgfield.interfaces import IPGFieldUtility
import logging
import sqlalchemy as sa
import jsonschema
from datetime import datetime
from guillotina.utils import get_current_request
from guillotina.json.deserialize_value import datetime_converter

logger = logging.getLogger(__name__)


class IPGListField(IField):
    """PG Field."""


@configure.adapter(for_=IPGListField, provides=IPatchFieldOperation, name="append")
class PatchPGListAppend(patch.PatchListAppend):
    async def __call__(self, context, value):
        value = get_adapter(self.field, IJSONToValue, args=[value, context])

        request = get_current_request()
        utility = get_utility(IPGFieldUtility)

        # Validation
        values_to_serialize = {}
        for column in self.field._pg_schema:
            if column.name in value:
                values_to_serialize[column.name] = value[column.name]
        
        table = utility.get_table(self.field._pg_table, self.field._pg_schema)
        statement = table.insert().values(zoid=context.__uuid__, ts=datetime.utcnow(), **values_to_serialize)
        await utility.add_statement(request, statement)

    async def set(self, value):
        await value.operation


@configure.adapter(for_=IPGListField, provides=IPatchFieldOperation, name="extend")
class PatchPGListExtend(PatchPGListAppend):
    async def __call__(self, context, value):
        value = get_adapter(self.field, IJSONToValue, args=[value, context])

        request = get_current_request()
        utility = get_utility(IPGFieldUtility)

        table = utility.get_table(self.field._pg_table, self.field._pg_schema)
        for real_value in value:
            values_to_serialize = {}
            for column in self.field._pg_schema:
                if column.name in real_value:
                    values_to_serialize[column.name] = real_value[column.name]
            statement = table.insert().values(zoid=context.__uuid__, ts=datetime.utcnow(), **values_to_serialize)
            await utility.add_statement(request, statement)


@configure.adapter(for_=IPGListField, provides=IPatchFieldOperation, name="del")
class PatchPGListDel(PatchPGListAppend):
    async def __call__(self, context, value):
        value = get_adapter(self.field, IJSONToValue, args=[value, context])

        request = get_current_request()
        utility = get_utility(IPGFieldUtility)

        table = utility.get_table(self.field._pg_table, self.field._pg_schema)
        statement = sa.select([table.c.ts]).where(table.c.zoid == context.__uuid__)
        result = await utility.query(statement)
        item_index = int(value)
        if item_index < len(result):
            statement = table.delete().where(table.c.zoid == context.__uuid__).where(table.c.ts == result[item_index][0])
            await utility.add_statement(request, statement)


@configure.value_deserializer(IPGListField)
def pg_list_deserializer(field, value, context):
    for key, values in field._json_schema["properties"].items():
        if isinstance(value, dict) and key in value:
            if values["type"] == "datetime":
                value[key] = datetime_converter(field, value[key], context)
    return value


@configure.adapter(for_=(IPGListField, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultFileSchemaFieldSerializer(DefaultSchemaFieldSerializer):
    @property
    def field_type(self):
        return "array"


@implementer(IPGListField)
class PGListField(schema.Field):
    def __init__(self, *args, json_schema=None, validator=None, pg_schema=None, pg_table=None, **kwargs):
        self._json_schema = json_schema
        self._validator = validator
        self._pg_schema = pg_schema
        self._pg_table = pg_table
        super().__init__(*args, **kwargs)

    def validate(self, value):
        if isinstance(value, list):
            for v in value.json_value:
                jsonschema.validate(v, self._json_schema)
        elif isinstance(value, dict):
            jsonschema.validate(value.json_value, self._json_schema)

    async def set(self, obj, value):
        if self._validator:
            await self._validator(obj, value)
        utility = get_utility(IPGFieldUtility)
        if not await utility.exist(self._pg_table):
            await utility.create(self._pg_table, self._pg_schema)

        if value.operation is None:
            return
        await value.operation
