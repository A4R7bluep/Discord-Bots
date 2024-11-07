import discord
from discord.ext import commands
from random import randrange

with open("token.txt", "r") as tokenFile:
    TOKEN = (tokenFile.readlines())[0].strip("\n")
    print(TOKEN)
    print()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command("help")


@bot.event
async def on_ready():
    """When the bot is ready"""
    print("bot is online")


@bot.command()
async def game(ctx, opponent: discord.Member = None):
    emojis = ["🪨", "📄", "✂️"]
    verdict: str = ""

    # bot v. human
    if opponent == None:
        opponent = ctx.author

        await opponent.send("how many rounds do you want to play?")
        roundsMessage = await bot.wait_for("message", check=lambda message: message.author == opponent)
        rounds = int(roundsMessage.content)

        for i in range(rounds):
            bot_choice = emojis[randrange(0, 2)]

            if randrange(1, 128) == 128:
                await opponent.send(f"I am going to play {bot_choice} this round")
                lying = randrange(0, 2)

                # Basic bot cheating
                if lying == 1 and bot_choice == "🪨":
                    bot_choice = "✂️"
                elif lying == 1 and bot_choice == "📄":
                    bot_choice = "🪨"
                elif lying == 1 and bot_choice == "✂️":
                    bot_choice = "📄"
                
                # Catch where the bot is lying and there would be a tie
                elif lying == 3 and bot_choice == "🪨":
                    bot_choice = "📄"
                elif lying == 3 and bot_choice == "📄":
                    bot_choice = "✂️"
                elif lying == 3 and bot_choice == "✂️":
                    bot_choice = "🪨"

            botMsg = await opponent.send("React with rock (🪨), paper(📄), or scissors(✂️) to show your choice")

            for emoji in emojis:
                await botMsg.add_reaction(emoji)

            opponent_choice = await bot.wait_for("reaction_add", check=lambda reaction, user: user == opponent and reaction.message.id == botMsg.id)

            if opponent_choice[0].emoji == bot_choice:
                verdict = "tie"
            elif opponent_choice[0].emoji == "🪨" and bot_choice == "✂️":
                verdict = "win"
            elif opponent_choice[0].emoji == "🪨" and bot_choice == "📄":
                verdict = "lose"
            elif opponent_choice[0].emoji == "📄" and bot_choice == "🪨":
                verdict = "win"
            elif opponent_choice[0].emoji == "📄" and bot_choice == "✂️":
                verdict = "lose"
            elif opponent_choice[0].emoji == "✂️" and bot_choice == "📄":
                verdict = "win"
            elif opponent_choice[0].emoji == "✂️" and bot_choice == "🪨":
                verdict = "lose"
            
            await opponent.send(f"you chose {opponent_choice[0].emoji}")

            if verdict == "tie":
                await opponent.send(f"I chose {bot_choice}, which ties with your {opponent_choice[0].emoji}.")
            elif verdict == "win":
                await opponent.send(f"I chose {bot_choice}, which loses to your {opponent_choice[0].emoji}.")
            elif verdict == "lose":
                await opponent.send(f"I chose {bot_choice}, which beats your {opponent_choice[0].emoji}.")
    
    # human v. human
    else:
        player1 = ctx.author
        player2 = opponent

        await player1.send("how many rounds do you want to play?")
        roundsMessage = await bot.wait_for("message", check=lambda message: message.author == player1)
        rounds = int(roundsMessage.content)

        for i in range(rounds):
            await player2.send("Please wait while your opponent to makes their choice.")

            # Player 1 turn
            botMsgPlayer1 = await player1.send("React with rock (🪨), paper(📄), or scissors(✂️) to show your choice")
            for emoji in emojis:
                await botMsgPlayer1.add_reaction(emoji)
            player1_choice = await bot.wait_for("reaction_add", check=lambda reaction, user: user == player1 and reaction.message.id == botMsgPlayer1.id)

            # Player 2 turn
            botMsgPlayer2 = await player2.send("React with rock (🪨), paper(📄), or scissors(✂️) to show your choice")
            for emoji in emojis:
                await botMsgPlayer2.add_reaction(emoji)
            player2_choice = await bot.wait_for("reaction_add", check=lambda reaction, user: user == player2 and reaction.message.id == botMsgPlayer2.id)

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


bot.run(TOKEN)
