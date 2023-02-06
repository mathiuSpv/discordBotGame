import discord
import asyncio
from discord.ext import commands
from dataScript import playersInfo

intents= discord.Intents.default()
intents.message_content = True
client= commands.Bot(command_prefix='$', intents= intents)
players= playersInfo("datausers")

@client.event
async def on_ready():
    await client.change_presence(activity= discord.Game(name= "Dark Era - Try to play \U000027A1  $start username" ))
    print(f'{client.user} is on!')


@client.command(aliases= ["rg" ,"reg" ,"start"])
async def registration(ctx, *, username= ""):
    
    def check(reaction, user):
        return str(reaction.emoji) in ['👍','👎'] and user == ctx.author
    
    def error_username(*args, **kwargs):
        if username == "":
            return "You need a username"
        elif " " in username:
            return "A username cannot have spaces"
        elif username in players.playersList.values():
            return "A username is already used"
        else:
            return "A username should be only have letters "
    

    if str(ctx.author.id) in players.playersList:
        await ctx.message.add_reaction('\U000026D4')
        await ctx.author.send("You are already registered")
        return
    else:
        if username.isalpha():
            bot_msg= await ctx.author.send(f"{username} is correct?```\n```")
            await bot_msg.add_reaction("👍")
            await bot_msg.add_reaction("👎")
                
            try:
                reaction, user= await client.wait_for("reaction_add", check = check, timeout = 60.0)
            except asyncio.TimeoutError:
                pass
            else:
                print("A")
                if reaction.emoji == '👍':
                    players.new_player(ctx.author.id, username)
                    await ctx.author.send("Welcome to a news adventures")
                
                    await ctx.author.send("Then try again ```$start username```")
        else:
            await ctx.message.add_reaction('\U000026D4')
            await ctx.author.send(error_username())

@client.command()
async def example(ctx):
    user = ctx.message.author
    private_channel = await user.create_dm()
    message_bot = await private_channel.send("React with 👍 or 👎 to this message")
    await message_bot.add_reaction("👍")
    await message_bot.add_reaction("👎")

    def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) in ["👍", "👎"]

    try:
        reaction, user = await client.wait_for("reaction_add", check=check, timeout=60.0)
    except asyncio.TimeoutError:
        await private_channel.send("Timed out.")
    else:
        if str(reaction.emoji) == "👍":
            await private_channel.send("You reacted with 👍")
        else:
            await private_channel.send("You reacted with 👎")

# @client.command()
# async def start(ctx):
#     """First steps of registation function"""

#     await ctx.message.add_reaction('\U0001F47E')
#     await ctx.author.send(
# """```\n
#     **$rg username**\n
#     \n
#     **$player stats**```""")
    
#     def validate_username(message):
#         print(message)
#         return message.startswith("$rg") or message.startswith("$registration") and message.channel == ctx.channel
    
#     try:
#         msg= await client.wait_for('message' , timeout= 30, check= validate_username)
#         print(msg)
#     except asyncio.TimeoutError:
#         await ctx.author.send("Time Out")


@client.command()
async def cls(ctx, *, amount: int): #CLEAR DE CHAT DISCORD CHANNEL.
    await ctx.channel.purge(limit= amount)

@cls.error
async def cls_error(ctx, error):
    """Raise error on $cls command"""
    await ctx.channel.purge(limit= 255)
    
    
    
if __name__ == "__main__":
    with open("token.txt", mode= "r") as filetext:
        token= filetext.readline()
        filetext.close()
    client.run(token)