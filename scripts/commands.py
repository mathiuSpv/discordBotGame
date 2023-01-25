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
async def start(ctx): #FOR BEGINERS REGISTRATION
    list= ['\U0001F47E',]
    await ctx.message.add_reaction('\U0001F47E')
    msg = await ctx.author.send("""ESTAMOS PROBANDO PORFAVOR REACCIONAR 👍""")
    await msg.add_reaction('\U0001F47E')
    check= lambda m: m.content == "ok" and m.channel ==  msg.channel
    try:
        msg= await client.wait_for('message' , timeout= 60, check= check)
        await ctx.author.send(f"Tamos chelo {ctx.author}") 
    except asyncio.TimeoutError:
        await ctx.author.send("DALE FLACO METELE PILA")
        


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