import os
import discord
from discord.ext import commands

class UtilityCmd(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client= client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'>>        commands.utility.py ready!')

    @commands.command(aliases= ["clear"])
    @commands.has_permissions(administrator= True)
    async def cls(self, ctx: commands.Context):
        msg_list=[]
        async for  message in ctx.channel.history(limit= 100):
            if not message.pinned:
                msg_list.append(message)
        await ctx.channel.delete_messages(msg_list)

async def setup(bot: commands.Bot):
    await bot.add_cog(UtilityCmd(bot))