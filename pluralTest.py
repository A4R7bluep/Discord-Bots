import discord
from discord import app_commands, Webhook, Guild, Forbidden
from discord.ext.commands import has_permissions
from typing import Optional

import json


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
webhookName = "MorganaPlural"

"""To properly import for the first time, the json file needs only curly braces"""
with open("pluralTree.json", "r") as treeJson:
    fileAsStr = treeJson.read()
    hookTree = json.loads(fileAsStr)
    print("Imported tree from ./pluralTree.json!")


@client.event
async def on_ready():
    """When the client is ready"""
    print(f"{client.user} is online")


# @client.tree.command(description="sends a proxied message")
# @app_commands.describe(message="Your message", hookname="username of webhook")
# async def hooksend(interaction: discord.Interaction, message: str, hookname: str):
#     foundHook = False
#     # hooks =

#     for hook in await interaction.guild.webhooks():
#         if hook.name == f"CustomPlural: {hookname}":
#             await hook.send(content='Hello World', username=hookname)
#             await interaction.response.send_message("hook sent message hopefully", ephemeral=True)
#             foundHook = True

#     if foundHook == False:
#         await interaction.channel.create_webhook(name=f"CustomPlural: {hookname}")

#         # hooks =
#         for hook in await interaction.channel.webhooks():
#             if hook.name == f"CustomPlural: {hookname}":
#                 await hook.send(content='Hello World', username=hookname)
#                 await interaction.response.send_message("hook sent message hopefully", ephemeral=True)

# class Proxy:
#     proxyname: str
#     avatarurl: str

#     def __init__(self, proxyname, avatarurl):
#         self.proxyname = proxyname
#         self.avatarurl = avatarurl


async def get_webhook(interaction: discord.Interaction):
    found = False
    for hook in await interaction.guild.webhooks():
        if hook.name == webhookName:
            return hook

    if not found:
        await interaction.channel.create_webhook(name=webhookName)


@client.tree.command(description="sends a proxied message")
@app_commands.describe(message="Your message", proxyname="username of webhook")
async def hooksend(interaction: discord.Interaction, message: str, proxyname: str):
    hook = await get_webhook(interaction)
    proxy = hookTree[str(interaction.user.id)][proxyname]

    await hook.send(content=message, username=proxyname, avatar_url=proxy["AvatarURL"])
    await interaction.response.send_message(
        "hook sent message hopefully", ephemeral=True
    )


@client.tree.command(description="Creates a proxy's account")
@app_commands.describe(
    proxyname="Name your proxy",
    avatarurl="Image to use as the pfp",
    default="Makes it the main proxy",
)
async def makeproxy(
    interaction: discord.Interaction, proxyname: str, avatarurl: Optional[str]
):
    # if default == True:
    #     if not str(interaction.user.id) in dictionary:
    #         dictionary[str(interaction.user.id)] = {}

    #     dictionary[str(interaction.user.id)]["default"] = Proxy(proxyname, avatarurl)
    # else:
    if not str(interaction.user.id) in hookTree:
        hookTree[str(interaction.user.id)] = {}

    hookTree[str(interaction.user.id)][proxyname] = {
        "User": str(interaction.user.id),
        "AvatarURL": avatarurl,
    }
    jsonText = json.dumps(hookTree)

    with open("pluralTree.json", "w") as treeJson:
        treeJson.write(jsonText)

    await interaction.response.send_message(f"Proxy {proxyname} made!", ephemeral=True)


@has_permissions(administrator=True)
@client.tree.command(description="returns the user who used the hooksend")
@app_commands.describe(message_id="Message ID")
async def gethookuser(interaction: discord.Interaction, message_id: str):
    await interaction.response.send_message(0)


client.run(TOKEN)
