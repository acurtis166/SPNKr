"""Live tests for all Halo Infinite API endpoints."""

import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_get_map(client):
    await client.get_map(
        asset_id="298d5036-cd43-47b3-a4bd-31e127566593",
        version_id="a6be2e70-dca8-44a5-aeca-70c1b5485823",
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_get_ugc_game_variant(client):
    await client.get_ugc_game_variant(
        asset_id="3899e110-91cd-4479-a8ad-5f8f8b91248d",
        version_id="9f315128-fe6f-4161-a52e-b35cb563dc2c",
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_get_playlist(client):
    await client.get_playlist(
        asset_id="edfef3ac-9cbe-4fa2-b949-8f29deafd483",
        version_id="bd985d58-2857-409d-8523-1917072f7435",
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_get_map_mode_pair(client):
    await client.get_map_mode_pair(
        asset_id="69d25f16-bc62-4d58-baf7-6210f65461f3",
        version_id="91ca22c3-e2a8-4586-8011-a4888f175d3e",
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_search_assets(client):
    await client.search_assets(count=5)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_film_by_match_id(client):
    await client.get_film_by_match_id(
        match_id="7f38edcc-7a9f-44a3-856e-7345f4c03175",
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_get_medal_metadata(client):
    await client.get_medal_metadata()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_csr_season_calendar(client):
    await client.get_csr_season_calendar()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_season_calendar(client):
    await client.get_season_calendar()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_career_reward_track(client):
    await client.get_career_reward_track()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_image(client):
    await client.get_image(
        relative_path="career_rank/NameplateAdornment/272_Hero.png",
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_get_current_user(client):
    await client.get_current_user()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_by_gamertag(client, current_user):
    await client.get_user_by_gamertag(gamertag=current_user.gamertag)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_by_id(client, current_user):
    await client.get_user_by_id(xuid=current_user.xuid)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_users_by_id(client, current_user):
    await client.get_users_by_id(
        xuids=[current_user.xuid],
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_get_match_skill(client, current_user):
    history = await client.get_match_history(
        current_user.xuid, count=1, match_type="matchmaking"
    )
    if not history.results:
        pytest.skip("Current user has no matchmade matches")
    await client.get_match_skill(
        match_id=history.results[0].match_id,
        xuids=[current_user.xuid],
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_get_playlist_csr(client, current_user):
    await client.get_playlist_csr(
        playlist_id="edfef3ac-9cbe-4fa2-b949-8f29deafd483",
        xuids=[current_user.xuid],
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_get_match_count(client, current_user):
    await client.get_match_count(player=current_user.xuid)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_service_record(client, current_user):
    await client.get_service_record(player=current_user.xuid)


@pytest.mark.asyncio(loop_scope="session")
async def test_match_stats(client):
    await client.get_match_stats(match_id="01b687a8-2f21-4041-997b-a60ff5fdce15")


@pytest.mark.asyncio(loop_scope="session")
async def test_get_player_customization(client, current_user):
    await client.get_player_customization(xuid=current_user.xuid)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_player_reward_track_operations(client, current_user):
    await client.get_player_reward_track_operations(xuid=current_user.xuid)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_player_career_rank(client, current_user):
    await client.get_player_career_rank(xuid=current_user.xuid)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_progression_file(client):
    await client.get_progression_file(
        relative_path="RewardTracks/CareerRanks/careerRank1.json"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_get_operation_reward_track(client):
    await client.get_operation_reward_track(
        reward_track_path="RewardTracks/Operations/S05OpPassM01.json"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_get_challenge_decks(client, current_user):
    await client.get_challenge_decks(player=current_user.xuid)
