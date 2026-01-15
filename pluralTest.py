import discord
from discord import app_commands, Webhook, Guild, Forbidden
from discord.ext.commands import has_permissions
import aiohttp



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


@client.tree.command(description="sends a proxied message")
@app_commands.describe(message="Your message", hookname="username of webhook")
async def hooksend(interaction: discord.Interaction, message: str, hookname: str):
    foundHook = False
    # hooks = 
    
    for hook in await interaction.guild.webhooks():
        if hook.name == f"CustomPlural: {hookname}":
            await hook.send(content='Hello World', username=hookname)
            await interaction.response.send_message("hook sent message hopefully", ephemeral=True)
            foundHook = True

    if foundHook == False:
        await interaction.channel.create_webhook(name=f"CustomPlural: {hookname}")

        # hooks = 
        for hook in await interaction.channel.webhooks():
            if hook.name == f"CustomPlural: {hookname}":
                await hook.send(content='Hello World', username=hookname)
                await interaction.response.send_message("hook sent message hopefully", ephemeral=True)

@has_permissions(administrator=True)
@client.tree.command(description="returns the user who used the hooksend")
@app_commands.describe(message_id="Message ID")
async def get_hookuser(interaction: discord.Interaction, message_id: str):
    await interaction.response.send_message(0)


client.run(TOKEN)
