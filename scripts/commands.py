import discord
import asyncio
import datetime
from discord.ext import commands
from dataScript import player

intents= discord.Intents.default()
intents.message_content = True
client= commands.Bot(command_prefix='$', intents= intents)
register_status= {}


@client.event
async def on_ready():
    await client.change_presence(activity= discord.Game(name= "Dark Era - Try to play \U000027A1  $start" ))
    print(f'{client.user} is on!')


@client.command(aliases= ["clear"])
async def cls(ctx):
    msg_list=[]
    async for  message in ctx.channel.history(limit= None):
        if not message.pinned:
            msg_list.append(message) 
    await ctx.channel.delete_messages(msg_list)

@client.command()
async def start(ctx, time= 15):
    user_id= ctx.author.id
    register_status[user_id]= True
    await ctx.author.send("Para registrater debes colocar $register 'nombre'!\n (El comando se desabilita al pasar 1 minuto)")
    await asyncio.sleep(time)
    register_status[user_id]= False
    print(register_status)
    if register_status[user_id] == False:
        del register_status[user_id]
        await ctx.author.send("Time out!")

@client.command(aliases= ["rg" ,"reg"])
async def register(ctx):
    async def __error(*args, **kwargs):
        error= False
        if player .get_user(ctx.author.id):
            error= True
            await ctx.author.send("You are already registered")
        if error:
            await ctx.message.add_reaction('\U000026D4')
            return error
        else:
            await ctx.message.add_reaction('\U0001F197')
            return error
    
    user_id= ctx.author.id
    if user_id in register_status:
        if not __error():
            player.new_player(user_id)
            del register_status[user_id]
        await ctx.author.send("Welcome new adventurer")
    else:
        await ctx.author.send("No")


if __name__ == "__main__":
    with open("token.txt", mode= "r") as filetext:
        token= filetext.readline()
        filetext.close()
    client.run(token)