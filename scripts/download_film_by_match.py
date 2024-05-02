"""Download and decompress all film chunks for a given match ID."""

import argparse
import asyncio
import os
import zlib
from pathlib import Path

import dotenv
from aiohttp import ClientSession

from spnkr.auth import AzureApp, refresh_player_tokens
from spnkr.client import HaloInfiniteClient

dotenv.load_dotenv()

REFRESH_TOKEN = os.environ["SPNKR_REFRESH_TOKEN"]
CLIENT_ID = os.environ["SPNKR_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPNKR_CLIENT_SECRET"]
REDIRECT_URI = os.environ["SPNKR_REDIRECT_URI"]


async def main(match_id: str, output_dir: Path) -> None:
    directory = output_dir / match_id
    directory.mkdir(parents=True, exist_ok=True)

    app = AzureApp(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    async with ClientSession() as session:
        player = await refresh_player_tokens(session, app, REFRESH_TOKEN)
        client = HaloInfiniteClient(
            session=session,
            spartan_token=player.spartan_token.token,
            clearance_token=player.clearance_token.token,
        )
        film = await client.discovery_ugc.get_film_by_match_id(match_id)

        for chunk, url in film.get_chunks_and_urls():
            chunk_type = chunk.chunk_type.name.lower()
            print(f"Chunk(index={chunk.index} type={chunk_type})")
            response = await session.get(url)
            uncompressed = zlib.decompress(await response.content.read())
            with open(directory / f"{chunk.index}_{chunk_type}.bin", "wb") as f:
                f.write(uncompressed)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("match_id")
    parser.add_argument("--output_dir", type=Path, default=Path("films"))
    args = parser.parse_args()

    asyncio.run(main(args.match_id, args.output_dir))
