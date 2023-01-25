import discord
import asyncio
import os
from discord.ext import commands

intents= discord.Intents.default()
intents.message_content = True
client= commands.Bot(command_prefix='$', intents= intents)

@client.event
async def on_ready():
    print('Bot On!')



@client.command()
async def start(ctx):
    await ctx.author.send("""ESTAMOS PROBANDO PORFAVOR REACCIONAR 👍""")
    check= lambda reaction: str(reaction.emoji) == '👍'

    try:
        reaction= await client.wait_for('reaction_add', timeout= 60, check= check)
        print(reaction)
    except asyncio.TimeoutError:
        await ctx.author.send("DALE FLACO METELE PILA")
    else:
        await ctx.author.send("NOS VIMOS GILES COCNHETUMARE")
        


@client.command()
#CLEAR DE CHAT DISCORD CHANNEL. DEFAULT 255
async def cls(ctx, *, amount= 255):
    await ctx.channel.purge(limit= amount)

    
    
    
if __name__ == "__main__":
    with open("token.txt", mode= "r") as filetext:
        token= filetext.readline()
        filetext.close()
    client.run(token)