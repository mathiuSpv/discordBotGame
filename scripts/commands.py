import discord
import asyncio
import os
from discord.ext import commands

intents= discord.Intents.default()
intents.message_content = True
client= commands.Bot(command_prefix='$', intents= intents)

def read_data():
    players_system= dict()
    with open("./datauser.csv", mode= 'r') as file:
        players_list= file.readlines()
    for user_id, user_name in players_list:
        players_system[f'{user_id}']= user_name
    return players_system

players= read_data()
client.change_presence(activity= discord.Game(name= "$start - DSRoleplay" ))

@client.event
async def on_ready():
    print(f'{client.user} is on!')


@client.command(aliases= ["rg" ,"reg" ,"start"])
async def registration(ctx, *, username= ""):
    
    async def regist_user(user_id: str, user_name: str):
        with open("./datausers.csv", mode= "a") as file:
            file.write(f"{user_id};{user_name}\n")
            file.close()
        players[f'{user_id}']= user_name
    
    async def error_username(username: str):
        if username == "":
            await ctx.author.send("You need a username")
        elif " " in username:
            await ctx.author.send("A username cannot have spaces")
        elif username in players.values():
            await ctx.author.send("A username is already used")
        else:
            await ctx.author.send("A username should be only have letters ")
            
    
    if ctx.author.id in players:
        await ctx.author.send("You are already register!")
        return
    else:
        if username.isalpha():
            await ctx.message.add_reaction('\U0001F44D')
            await regist_user(ctx.author.id, username , "None")
            await ctx.author.send("Welcome to a news adventures")
        else:
            await ctx.message.add_reaction('\U0001F44E')
            await error_username(username)
            await ctx.author.send("Remember you can only user Letter as a user name")

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