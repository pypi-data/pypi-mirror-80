import json
import pytest
import asyncio

pytestmark = pytest.mark.asyncio
@pytest.mark.asyncio
async def test_pgfieldfield(custom_pgfield_type_container_requester):
    async with custom_pgfield_type_container_requester as requester:

        response, status = await requester(
            'POST',
            '/db/guillotina/',
            data=json.dumps({
                "@type": "Foobar",
                "title": "Item1",
                "id": "item1"
            })
        )
        assert status == 201

        response, status = await requester(
            'PATCH',
            '/db/guillotina/item1',
            data=json.dumps({
                "foobar": {
                    "op": "append",
                    "value": {
                        "num": 4.5,
                        "text": "hello"
                    }
                }
            })
        )
        assert status == 204

        response, status = await requester(
            'GET',
            '/db/guillotina/item1',
        )
        assert status == 200

        response, status = await requester(
            'PATCH',
            '/db/guillotina/item1',
            data=json.dumps({
                "foobar": {
                    "op": "extend",
                    "value": [{
                        "num": 4.5,
                        "text": "hello2"
                    }]
                }
            })
        )
        assert status == 204
        
        await asyncio.sleep(2)
        response, status = await requester(
            'GET',
            '/db/guillotina/item1',
        )
        assert status == 200

        response, status = await requester(
            'PATCH',
            '/db/guillotina/item1',
            data=json.dumps({
                "foobar": {
                    "op": "del",
                    "value": 0
                }
            })
        )
        assert status == 204

        response, status = await requester(
            'GET',
            '/db/guillotina/item1',
        )
        assert status == 200
