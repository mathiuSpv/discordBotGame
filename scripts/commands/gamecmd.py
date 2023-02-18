import discord
import asyncio
import sys
from discord.ext import commands
from os.path import dirname, abspath
_dir= dirname(dirname(abspath(__file__))); sys.path.append(_dir)
from database.player import player as playerdb
from database.levelstatment import level

intents= discord.Intents.default()
intents.message_content = True
client= commands.Bot(command_prefix='$', intents= intents)


@client.event
async def on_ready():
    print(f'        gamecmd.py is on!')

@client.command()
async def newstart(ctx):
    user_id= ctx.author.id
    if not playerdb.get_user(user_id):
        text= """ANDVENTURE is a RPG Turn in Discord Game\n
        You have a random enemys, raids and rare loot \n
        First off, you must assing your Stats Points: \n
        **$stats**"""
        embed= discord.Embed(title="__Welcome new Adventurer!__", description= text, color=0x9F00FF)
        playerdb.new_player(user_id)
        await ctx.author.send(embed= embed)
        await ctx.message.add_reaction('\U00002714')
    else:
        await ctx.author.send("```You are already registered```")
        await ctx.message.add_reaction('\U0000274C')
        
@client.command()
async def stats(ctx):
    SPACE= '\u200b'
    user_id= ctx.author.id
    
    def __view_points_update(stat_type: str):
        points= player_stats_new[stat_type]- player_stats[stat_type]
        return f'+{points}' if points>  0 else '  '    
    
    def __move(move_up: bool):
        if move_up:
            pointers.append(pointers.pop(0))
        else:
            pointers.insert(0, pointers.pop())
    
    def __select(player_points: int):
        if player_points >0:
            player_points-= 1
            pointers_index= {0: 'vig', 1: 'end', 2: 'str', 3: 'dex', 4: 'int'}
            index= pointers_index[pointers.index('\U000026AA')]
            player_stats_new[index]+= 1
        return player_points
        
    def __restart():
        player_points= player_level['pts']
        player_stats_restart= dict(player_stats)
        return player_points, player_stats_restart
    
    async def multiple_reactions(message):
        reactions= ['\U0001F53C', '\U0001F53D', '\U0001F199', '\U0001F501', '\U00002705']
        for reaction in reactions: await message.add_reaction(reaction)
    
    async def edit_bot_message(message):
        __text_level_base= f"**LEVEL {player_level['lvl']}\n  {SPACE*2}{player_level['exp']}/{level.get_exp_needed(player_level['lvl'])}**\n\n"
        __text_stats= f"""```
{pointers[0]} VIG  >>> {SPACE*2}  {player_stats['vig']} {__view_points_update('vig')}\n
{pointers[1]} END  >>> {SPACE*2}  {player_stats['end']} {__view_points_update('end')}\n
{pointers[2]} STR  >>> {SPACE*2}  {player_stats['str']} {__view_points_update('str')}\n
{pointers[3]} DEX  >>> {SPACE*2}  {player_stats['dex']} {__view_points_update('dex')}\n
{pointers[4]} INT  >>> {SPACE*2}  {player_stats['int']} {__view_points_update('int')}
```"""
        __text_stats_new= f"""```
  {player_stats_new['vig']} \n
  {player_stats_new['end']} \n
  {player_stats_new['str']} \n
  {player_stats_new['dex']} \n
  {player_stats_new['int']}```"""
        __text_help=  f"""```\n
  🔼 >> Up Selector
  🔽 >> Down Selector
  🆙 >> Upload Stats
  🔁 >> Restart Points not Confirmed   
  ✅ >> Confirm Points```"""

        embed = discord.Embed(description= __text_level_base, color=0x9F00FF)
        embed.add_field(name= f"**STATS**         **POINTS**  >>  {player_points}", value= __text_stats)
        embed.add_field(name= "**NEW STATS**", value= __text_stats_new)
        embed.add_field(name= "**UTILITY OF REACTIONS**", value= __text_help, inline= False)
        await message.edit(embed= embed)
    
    def check(reaction, user):
        return user == ctx.author
    
            
    if playerdb.get_user(user_id) and not isinstance(ctx.channel, discord.DMChannel):
        player_level= playerdb.get_level(user_id)
        player_stats= playerdb.get_stats(user_id)
        player_stats_new= dict(player_stats)
        player_points= player_level['pts']
        pointers= ['\U000026AA', '\U000026AB', '\U000026AB', '\U000026AB', '\U000026AB']
        
        message= await ctx.channel.send(f'__**{ctx.author}**__  >>  **STATS UPDATE**')
        await multiple_reactions(message)
        stop= False
        while not stop:
            await edit_bot_message(message)
            try:
                reaction, user = await client.wait_for('reaction_add', check= check , timeout= 60)
                await reaction.remove(user)
            except asyncio.TimeoutError:
                await message.delete()
                stop= True
            else:
                match str(reaction):
                    case '\U0001F53C': #is 🔼
                        __move(True)
                    case '\U0001F53D': #is 🔽
                        __move(False)
                    case '\U0001F199': #is 🆙
                        player_points= __select(player_points)
                    case '\U0001F501': #is 🔂
                        player_points, player_stats_new= __restart()
                    case '\U00002705': #is ✅
                        player_level['pts']= player_points
                        playerdb.update_level_info(user_id, player_level)
                        playerdb.update_stats_info(user_id, player_stats_new)
                        await asyncio.sleep(3)
                        await message.delete()
                        stop= True
    elif not playerdb.get_user(user_id):
        await ctx.message.add_reaction('\U0000274C')
        await ctx.author.send("You are not registed\nFirst off, create a account with **$newstart**")
    else:
        await ctx.message.add_reaction('\U0000274C')
        await ctx.author.send("Do not **$stats** on Direct Message\n")
    await asyncio.sleep(3)
    await ctx.message.delete()



if __name__ == "__main__":
    with open("token.txt", mode= "r") as filetext:
        token= filetext.readline()
        filetext.close()
    client.run(token)