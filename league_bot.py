from decouple import config
import discord
from io import BytesIO
from pymongo import MongoClient
from pymongo.server_api import ServerApi

intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("__"):
        cmd = message.content.split()[0].replace("__", "")

        if cmd == "runes":
            if len(message.content.split()) > 1:
                champion = message.content.split()[1]
                if type(champion) != str or len(message.content.split()) > 2:
                    await message.channel.send("Please only call the function via __*action* *champion* *game_mode*.")
                else:
                    try:
                        db_client = MongoClient(
                            f"mongodb+srv://{config('MONGODB_USERNAME')}:{config('MONGODB_PASSWORD')}@leaguebot.3wl3vhh.mongodb.net/?retryWrites=true&w=majority",
                            server_api=ServerApi('1'))
                        league_db = db_client["leaguebot"]
                        champions = league_db["champions"]
                        champ = champions.find({"name": champion})
                    except:
                        await message.channel.send("Not a valid League Of Legends Champion.")
                    else:
                        file = BytesIO(champ[0]["runes"])

                        # pm the user the div as an image
                        await message.author.send(file=discord.File(file, "image.png"))
            else:
                await message.channel.send("Please supply a champion.")

        if cmd == "build":
            if len(message.content.split()) > 1:
                champion = message.content.split()[1]
                if type(champion) != str or len(message.content.split()) > 2:
                    await message.channel.send("Please only call the function via __*action* *champion* *game_mode*.")
                else:
                    try:
                        db_client = MongoClient(
                            f"mongodb+srv://{config('MONGODB_USERNAME')}:{config('MONGODB_PASSWORD')}@leaguebot.3wl3vhh.mongodb.net/?retryWrites=true&w=majority",
                            server_api=ServerApi('1'))
                        league_db = db_client["leaguebot"]
                        champions = league_db["champions"]
                        champ = champions.find({"name": champion})
                    except:
                        await message.channel.send("Not a valid League Of Legends Champion.")
                    else:
                        file = BytesIO(champ[0]["build"])

                        # pm the user the div as an image
                        await message.author.send(file=discord.File(file, "image.png"))
            else:
                await message.channel.send("Please supply a champion.")

        if cmd == "skills":
            if len(message.content.split()) > 1:
                champion = message.content.split()[1]
                if type(champion) != str or len(message.content.split()) > 2:
                    await message.channel.send("Please only call the function via __*action* *champion* *game_mode*.")
                else:
                    try:
                        db_client = MongoClient(
                            f"mongodb+srv://{config('MONGODB_USERNAME')}:{config('MONGODB_PASSWORD')}@leaguebot.3wl3vhh.mongodb.net/?retryWrites=true&w=majority",
                            server_api=ServerApi('1'))
                        league_db = db_client["leaguebot"]
                        champions = league_db["champions"]
                        champ = champions.find({"name": champion})
                    except:
                        await message.channel.send("Not a valid League Of Legends Champion.")
                    else:
                        file = BytesIO(champ[0]["skills"])

                        # pm the user the div as an image
                        await message.author.send(file=discord.File(file, "image.png"))
            else:
                await message.channel.send("Please supply a champion.")


@client.event
async def on_presence_update(before, after):
    activity = after.activity
    if activity and activity.name == "League of Legends" and activity.state == "In Game":
        champion = activity.large_image_text.lower().replace("'", "").replace(".", "").replace(" ", "")
        user = client.get_user(after.id)
        await user.send(
            f"Hey, I noticed you are playing {champion.capitalize()}. "
            "Here are some pieces of information that might help you out."
        )
        db_client = MongoClient(
            f"mongodb+srv://{config('MONGODB_USERNAME')}:{config('MONGODB_PASSWORD')}@leaguebot.3wl3vhh.mongodb.net/?retryWrites=true&w=majority",
            server_api=ServerApi('1'))
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
