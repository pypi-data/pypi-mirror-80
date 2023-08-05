# Introduction


Naive aproach of pgfield with an external PG database

## Basic instructions

- Python >= 3.7
- PostgreSQL >= 9.6


```
  load_utilities:
    pgfield:
      factory: guillotina_pgfield.utility.PGFieldUtility
      provides: guillotina_pgfield.interfaces.IPGFieldUtility
      settings:
        dsn: postgres://user:passwd@pg_url:5432/db
        pool_size: 10
```

## Content type definition

```
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

```
