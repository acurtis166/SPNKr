"""Live tests for all Halo Infinite API endpoints."""

import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_get_map(client):
    resp = await client.discovery_ugc.get_map(
        asset_id="298d5036-cd43-47b3-a4bd-31e127566593",
        version_id="a6be2e70-dca8-44a5-aeca-70c1b5485823",
    )
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_ugc_game_variant(client):
    resp = await client.discovery_ugc.get_ugc_game_variant(
        asset_id="3899e110-91cd-4479-a8ad-5f8f8b91248d",
        version_id="9f315128-fe6f-4161-a52e-b35cb563dc2c",
    )
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_playlist(client):
    resp = await client.discovery_ugc.get_playlist(
        asset_id="edfef3ac-9cbe-4fa2-b949-8f29deafd483",
        version_id="bd985d58-2857-409d-8523-1917072f7435",
    )
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_map_mode_pair(client):
    resp = await client.discovery_ugc.get_map_mode_pair(
        asset_id="69d25f16-bc62-4d58-baf7-6210f65461f3",
        version_id="91ca22c3-e2a8-4586-8011-a4888f175d3e",
    )
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_search_assets(client):
    resp = await client.discovery_ugc.search_assets(count=5)
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_film_by_match_id(client):
    resp = await client.discovery_ugc.get_film_by_match_id(
        match_id="63391382-6b88-43f9-9ff4-6313404c419c",
    )
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_medal_metadata(client):
    resp = await client.gamecms_hacs.get_medal_metadata()
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_csr_season_calendar(client):
    resp = await client.gamecms_hacs.get_csr_season_calendar()
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_season_calendar(client):
    resp = await client.gamecms_hacs.get_season_calendar()
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_career_reward_track(client):
    resp = await client.gamecms_hacs.get_career_reward_track()
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_image(client):
    resp = await client.gamecms_hacs.get_image(
        relative_path="career_rank/NameplateAdornment/272_Hero.png",
    )
    await resp.read()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_current_user(client):
    resp = await client.profile.get_current_user()
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_by_gamertag(client):
    resp = await client.profile.get_user_by_gamertag(gamertag="aCurtis X89")
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_by_id(client):
    resp = await client.profile.get_user_by_id(xuid=2535445291321133)
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_users_by_id(client):
    resp = await client.profile.get_users_by_id(
        xuids=[2535445291321133, 2533274880629884],
    )
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_match_skill(client):
    resp = await client.skill.get_match_skill(
        match_id="a6106664-fd07-4973-9251-d2196502a8da",
        xuids=[2533274824889939, 2533274792954103],
    )
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_playlist_csr(client):
    resp = await client.skill.get_playlist_csr(
        playlist_id="edfef3ac-9cbe-4fa2-b949-8f29deafd483",
        xuids=[2535445291321133, 2533274880629884],
    )
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_match_count(client):
    resp = await client.stats.get_match_count(player="aCurtis X89")
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_service_record(client):
    resp = await client.stats.get_match_history(player="aCurtis X89", count=5)
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_match_stats(client):
    resp = await client.stats.get_match_stats(
        match_id="01b687a8-2f21-4041-997b-a60ff5fdce15"
    )
    await resp.parse()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_player_customization(client):
    resp = await client.economy.get_player_customization(xuid=2535445291321133)
    await resp.parse()
