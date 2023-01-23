import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from random import randrange



with open("token.txt", "r") as tokenFile:
    TOKEN = (tokenFile.readlines())[0].strip("\n")
    print(TOKEN)
    print()

GUILD_ID = discord.Object(id=1065377395655323728)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.client instead of discord.Client, the client will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=GUILD_ID)
        await self.tree.sync(guild=GUILD_ID)


intents = discord.Intents.all()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    """When the client is ready"""
    print(f"{client.user} is online")


@client.tree.command()
@app_commands.describe(
    opponent="Person you want to play against"
)
async def game(interaction: discord.Interaction, opponent: Optional[discord.Member] = None):
    emojis = ["🪨", "📄", "✂️"]
    verdict: str = ""

    # client v. human
    if opponent == None:
        opponent = interaction.user

        await interaction.response.send_message("Started")

        await opponent.send("how many rounds do you want to play?")
        roundsMessage = await client.wait_for("message", check=lambda message: message.author == opponent)
        rounds = int(roundsMessage.content)

        for i in range(rounds):
            client_choice = emojis[randrange(0, 2)]

            if randrange(1, 128) == 128:
                await opponent.send(f"I am going to play {client_choice} this round")
                lying = randrange(0, 2)

                # Basic client cheating
                if lying == 1 and client_choice == "🪨":
                    client_choice = "✂️"
                elif lying == 1 and client_choice == "📄":
                    client_choice = "🪨"
                elif lying == 1 and client_choice == "✂️":
                    client_choice = "📄"
                
                # Catch where the client is lying and there would be a tie
                elif lying == 3 and client_choice == "🪨":
                    client_choice = "📄"
                elif lying == 3 and client_choice == "📄":
                    client_choice = "✂️"
                elif lying == 3 and client_choice == "✂️":
                    client_choice = "🪨"

            clientMsg = await opponent.send("React with rock (🪨), paper(📄), or scissors(✂️) to show your choice")

            for emoji in emojis:
                await clientMsg.add_reaction(emoji)

            opponent_choice = await client.wait_for("reaction_add", check=lambda reaction, user: user == opponent and reaction.message.id == clientMsg.id)

            if opponent_choice[0].emoji == client_choice:
                verdict = "tie"
            elif opponent_choice[0].emoji == "🪨" and client_choice == "✂️":
                verdict = "win"
            elif opponent_choice[0].emoji == "🪨" and client_choice == "📄":
                verdict = "lose"
            elif opponent_choice[0].emoji == "📄" and client_choice == "🪨":
                verdict = "win"
            elif opponent_choice[0].emoji == "📄" and client_choice == "✂️":
                verdict = "lose"
            elif opponent_choice[0].emoji == "✂️" and client_choice == "📄":
                verdict = "win"
            elif opponent_choice[0].emoji == "✂️" and client_choice == "🪨":
                verdict = "lose"
            
            await opponent.send(f"you chose {opponent_choice[0].emoji}")

            if verdict == "tie":
                await opponent.send(f"I chose {client_choice}, which ties with your {opponent_choice[0].emoji}.")
            elif verdict == "win":
                await opponent.send(f"I chose {client_choice}, which loses to your {opponent_choice[0].emoji}.")
            elif verdict == "lose":
                await opponent.send(f"I chose {client_choice}, which beats your {opponent_choice[0].emoji}.")
    
    # human v. human
    else:
        player1 = interaction.user
        player2 = opponent

        await interaction.response.send_message("Started")


        await player1.send("how many rounds do you want to play?")
        roundsMessage = await client.wait_for("message", check=lambda message: message.author == player1)
        rounds = int(roundsMessage.content)

        for i in range(rounds):
            await player2.send("Please wait while your opponent to makes their choice.")

            # Player 1 turn
            clientMsgPlayer1 = await player1.send("React with rock (🪨), paper(📄), or scissors(✂️) to show your choice")
            for emoji in emojis:
                await clientMsgPlayer1.add_reaction(emoji)

            player1_choice = await client.wait_for("reaction_add", check=lambda reaction, user: user == player1 and reaction.message.id == clientMsgPlayer1.id) 

            # Player 2 turn
            clientMsgPlayer2 = await player2.send("React with rock (🪨), paper(📄), or scissors(✂️) to show your choice")
            for emoji in emojis:
                await clientMsgPlayer2.add_reaction(emoji)
            player2_choice = await client.wait_for("reaction_add", check=lambda reaction, user: user == player2 and reaction.message.id == clientMsgPlayer2.id)

            if player1_choice[0].emoji == player2_choice[0].emoji:
                verdict = "tie"
            elif player1_choice[0].emoji == "🪨" and player2_choice[0].emoji == "✂️":
                verdict = "player1 win"
            elif player1_choice[0].emoji == "🪨" and player2_choice[0].emoji == "📄":
                verdict = "player2 win"
            elif player1_choice[0].emoji == "📄" and player2_choice[0].emoji == "🪨":
                verdict = "player1 win"
            elif player1_choice[0].emoji == "📄" and player2_choice[0].emoji == "✂️":
                verdict = "player2 win"
            elif player1_choice[0].emoji == "✂️" and player2_choice[0].emoji == "📄":
                verdict = "player1 win"
            elif player1_choice[0].emoji == "✂️" and player2_choice[0].emoji == "🪨":
                verdict = "player2 win"
            
            await player1.send(f"you chose {player1_choice[0].emoji}")
            await player2.send(f"you chose {player2_choice[0].emoji}")

            if verdict == "tie":
                await player1.send(f"You chose {player1_choice[0].emoji}, which ties with {player2.name}'s {player2_choice[0].emoji}.")
                await player2.send(f"You chose {player2_choice[0].emoji}, which ties with {player1.name}'s {player1_choice[0].emoji}.")

            elif verdict == "player1 win":
                await player1.send(f"You chose {player1_choice[0].emoji}, which beats {player2.name}'s {player2_choice[0].emoji}.")
                await player2.send(f"You chose {player2_choice[0].emoji}, which loses to {player1.name}'s {player1_choice[0].emoji}.")

            elif verdict == "player2 win":
                await player1.send(f"You chose {player1_choice[0].emoji}, which loses to {player2.name}'s {player2_choice[0].emoji}.")
                await player2.send(f"You chose {player2_choice[0].emoji}, which beats {player1.name}'s {player1_choice[0].emoji}.")


client.run(TOKEN)
