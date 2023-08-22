"""Test the spnkr.auth.player module."""

from spnkr.auth import halo, player


def test_authenticated_player_is_valid_true():
    """Test that the authenticated player is valid."""
    expires_utc = {"ISO8601Date": "2999-09-01T00:00:00.000Z"}
    spartan_token = halo.SpartanToken({"ExpiresUtc": expires_utc})
    clearance_token = halo.ClearanceToken({"FlightConfigurationId": "token"})
    authenticated_player = player.AuthenticatedPlayer(
        "player_id",
        "gamertag",
        spartan_token,
        clearance_token,
    )
    assert authenticated_player.is_valid


def test_authenticated_player_is_valid_false():
    """Test that the authenticated player is not valid."""
    expires_utc = {"ISO8601Date": "1999-09-01T00:00:00.000Z"}
    spartan_token = halo.SpartanToken({"ExpiresUtc": expires_utc})
    clearance_token = halo.ClearanceToken({"FlightConfigurationId": "token"})
    authenticated_player = player.AuthenticatedPlayer(
        "player_id",
        "gamertag",
        spartan_token,
        clearance_token,
    )
    assert not authenticated_player.is_valid
