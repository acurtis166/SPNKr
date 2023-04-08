"""Example usage of the SPNKR API."""

import asyncio

import aiohttp

from spnkr import SPNKR, AzureApp


async def main():
    app = AzureApp("CLIENT_ID", "CLIENT_SECRET", "REDIRECT_URI")
    refresh_token = "REFRESH_TOKEN"

    async with SPNKR(app, refresh_token) as spnkr:
        # Get your Xbox Live ID
        xuid = await spnkr.get_my_xuid()
        print(f"Xbox Live ID: {xuid}")

        # Get your gamertag
        gamertag = await spnkr.get_my_gamertag()
        print(f"Gamertag: {gamertag}")

        # Get your most recent matches
        matches = await spnkr.get_match_history(xuid)
        most_recent_match = matches.matches[0]
        print(f"Last match played at {most_recent_match.info.start}")

        # Get match stats for the most recent match
        stats = await spnkr.get_match_stats(str(most_recent_match.id))
        player_stats = stats.players[0].last_team_stats.core
        print("Kills:", player_stats.kills)
        print("Deaths:", player_stats.deaths)
        print("Assists:", player_stats.assists)

        # Get all the human players from the match
        player_ids = [p.xuid for p in stats.players if p.is_human]

        # Get skill info for the match
        try:
            skill = await spnkr.get_match_skill(
                str(most_recent_match.id), player_ids
            )
        except aiohttp.ClientResponseError:
            print("Skill info not available for this match.")
        else:
            print("Skill info for match:")
            for xuid, result in skill.results.items():
                pre_match_csr = result.pre_match_csr
                print("Pre-match CSR:", pre_match_csr.value)
                post_match_csr = result.post_match_csr
                print("Post-match CSR:", post_match_csr.value)


if __name__ == "__main__":
    asyncio.run(main())
