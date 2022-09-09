from typing import List
import cassiopeia as cass
import discord
from discord import app_commands
from decouple import config

DISCORD_GUILD = config("GUILD_ID")


class league_bot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=DISCORD_GUILD))
            self.synced = True
        print(f"We have logged in as {self.user}")


client = league_bot()
tree = app_commands.CommandTree(client)


@tree.command(name="build", description="check build for champion", guild=discord.Object(id=DISCORD_GUILD))
async def build(interaction: discord.Interaction, champion: str):
    await interaction.response.send_message(f"Hello, here's the build for {champion} that you requested.",
                                            ephemeral=True)


@build.autocomplete('champion')
async def builds_autocomplete(
        interaction: discord.Interaction,
        current: str,
) -> List[app_commands.Choice[str]]:
    champions = [champ.name for champ in cass.get_champions("EUW")]
    return [
        app_commands.Choice(name=champion, value=champion)
        for champion in champions if current in champion
    ]


client.run(config("CLIENT_RUN_KEY"))
