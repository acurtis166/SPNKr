"""Test the spnkr.responses module."""

import pytest

from spnkr.responses import ImageResponse, JsonResponse


def test_json_response_from_cache(cached_response):
    result = JsonResponse(cached_response, lambda _: None)
    assert result.from_cache


@pytest.mark.asyncio
async def test_json_response_parse(response):
    result: JsonResponse[dict] = JsonResponse(
        response, lambda data: data | {"test": 1}
    )
    assert (await result.parse())["test"] == 1


def test_image_response_from_cache(cached_response):
    result = ImageResponse(cached_response)
    assert result.from_cache


@pytest.mark.asyncio
async def test_image_response_read(response):
    result = ImageResponse(response)
    assert await result.read() == b"{}"
