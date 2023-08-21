"""An Azure AD application."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AzureApp:
    """An Azure AD application.

    Attributes:
        client_id (str): The client ID of the application.
        client_secret (str): The client secret of the application.
        redirect_uri (str): The redirect URI of the application.
    """

    client_id: str
    client_secret: str
    redirect_uri: str = "https://localhost"
