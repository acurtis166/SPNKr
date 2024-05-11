"""Test the spnkr.responses module."""

import pytest

from spnkr.responses import JsonResponse, _BaseResponse


def test_response_from_cache(cached_response):
    result = _BaseResponse(cached_response)
    assert result.from_cache


@pytest.mark.asyncio
async def test_response_read(response):
    result = _BaseResponse(response)
    assert await result.read() == b"{}"


@pytest.mark.asyncio
async def test_json_response_json(response):
    result: JsonResponse[dict] = JsonResponse(response, lambda data: data)
    assert await result.json() == {}


@pytest.mark.asyncio
async def test_json_response_parse(response):
    result: JsonResponse[dict] = JsonResponse(
        response, lambda data: data | {"test": 1}
    )
    assert (await result.parse())["test"] == 1
