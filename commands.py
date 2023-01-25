import discord
from discord.ext import commands
 

intents= discord.Intents.default()
intents.message_content = True
client= commands.Bot(command_prefix='$', intents= intents)

@client.event
async def on_ready():
    print('Bot On!')
    
@client.command()
async def start(ctx):
    await ctx.author.send("""
                          WELCOME TO THE GAME OF THE YEAR\
                              TWITCH SUPPORT IS A TRASH!""")