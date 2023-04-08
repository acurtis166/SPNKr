from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AzureApp:
    """Represents an Azure AD application."""

    client_id: str
    client_secret: str
    redirect_uri: str
