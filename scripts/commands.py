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
    print(f"{ctx.author} try $cls but raise error")
    await ctx.channel.purge(limit= 255)
    
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
#@client.command estoy haciendo el que va a mandar la imagen


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")#Forma de poner que busque los archivos que terminan con 3 caracteres

if __name__ == "__main__":
    with open("token.txt", mode= "r") as filetext:
        token= filetext.readline()
        filetext.close()
    client.run(token)