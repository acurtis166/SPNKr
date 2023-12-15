"""Models for the "profile" authority."""

from pydantic import BaseModel


class GamerPicture(BaseModel, frozen=True):
    """URLs to different sizes of a user's gamerpic.

    Attributes:
        small: 64x64 PNG
        medium: 208x208 PNG
        large: 424x424 PNG
        xlarge: 1080x1080 PNG
    """

    small: str
    medium: str
    large: str
    xlarge: str


class User(BaseModel, frozen=True):
    """High-level information about an Xbox Live user.

    Attributes:
        xuid: Xbox user ID.
        gamertag: User's gamertag.
        gamerpic: URLs to different sizes of the user's gamerpic.
    """

    xuid: int
    gamertag: str
    gamerpic: GamerPicture
