from guillotina import configure
from guillotina.content import Item
from guillotina.content import load_cached_schema
from guillotina.db import ROOT_ID
from guillotina.tests.utils import ContainerRequesterAsyncContextManager
from guillotina.transactions import transaction
from guillotina.utils import apply_coroutine
from guillotina_numpy.field import NumPyArrayField
from zope.interface import Interface

import json
import numpy as np
import pytest


class IFoobarType(Interface):
    foobar = NumPyArrayField(required=False)


class FoobarType(Item):
    pass


class CustomTypeContainerRequesterAsyncContextManager(
    ContainerRequesterAsyncContextManager
):  # noqa
    async def __aenter__(self):
        configure.register_configuration(
            FoobarType,
            dict(schema=IFoobarType, type_name="Foobar", behaviors=[]),
            "contenttype",
        )
        requester = await super(
            CustomTypeContainerRequesterAsyncContextManager, self
        ).__aenter__()
        config = requester.root.app.config
        # now test it...
        configure.load_configuration(config, "guillotina_numpy.tests", "contenttype")
        config.execute_actions()
        load_cached_schema()
        return requester


@pytest.fixture(scope="function")
async def custom_numpy_type_container_requester(guillotina):
    return CustomTypeContainerRequesterAsyncContextManager(guillotina)


@pytest.mark.asyncio
async def test_numpyfield(custom_numpy_type_container_requester):
    async with custom_numpy_type_container_requester as requester:

        response, status = await requester(
            "POST",
            "/db/guillotina/",
            data=json.dumps({"@type": "Foobar", "title": "Item1", "id": "item1"}),
        )
        assert status == 201

        value = np.random.rand(3, 3)
        async with transaction(db=requester.db, abort_when_done=False) as txn:
            root = await txn.get(ROOT_ID)
            container = await root.async_get("guillotina")
            obj = await container.async_get("item1")
            field = IFoobarType["foobar"].bind(obj)
            await apply_coroutine(field.set, obj, value)

        async with transaction(db=requester.db, abort_when_done=True) as txn:
            root = await txn.get(ROOT_ID)
            container = await root.async_get("guillotina")
            obj = await container.async_get("item1")
            field = IFoobarType["foobar"].bind(obj)
            value = await apply_coroutine(field.get, obj)
            # Get the Value and the numpy
            nparray = await value.get(obj)
            assert len(nparray.value) == 3
