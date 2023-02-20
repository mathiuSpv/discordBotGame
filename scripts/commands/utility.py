import os
from discord.ext import commands

class UtilityCmd(commands.Cog):
    def __init__(self, bot):
        self.client= bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'        commands.utility.py is loaded!')

    @commands.command(aliases= ["clear"])
    @commands.has_permissions(administrator= True)
    async def cls(self, ctx):
        msg_list=[]
        async for  message in ctx.channel.history(limit= 100):
            if not message.pinned:
                msg_list.append(message)
        await ctx.channel.delete_messages(msg_list)

def setup(bot):
    bot.add_cogs(UtilityCmd(bot))