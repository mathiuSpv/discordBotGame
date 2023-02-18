import discord
from discord.ext import commands

intents= discord.Intents.default()
intents.message_content = True
client= commands.Bot(command_prefix='$', intents= intents)


@client.event
async def on_ready():
    await client.change_presence(activity= discord.Game(name= "Andventure - PLAY RPG \U000027A1  $newstart" ))
    print(f'{client.user} is on!')

@client.command(aliases= ["clear"])
@commands.has_permissions(administrator= True)
async def cls(ctx):
    msg_list=[]
    async for  message in ctx.channel.history(limit= 100):
        if not message.pinned:
            msg_list.append(message) 
    await ctx.channel.delete_messages(msg_list)


if __name__ == "__main__":
    with open("token.txt", mode= "r") as filetext:
        token= filetext.readline()
        filetext.close()
    client.run(token)



# await asyncio.sleep(time)
#     register_status[user_id]= False
#     if register_status[user_id] == False:
#         del register_status[user_id]
#         await ctx.author.send("Time out! Try again $newstart for register!")