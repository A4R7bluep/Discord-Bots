import discord
from discord import app_commands

from bs4 import BeautifulSoup
import requests

with open("token.txt", "r") as tokenFile:
    TOKEN = (tokenFile.readlines())[1].strip("\n")

GUILD_ID = discord.Object(id=1088953784090251284)


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD_ID)
        await self.tree.sync(guild=GUILD_ID)


intents = discord.Intents.all()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    """When the client is ready"""
    print(f"{client.user} is online")


@client.tree.command(description="returns the definition of the word")
@app_commands.describe(word="Word to look up")
async def define(interaction: discord.Interaction, word: str):
    url = "https://www.merriam-webster.com/dictionary/" + word

    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    definition = soup.find(attrs={"class": "dtText"}).text.split(": ")[1]

    await interaction.response.send_message(f"# {word}:\n ```{definition}```")


@client.tree.command(description="returns the etymology of the word")
@app_commands.describe(word="Word to look up")
async def etymology(interaction: discord.Interaction, word: str):
    url = "https://www.merriam-webster.com/dictionary/" + word

    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    etymology = soup.find(attrs={"class": "et"}).text.strip()

    await interaction.response.send_message(f"# {word}:\n ```{etymology}```")


@client.tree.command(description="returns the synonyms of the word")
@app_commands.describe(word="Word to look up")
async def synonyms(interaction: discord.Interaction, word: str):
    url = "https://www.merriam-webster.com/thesaurus/" + word

    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    synonyms = soup.find(attrs={"class": "thes-list-content"}).text.strip().split()
    synonymStr = ""

    for i in range(len(synonyms)):
        if i == len(synonyms):
            synonymStr += synonyms[i]
        else:
            synonymStr += synonyms[i] + ", "

    await interaction.response.send_message(f"# {word}:\n ```{synonymStr}```")


client.run(TOKEN)
