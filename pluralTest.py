import discord
from discord import app_commands


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


@client.tree.command(description="testing")
@app_commands.describe(message="Your message you want to send")
async def define(interaction: discord.Interaction, word: str):
    pass


client.run(TOKEN)
