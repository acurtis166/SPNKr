"""An Azure AD application."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AzureApp:
    """An Azure Active Directory (Azure AD) application.

    Azure AD is a cloud-based identity and access management service from
    Microsoft. It allows you to sign in and access Microsoft resources from an
    application.

    Attributes:
        client_id (str): The client ID of the application.
        client_secret (str): The client secret of the application.
        redirect_uri (str): The redirect URI of the application.
    """

    client_id: str
    client_secret: str
    redirect_uri: str = "https://localhost"
