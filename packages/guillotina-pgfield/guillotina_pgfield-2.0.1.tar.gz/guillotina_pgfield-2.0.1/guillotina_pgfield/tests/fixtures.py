import pytest
from guillotina import testing
from guillotina import configure
from guillotina.content import load_cached_schema
from guillotina.tests.utils import ContainerRequesterAsyncContextManager
from guillotina.content import Item
from zope.interface import Interface
from guillotina_pgfield.field import PGListField
from guillotina.fields import PatchField
from sqlalchemy import Column, DateTime, String, Float


def base_settings_configurator(settings):
    if "applications" in settings:
        settings["applications"].append("guillotina_pgfield")
    else:
        settings["applications"] = ["guillotina_pgfield"]

    settings["load_utilities"]["pgfield"] = {
        "provides": "guillotina_pgfield.interfaces.IPGFieldUtility",  # noqa
        "factory": "guillotina_pgfield.utility.PGFieldUtility",
        "settings": {
            "dsn": "postgres://postgres@{}:{}/postgres".format(
                getattr(pg_pgfield, "host", "localhost"), getattr(pg_pgfield, "port", 5432)
            ),
            "pool_size": 10,
        },
    }


testing.configure_with(base_settings_configurator)


@pytest.fixture(scope="session")
def pg_pgfield(pg):
    host, port = pg

    setattr(pg_pgfield, "host", host)
    setattr(pg_pgfield, "port", port)

    yield pg


FOOBAR_PG = [
    Column("num", Float),
    Column("text", String, nullable=True)]

FOOBAR_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "num": {"type": "number"},
        "text": {"type": "string"}
    }
}
async def foobar_validator(context, value):
    return True


class IFoobarType(Interface):
    foobar = PatchField(
        PGListField(
            title="foobar",
            json_schema=FOOBAR_SCHEMA,
            validator=foobar_validator,
            pg_schema=FOOBAR_PG,
            pg_table="foobar",
            required=False,
        )
    )

class FoobarType(Item):
    pass


class CustomTypeContainerRequesterAsyncContextManager(ContainerRequesterAsyncContextManager):  # noqa

    async def __aenter__(self):
        configure.register_configuration(FoobarType, dict(
            schema=IFoobarType,
            type_name="Foobar",
            behaviors=[]
        ), 'contenttype')
        requester = await super(
            CustomTypeContainerRequesterAsyncContextManager, self).__aenter__()
        config = requester.root.app.config
        # now test it...
        configure.load_configuration(
            config, 'guillotina_pgfield.tests', 'contenttype')
        config.execute_actions()
        load_cached_schema()
        return requester

@pytest.fixture(scope='function')
async def custom_pgfield_type_container_requester(pg_pgfield, guillotina):
    return CustomTypeContainerRequesterAsyncContextManager(guillotina)
