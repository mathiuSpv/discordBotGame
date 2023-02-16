import discord
from discord.ext import commands
from dataScript import player

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
    async for  message in ctx.channel.history(limit= 255):
        if not message.pinned:
            msg_list.append(message) 
    await ctx.channel.delete_messages(msg_list)
    
@client.command()
async def deletedb(ctx):
    founders= [395647730112004107] 
    if ctx.author.id in founders:
        player.delete_db()
        await ctx.channel.send("All data base clear!")

@client.command()
async def newstart(ctx):
    def __error(*args, **kwargs):
        if player.get_user(user_id):
            return True
        return False
    
    user_id= ctx.author.id
    if not __error(user_id):
        text= """ANDVENTURE is a RPG Turn in Discord Game\n
        You have a random enemys, raids and rare loot \n
        First off, you must assing your Stats Points: \n
        **$stats**"""
        embed= discord.Embed(title="__Welcome new Adventurer!__", color=0x9F00FF ,description= text)
        player.new_player(user_id)
        await ctx.author.send(embed= embed)
    else:
        await ctx.author.send("```You are already registered```")
        await ctx.message.add_reaction('\U000026D4')
        
@client.command()
async def mycommand(ctx):
    embed = discord.Embed(title="Título del Embed", description="Descripción del Embed", color=0x9F00FF)
    await ctx.send(embed=embed)


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