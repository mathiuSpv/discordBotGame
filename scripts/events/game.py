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
        print(f'>>      events.Game ready!')
        await self.loop_enemies.start()
    
    @tasks.loop(seconds=1)
    async def loop_enemies(self):
        
        async def send_embed(channel: discord.TextChannel):
            embed= discord.Embed(title="**NEW ENEMY APPEARED**")
            embed.set_image(url='https://www.soyvisual.org/sites/default/files/styles/twitter_card/public/images/photos/her_0004.jpg?itok=j85_yxCg')
            await channel.send(embed=embed)
        
        for guild in self.client.guilds:
            category = discord.utils.get(guild.categories, name="rpg")
            channel = discord.utils.get(category.channel, name="enemies-spawn")
            if channel is not None:
                interval= random.randint(20,40)
                self.loop_enemies.change_interval(minutes=interval)
                await send_embed(channel)
                
    
        
        
async def setup(bot: commands.Bot):
    await bot.add_cog(EventGm(bot))