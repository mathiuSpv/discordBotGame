import discord
import asyncio
import os
from discord.ext import commands

intents= discord.Intents.default()
intents.message_content = True
client= commands.Bot(command_prefix='$', intents= intents)


@client.event
async def on_ready():
    await client.change_presence(activity= discord.Game(name= "$start - DSRoleplay" ))
    print(f'{client.user} is on!')


@client.command()
async def start(ctx):
    """First steps of registation function"""

    await ctx.message.add_reaction('\U0001F47E')
    msg = await ctx.author.send(
"""```Para poder registrarte escribeme:\n
    **$rg username**\n
Registrado, debes asignar tus puntos:\n
    **$player stats**```""")
    
    def check(message):
        return "$rg" in message.content and message.channel == msg.channel

    try:
        msg = await client.wait_for('message' , timeout= 30, check= check)
        if msg: await ctx.author.send("Well done!")
    except asyncio.TimeoutError:
        await ctx.author.send("Time Out")
    else:
        pass

@client.command(aliases= ["rg"])
@start.after_invoke
async def registration(ctx, *, arg= ""):
    if arg.isalpha():
        await ctx.author.send("Registro completado, asigna tus puntos y empeza a jugar")
    else:
        await ctx.author.send("El username solo deben ser letras")
        
@registration.error
async def registation_errors(ctx, error):
    print(error)


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