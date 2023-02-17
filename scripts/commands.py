import discord
import asyncio
from discord.ext import commands
from dbscripts import player_db

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
    founders= [395647730112004107, 1000193127073710170]
    if ctx.author.id in founders:
        player_db.delete_db()
        await ctx.channel.send("All data base clear!")

@client.command()
async def newstart(ctx):
    user_id= ctx.author.id
    if not player_db.get_user(user_id):
        text= """ANDVENTURE is a RPG Turn in Discord Game\n
        You have a random enemys, raids and rare loot \n
        First off, you must assing your Stats Points: \n
        **$stats**"""
        embed= discord.Embed(title="__Welcome new Adventurer!__", description= text, color=0x9F00FF)
        player_db.new_player(user_id)
        await ctx.author.send(embed= embed)
        await ctx.message.add_reaction('\U00002714')
    else:
        await ctx.author.send("```You are already registered```")
        await ctx.message.add_reaction('\U0000274C')
        
@client.command()
async def stats(ctx):
    def __move(index: int ,pointers: list, move_down: bool):
        try:
            if move_down:            
                pointers[index]= pointers[index+1]; pointers[index+1]= pointers[index]
                index+= 1 
            else:
                pointers[index]= pointers[index-1]; pointers[index-1]= pointers[index]
                index-= 1
        except IndexError:
            pointers.reverse()
            if index == 5:
                index= 1
            else:
                index= 4
        return index
    
    def __select(index: int,player_stats: dict ):
        pointer_index= {0: 'vig', 1: 'end', 2: 'str', 3: 'dex', 4: 'int'}
        i= pointer_index[index]
        player_stats[i]+= 1
        pass
    
    async def __reactions(message):
        reactions= ['\U0001F53C', '\U0001F53D', '\U0001F199', '\U0001F501', '\U00002705']
        for reaction in reactions:
            await message.add_reaction(reaction)
            
        
    
        
            
    SPACE= '\u200b'
    user= ctx.author
    if player_db.get_user(user.id):
        player_level= player_db.get_level(user.id)
        player_stats= player_db.get_stats(user.id)
        player_stats_new= player_stats
        player_points= player_level['pts']
        pointer_list= ['\U000026AA', '\U000026AB', '\U000026AB', '\U000026AB', '\U000026AB']
        points_updated= {'vig': 0, 'end': 0, 'str': 0, 'dex': 0, 'int': 0}
        
        text= f"""
**LEVEL {player_level['lvl']}
{SPACE*2}{player_level['exp']}/{200}**\n
**POINTS {SPACE*2} >> {SPACE*2} {player_points}**\n\n
"""
        
        text_stats_base= f"""
```
{pointer_list[0]} VIG  >> {SPACE*2} {player_stats['vig']}     {'+'+str(points_updated['vig']) if points_updated['vig']> 0 else ''}     \n
{pointer_list[1]} END  >> {SPACE*2} {player_stats['end']}     {'+'+str(points_updated['end']) if points_updated['end']> 0 else ''}     \n
{pointer_list[2]} STR  >> {SPACE*2} {player_stats['str']}     {'+'+str(points_updated['str']) if points_updated['str']> 0 else ''}     \n
{pointer_list[3]} DEX  >> {SPACE*2} {player_stats['dex']}     {'+'+str(points_updated['dex']) if points_updated['dex']> 0 else ''}     \n
{pointer_list[4]} INT  >> {SPACE*2} {player_stats['int']}     {'+'+str(points_updated['int']) if points_updated['int']> 0 else ''}     
```
"""
        
        text_stats_new= f"""
```
   {player_stats_new['vig']}  \n
   {player_stats_new['end']}   \n
   {player_stats_new['str']}   \n
   {player_stats_new['dex']}   \n
   {player_stats_new['int']}   
```
"""
        
        embed = discord.Embed(title= f"__**{user}**__", description= text, color=0x9F00FF)
        embed.add_field(name= "**STATS**", value= text_stats_base)
        embed.add_field(name= "**NEW STATS**", value= text_stats_new)
        dm_message= await user.send(embed=embed)
        await __reactions(dm_message)






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