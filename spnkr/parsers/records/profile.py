"""Parsing functions for the "profile" authority."""

from typing import NamedTuple


class User(NamedTuple):
    """High-level information about an Xbox Live user.

    Attributes:
        xuid: Xbox user ID.
        gamertag: User's gamertag.\
        gamerpic: URL to the user's gamerpic (1080x1080 PNG). The URL will
            accept additional query parameters `w` and `h` to request a smaller
            image having pixel width and height dimensions, respectively. Known
            sizes are 64x64, 208x208, and 424x424. For example, "&w=424&h=424".
    """

    xuid: int
    gamertag: str
    gamerpic: str


def parse_users(data: list[dict]) -> list[User]:
    """Parse a list of users from the "get_users" client response.

    Args:
        data: A "get_users" response from the client.

    Returns:
        List of parsed users.
    """
    return [_parse_user(user) for user in data]


def _parse_user(data: dict) -> User:
    """Parse a single user from an item in the "get_users" array response."""
    return User(
        xuid=int(data["xuid"]),
        gamertag=data["gamertag"],
        gamerpic=data["gamerpic"]["xlarge"],
    )
