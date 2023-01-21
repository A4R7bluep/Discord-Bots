from typing import Literal, Optional
import discord
from discord.ext.commands import Greedy, Context
from discord.ext import commands

# Get token and guilds from files
with open("token.txt", "r") as tokenFile:
    TOKEN = (tokenFile.readlines())[1].strip("\n")
    print(TOKEN)
    print()

with open("slashguilds.txt", "r") as guildFile:
    guilds = guildFile.readlines()
    for i in range(len(guilds)):
        guilds[i] = guilds[i].strip("\n")
    print(guilds)
    print()

# Prepare discord data
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="!")

# Onready notice
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Bot user id: {bot.user.id}")

# Slash command tree
@bot.tree.command(name="ping", description="Test command")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong!", ephemeral=True)

@bot.tree.command(name="args", description="args test")
async def args(interaction: discord.Interaction, arg1: str):
    await interaction.response.send_message(arg1, ephemeral=True)

'''Would not work because of a way the person who made the commission could be scammed'''
# @bot.tree.command(name="secure-transaction", description="Command for making commission transactions as to not be scammed")
# async def secure_transaction(interaction: discord.Interaction, user: discord.Member, *files: discord.file):
#     await user.send(f"{interaction.user} has initiated a secure transaction.")
#     await user.send("They have finished the work. Send the payment and I will send you the files.")
#     await user.sent("React with ✅ when you have sent the payment.")


# Sync command - run after updating command tree and use "!sync"
@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
    ctx: Context,
    guilds: Greedy[discord.Object],
    spec: Optional[Literal["~", "*", "^"]] = None,
) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


bot.run(TOKEN)
