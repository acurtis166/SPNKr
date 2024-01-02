"""Live tests for all Halo Infinite API endpoints."""

import asyncio
import os

import dotenv
import pytest
import pytest_asyncio
from aiohttp import ClientSession

from spnkr.auth import AzureApp, refresh_player_tokens
from spnkr.client import HaloInfiniteClient


@pytest_asyncio.fixture(scope="module")
async def authenticated_player():
    dotenv.load_dotenv()
    refresh_token = os.environ["SPNKR_REFRESH_TOKEN"]
    client_id = os.environ["SPNKR_CLIENT_ID"]
    client_secret = os.environ["SPNKR_CLIENT_SECRET"]
    redirect_uri = os.environ["SPNKR_REDIRECT_URI"]
    app = AzureApp(client_id, client_secret, redirect_uri)
    async with ClientSession() as session:
        return await refresh_player_tokens(session, app, refresh_token)


@pytest_asyncio.fixture(scope="module")
async def client(authenticated_player):
    """Return a client."""
    async with ClientSession() as session:
        yield HaloInfiniteClient(
            session=session,
            spartan_token=authenticated_player.spartan_token.token,
            clearance_token=authenticated_player.clearance_token.token,
            requests_per_second=None,
        )


@pytest.fixture(scope="module")
def event_loop():
    """Redefine the event loop to be module-scoped."""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_get_map(client):
    await client.discovery_ugc.get_map(
        asset_id="298d5036-cd43-47b3-a4bd-31e127566593",
        version_id="a6be2e70-dca8-44a5-aeca-70c1b5485823",
    )


@pytest.mark.asyncio
async def test_get_ugc_game_variant(client):
    await client.discovery_ugc.get_ugc_game_variant(
        asset_id="3899e110-91cd-4479-a8ad-5f8f8b91248d",
        version_id="9f315128-fe6f-4161-a52e-b35cb563dc2c",
    )


@pytest.mark.asyncio
async def test_get_playlist(client):
    await client.discovery_ugc.get_playlist(
        asset_id="edfef3ac-9cbe-4fa2-b949-8f29deafd483",
        version_id="bd985d58-2857-409d-8523-1917072f7435",
    )


@pytest.mark.asyncio
async def test_get_map_mode_pair(client):
    await client.discovery_ugc.get_map_mode_pair(
        asset_id="69d25f16-bc62-4d58-baf7-6210f65461f3",
        version_id="91ca22c3-e2a8-4586-8011-a4888f175d3e",
    )


@pytest.mark.asyncio
async def test_search_assets(client):
    await client.discovery_ugc.search_assets(count=5)


@pytest.mark.asyncio
async def test_get_film_by_match_id(client):
    await client.discovery_ugc.get_film_by_match_id(
        match_id="9e3b9529-4dd9-47b0-9669-1f589b9daaf0",
    )


@pytest.mark.asyncio
async def test_get_medal_metadata(client):
    await client.gamecms_hacs.get_medal_metadata()


@pytest.mark.asyncio
async def test_get_csr_season_calendar(client):
    await client.gamecms_hacs.get_csr_season_calendar()


@pytest.mark.asyncio
async def test_get_season_calendar(client):
    await client.gamecms_hacs.get_season_calendar()


@pytest.mark.asyncio
async def test_get_career_reward_track(client):
    await client.gamecms_hacs.get_career_reward_track()


@pytest.mark.asyncio
async def test_get_image(client):
    await client.gamecms_hacs.get_image(
        relative_path="career_rank/NameplateAdornment/272_Hero.png",
    )


@pytest.mark.asyncio
async def test_get_current_user(client):
    await client.profile.get_current_user()


@pytest.mark.asyncio
async def test_get_user_by_gamertag(client):
    await client.profile.get_user_by_gamertag(gamertag="aCurtis X89")


@pytest.mark.asyncio
async def test_get_user_by_id(client):
    await client.profile.get_user_by_id(xuid=2535445291321133)


@pytest.mark.asyncio
async def test_get_users_by_id(client):
    await client.profile.get_users_by_id(
        xuids=[2535445291321133, 2533274880629884],
    )


@pytest.mark.asyncio
async def test_get_match_skill(client):
    await client.skill.get_match_skill(
        match_id="44fedab3-6cc3-4eff-a154-5a2a26e4965f",
        xuids=[2535445291321133, 2533274880629884],
    )


@pytest.mark.asyncio
async def test_get_playlist_csr(client):
    await client.skill.get_playlist_csr(
        playlist_id="edfef3ac-9cbe-4fa2-b949-8f29deafd483",
        xuids=[2535445291321133, 2533274880629884],
    )


@pytest.mark.asyncio
async def test_get_match_count(client):
    await client.stats.get_match_count(player="aCurtis X89")


@pytest.mark.asyncio
async def test_get_service_record(client):
    await client.stats.get_match_history(player="aCurtis X89", count=5)


@pytest.mark.asyncio
async def test_match_stats(client):
    await client.stats.get_match_stats(
        match_id="01b687a8-2f21-4041-997b-a60ff5fdce15"
    )
