from aiohttp import ClientSession

from spnkr.auth import AzureApp, refresh_player_tokens
from spnkr.client import HaloInfiniteClient
from spnkr.parsers.pydantic import PydanticParser


async def main():
    refresh_token = ""
    app = AzureApp("", "", "")
    parser = PydanticParser(validate=True)

    async with ClientSession() as session:
        tokens = await refresh_player_tokens(session, refresh_token, app)
        client = HaloInfiniteClient(
            session=session,
            spartan_token=tokens.spartan_token.token,
            clearance_token=tokens.clearance_token.token,
        )
        match_skill = await client.get_match_skill(
            match_id="",
            xuids=[""],
        )
        match_skill = await parser.parse_match_skill(match_skill)
        print(match_skill)
