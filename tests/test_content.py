"""Test the HIUGC_Discovery authority."""

from spnkr.api.client import Client


def test_get_custom_game_manifest(client: Client):
    result = client.ugc_discovery.get_custom_game_manifest()
    assert result.asset_id is not None


def test_get_engine_game_variant_without_version(client: Client):
    asset_id = "6ea0d1e7-57f7-4658-ac1e-7223cbb4f765"
    result = client.ugc_discovery.get_engine_game_variant_without_version(
        asset_id
    )
    assert result.asset_id is not None


def test_get_manifest(client: Client):
    asset_id = "6369c3a6-390e-496c-ab71-93c326347327"
    version_id = "9a348b5b-08aa-41c2-8b3a-681870c78a76"
    result = client.ugc_discovery.get_manifest(asset_id, version_id)
    assert result.asset_id is not None


def test_get_manifest_by_build(client: Client):
    build_number = "6.10022.13411"
    result = client.ugc_discovery.get_manifest_by_build(build_number)
    assert result.asset_id is not None


def test_get_map_mode_pair(client: Client):
    asset_id = "95018e68-41fc-4d5f-b627-15590feb7469"
    version_id = "fad19fca-afa8-41c4-a3d9-3da96c248a1e"
    result = client.ugc_discovery.get_map_mode_pair(asset_id, version_id)
    assert result.asset_id is not None


# def test_get_map_mode_pair_without_version(client: Client):
#     # TODO fails with 404
#     asset_id = 'b6aca0c7-8ba7-4066-bf91-693571374c3c'  # sgh_interlock
#     result = client.ugc_discovery.get_map_mode_pair_without_version(asset_id)
#     # assert result.asset_id is not None


def test_get_map_without_version(client: Client):
    asset_id = "8420410b-044d-44d7-80b6-98a766c8c39f"  # Recharge
    result = client.ugc_discovery.get_map_without_version(asset_id)
    assert result.asset_id is not None


def test_get_playlist(client: Client):
    # 404
    asset_id = "edfef3ac-9cbe-4fa2-b949-8f29deafd483"  # Ranked Open
    version_id = "6c1bb887-628f-4a16-a794-f07adad39a38"
    result = client.ugc_discovery.get_playlist(asset_id, version_id)
    assert result.asset_id is not None


def test_get_playlist_without_version(client: Client):
    asset_id = "0fb8a1cc-634f-4133-9eff-2c54f79d55c8"  # Ranked Arena
    result = client.ugc_discovery.get_playlist_without_version(asset_id)
    assert result.asset_id is not None


def test_get_prefab(client: Client):
    # 404
    asset_id = "568fa365-6cdf-42c6-9d2a-751c676118a2"  # f?
    version_id = "d9e73ad7-ff48-46a1-b5cd-3ca5754aa461"
    result = client.ugc_discovery.get_prefab(asset_id, version_id)
    assert result.asset_id is not None


def test_get_prefab_without_version(client: Client):
    # 404
    asset_id = "568fa365-6cdf-42c6-9d2a-751c676118a2"  # f?
    result = client.ugc_discovery.get_prefab_without_version(asset_id)
    assert result.asset_id is not None


def test_get_project(client: Client):
    # 404
    asset_id = "a9dc0785-2a99-4fec-ba6e-0216feaaf041"  # custom game manifest
    version_id = "a4e68648-f994-44bb-853e-d09ee224d799"
    result = client.ugc_discovery.get_project(asset_id, version_id)
    assert result.asset_id is not None


def test_get_project_without_version(client: Client):
    asset_id = "a9dc0785-2a99-4fec-ba6e-0216feaaf041"  # custom game manifest
    result = client.ugc_discovery.get_project_without_version(asset_id)
    assert result.asset_id is not None


def test_get_tags_info(client: Client):
    result = client.ugc_discovery.get_tags_info()
    assert len(result.canned_tags) > 0


def test_get_ugc_game_variant_without_version(client: Client):
    asset_id = "aca7bbf8-7a18-4aae-8785-1bd3f58275fd"  # Fiesta Slayer
    result = client.ugc_discovery.get_ugc_game_variant_without_version(asset_id)
    assert result.asset_id is not None


def test_search(client: Client):
    result = client.ugc_discovery.search(count=1)
    assert result.result_count > 0


def test_spectate_by_match_id(client: Client):
    # 404
    match_id = "6f050134-bede-47bc-a6df-eeafdcb9f97f"
    result = client.ugc_discovery.spectate_by_match_id(match_id)
    assert result.asset_id is not None


def test_get_engine_gamevariant(client: Client):
    asset_id = "6ea0d1e7-57f7-4658-ac1e-7223cbb4f765"
    version_id = "241f10a0-b997-40bf-b2b6-5de1b35c9ee1"
    result = client.ugc_discovery.get_engine_gamevariant(asset_id, version_id)
    assert result.asset_id is not None


def test_get_map(client: Client):
    asset_id = "76669255-697d-48c9-a802-7ff2ec8257f1"
    version_id = "b8abf687-4e95-4846-83c7-33e779eed33e"
    result = client.ugc_discovery.get_map(asset_id, version_id)
    assert result.asset_id is not None


def test_get_ugc_game_variant(client: Client):
    asset_id = "aca7bbf8-7a18-4aae-8785-1bd3f58275fd"
    version_id = "3685f6b2-2860-4e98-9d13-513087edb465"
    result = client.ugc_discovery.get_ugc_game_variant(asset_id, version_id)
    assert result.asset_id is not None
