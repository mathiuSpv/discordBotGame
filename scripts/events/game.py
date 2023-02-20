import discord
import random
from discord.ext import commands, tasks
from itertools import cycle


status= cycle(["Morning", "Midday", "Night"])


class EventGm(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client= client
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.loop_enemies.start()
        print(f'>>          evernts.py is on!')
    
    @tasks.loop(seconds=1)
    async def loop_enemies(self):
        interval= random.randint(20,40)
        self.loop_enemies.change_interval(minutes=interval)
