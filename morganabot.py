from typing import Literal, Optional, Union
import discord
from discord import app_commands
from discord.ext.commands import Greedy, Context
from discord.ext import commands
import asyncio

# Get token and guilds from files
with open("token.txt", "r") as tokenFile:
    TOKEN = (tokenFile.readlines())[1].strip("\n")
    # print(TOKEN)
    # print()

with open("slashguilds.txt", "r") as guildFile:
    guilds = guildFile.readlines()
    for i in range(len(guilds)):
        guilds[i] = guilds[i].strip("\n")
    # print(guilds)
    # print()

# Prepare discord data
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="!")


# Select menu classes
class TransactionRoleSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Commissioner"),
            discord.SelectOption(label="Commissioned"),
        ]
        super().__init__(
            placeholder="Are you the commissioner or being commissioned?",
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        pass


class TransactionRoleView(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.transactionRoleSelect = TransactionRoleSelect()
        self.add_item(self.transactionRoleSelect)


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


@bot.tree.command(
    name="secure-transaction",
    description="Command for making commission transactions as to not be scammed",
)
async def secure_transaction(
    interaction: discord.Interaction,
    user: discord.Member,
    choice: Union[Literal["USD", "Robux", "Nitro"], Literal["USD", "Robux", "Nitro"]],
):
    await interaction.response.send_message(
        f"Transaction with {user.mention} opened. The transaction will be in {choice}"
    )

    selectView = TransactionRoleView()
    await interaction.followup.send(
        f"Are you the commissioner? or are you being commissioned?",
        ephemeral=True,
        view=selectView,
    )

    while selectView.transactionRoleSelect.values == []:
        await asyncio.sleep(1)

    transactionRole = selectView.transactionRoleSelect.values[0].lower()

    if transactionRole == "commissioner":
        commissioner = interaction.user
        commissioned = user
    else:
        commissioner = user
        commissioned = interaction.user

    if choice == "Nitro":
        await commissioner.send(
            "Please send the Nitro link to me. I'll pass it on to the commissioner when the commissioned person has given me the files."
        )
        payment = await bot.wait_for(
            "message",
            check=lambda message: message.author == commissioner
            and message.channel == commissioner,
        )

        await commissioned.send(
            "Please send the files to me. I'll pass them on to the commissioner when they have given me the Nitro link."
        )
        work = await bot.wait_for(
            "message",
            check=lambda message: message.author == commissioned
            and message.channel == commissioned,
        )


# Sync command - run after updating command tree by using "!sync"
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
