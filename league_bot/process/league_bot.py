import discord
import certifi
import asyncio
from decouple import config
from io import BytesIO
from pymongo import MongoClient
from pymongo.server_api import ServerApi

ca = certifi.where()
DISCORD_GUILD = config("GUILD_ID")


class LeagueBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=DISCORD_GUILD))
            self.synced = True
        print(f"We have logged in as {self.user}")


client = LeagueBot()
tree = discord.app_commands.CommandTree(client)


@tree.command(name="champ_helper", description="check required builds/runes/skills for entered champion",
              guild=discord.Object(id=DISCORD_GUILD))
async def champ_helper(interaction: discord.Interaction, requested_info: str, champion: str):
    await interaction.response.defer()
    await asyncio.sleep(1)
    db_client = MongoClient(
        f"mongodb+srv://{config('MONGODB_USERNAME')}:{config('MONGODB_PASSWORD')}@leaguebot.3wl3vhh.mongodb.net/?retryWrites=true&w=majority",
        server_api=ServerApi('1'), tlsCAFile=ca)
    league_db = db_client["leaguebot"]
    champions = league_db["champions"]
    champ = champions.find({"name": champion})
    file = BytesIO(champ[0][requested_info])

    # pm the user the div as an image
    await interaction.followup.send(file=discord.File(file, "image.png"), ephemeral=True)


@client.event
async def on_presence_update(before, after):
    activity = after.activity
    if activity and activity.name == "League of Legends" and activity.state == "In Game":
        champion = activity.large_image_text.lower().replace("'", "").replace(".", "").replace(" ", "")
        if champion == "nunu&willump":
            champion = "nunu"
        elif champion == "renataglasc":
            champion = "renata"
        user = client.get_user(after.id)
        await user.send(
            f"Hey, I noticed you are playing {champion.capitalize()}. "
            "Here are some pieces of information that might help you out."
        )
        db_client = MongoClient(
            f"mongodb+srv://{config('MONGODB_USERNAME')}:{config('MONGODB_PASSWORD')}@leaguebot.3wl3vhh.mongodb.net/?retryWrites=true&w=majority",
            server_api=ServerApi('1'), tlsCAFile=ca)
        league_db = db_client["leaguebot"]
        champions = league_db["champions"]
        champ = champions.find({"name": champion})
        skill_file = BytesIO(champ[0]["skills"])
        await user.send(
            f"This is the skilling order for {champion.capitalize()}.",
            file=discord.File(skill_file, "image.png"),
        )

        build_file = BytesIO(champ[0]["build"])
        await user.send(
            f"These are the items you should be building for {champion.capitalize()}, in order.",
            file=discord.File(build_file, "image.png"),
        )


client.run(config("CLIENT_RUN_KEY"))
