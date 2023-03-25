"""Endpoints for the "HIUGC_Discovery" and "HIUGC_Discovery_Open" authorities."""

from spnkr.api.enums import (
    AssetKind,
    AuthenticationMethod,
    ResultOrder,
    SearchProperty,
)
from spnkr.api.authorities.base import BaseAuthority
from spnkr.api.authorities.ugc_discovery import models


class UgcDiscoveryAuthority(BaseAuthority):
    URL = "https://discovery-infiniteugc.svc.halowaypoint.com:443"

    def get_manifest(
        self, asset_id: str, version_id: str, clearance_id: str | None = None
    ) -> models.Manifest:
        url = self.URL + f"/hi/manifests/{asset_id}/versions/{version_id}"
        params = (
            dict(clearanceId=clearance_id) if clearance_id is not None else None
        )
        resp = self._session.get(url, params=params)
        resp.raise_for_status()
        return models.Manifest.from_dict(resp.json())

    def get_manifest_by_build(self, build_number: str) -> models.Manifest:
        url = self.URL + f"/hi/manifests/builds/{build_number}/game"
        resp = self._session.get(url)
        resp.raise_for_status()
        return models.Manifest.from_dict(resp.json())

    def get_custom_game_manifest(self) -> models.Manifest:
        url = self.URL + "/hi/projects/a9dc0785-2a99-4fec-ba6e-0216feaaf041"
        resp = self._session.get(url)
        resp.raise_for_status()
        return models.Manifest.from_dict(resp.json())

    def get_engine_gamevariant(
        self, asset_id: str, version_id: str
    ) -> models.EngineGameVariant:
        url = (
            self.URL
            + f"/hi/engineGameVariants/{asset_id}/versions/{version_id}"
        )
        resp = self._session.get(url)
        resp.raise_for_status()
        return models.EngineGameVariant.from_dict(resp.json())

    def get_engine_game_variant_without_version(
        self, asset_id: str
    ) -> models.EngineGameVariant:
        url = self.URL + f"/hi/engineGameVariants/{asset_id}"
        resp = self._session.get(url)
        resp.raise_for_status()
        return models.EngineGameVariant.from_dict(resp.json())

    def get_ugc_game_variant(
        self, asset_id: str, version_id: str
    ) -> models.UgcGameVariant:
        url = self.URL + f"/hi/ugcGameVariants/{asset_id}/versions/{version_id}"
        resp = self._session.get(url)
        resp.raise_for_status()
        return models.UgcGameVariant.from_dict(resp.json())

    def get_ugc_game_variant_without_version(
        self, asset_id: str
    ) -> models.UgcGameVariant:
        url = self.URL + f"/hi/ugcGameVariants/{asset_id}"
        resp = self._session.get(url)
        resp.raise_for_status()
        return models.UgcGameVariant.from_dict(resp.json())

    def get_map_mode_pair(
        self, asset_id: str, version_id: str, clearance_id: str | None = None
    ) -> models.MapModePair:
        url = self.URL + f"/hi/mapModePairs/{asset_id}/versions/{version_id}"
        params = (
            dict(clearanceId=clearance_id) if clearance_id is not None else None
        )
        resp = self._session.get(url, params=params)
        resp.raise_for_status()
        return models.MapModePair.from_dict(resp.json())

    def get_map_mode_pair_without_version(
        self, asset_id: str
    ) -> models.MapModePair:
        """Work in progress, currently only returns 404."""
        url = self.URL + f"/hi/mapModePairs/{asset_id}"
        resp = self._session.get(url)
        resp.raise_for_status()
        return resp.text  # type: ignore

    def get_map(self, asset_id: str, version_id: str) -> models.Map:
        url = self.URL + f"/hi/maps/{asset_id}/versions/{version_id}"
        resp = self._session.get(url)
        resp.raise_for_status()
        return models.Map.from_dict(resp.json())

    def get_map_without_version(self, asset_id: str) -> models.Map:
        url = self.URL + f"/hi/maps/{asset_id}"
        resp = self._session.get(url)
        resp.raise_for_status()
        return models.Map.from_dict(resp.json())

    def get_playlist(
        self, asset_id: str, version_id: str, clearance_id: str | None = None
    ) -> models.Playlist:
        url = self.URL + f"/hi/playlists/{asset_id}/versions/{version_id}"
        params = (
            dict(clearanceId=clearance_id) if clearance_id is not None else None
        )
        resp = self._session.get(url, params=params)
        resp.raise_for_status()
        return models.Playlist.from_dict(resp.json())

    def get_playlist_without_version(self, asset_id: str) -> models.Playlist:
        url = self.URL + f"/hi/playlists/{asset_id}"
        resp = self._session.get(url)
        resp.raise_for_status()
        return models.Playlist.from_dict(resp.json())

    def get_prefab(self, asset_id: str, version_id: str) -> models.Prefab:
        url = self.URL + f"/hi/prefabs/{asset_id}/versions/{version_id}"
        resp = self._session.get(url)
        resp.raise_for_status()
        return models.Prefab.from_dict(resp.json())

    def get_prefab_without_version(self, asset_id: str) -> models.Prefab:
        url = self.URL + f"/hi/prefabs/{asset_id}"
        resp = self._session.get(url)
        resp.raise_for_status()
        return models.Prefab.from_dict(resp.json())

    def get_project(self, asset_id: str, version_id: str) -> models.Project:
        url = self.URL + f"/hi/projects/{asset_id}/versions/{version_id}"
        resp = self._session.get(url)
        resp.raise_for_status()
        return models.Project.from_dict(resp.json())

    def get_project_without_version(self, asset_id: str) -> models.Project:
        url = self.URL + f"/hi/projects/{asset_id}"
        resp = self._session.get(url)
        resp.raise_for_status()
        return models.Project.from_dict(resp.json())

    def get_tags_info(self) -> models.TagsInfo:
        url = self.URL + "/hi/info/tags"
        resp = self._session.get(
            url, auth_method=AuthenticationMethod.ClearanceToken
        )
        resp.raise_for_status()
        return models.TagsInfo.from_dict(resp.json())

    def search(
        self,
        start: int = 0,
        count: int = 101,
        sort: SearchProperty = SearchProperty.PlaysRecent,
        order: ResultOrder = ResultOrder.Desc,
        asset_kind: AssetKind | None = None,
    ) -> models.Search:
        """Search for assets in the user-generated content directory.

        Args:
            start (int): Number of results from which to offset the result set, starting at 0.
            count (int): Count of results to return. Max 101.
            sort (enums.SearchProperty): Property by which to sort the results. Example is "PlaysRecent".
            order (enums.ResultOrder): Determines whether results are ordered in descending or ascending order.
            asset_kind (enums.AssetKind): Type of asset to be searched.
        """
        url = self.URL + "/hi/search"
        params = {
            "start": start,
            "count": count,
            "sort": sort.name,
            "order": order.name,
            "assetKind": asset_kind.name if asset_kind is not None else None,
        }
        resp = self._session.get(url, params=params)
        resp.raise_for_status()
        return models.Search.from_dict(resp.json())

    def spectate_by_match_id(self, match_id: str) -> models.Film:
        url = self.URL + f"/hi/films/matches/{match_id}/spectate"
        resp = self._session.get(url)
        resp.raise_for_status()
        return models.Film.from_dict(resp.json())

    # HTTP 404 - Not Found for "6369c3a6-390e-496c-ab71-93c326347327" asset id on 9/9/2022
    # def get_manifest_without_version(self, asset_id: str):
    #     url = self.URL + f'/hi/manifests/{asset_id}'
    #     resp = self._session.get(url)
    #     resp.raise_for_status()
    #     return resp.text

    # HTTP 403 - Forbidden for "HIRC" branch name on 9/9/2022
    # def get_manifest_by_branch(self, branch_name: str):
    #     url = self.URL + f'/hi/manifests/branches/{branch_name}/game'
    #     resp = self._session.get(url)
    #     resp.raise_for_status()
    #     return resp.text
