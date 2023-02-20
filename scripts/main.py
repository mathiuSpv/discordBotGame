import discord
import os
from discord.ext import commands

class InitBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix= '$',intents= discord.Intents.all())
        self.initial_extensions= list()
        
        folder_notrd= ['database','test.py','main.py']
        for folder in os.listdir('scripts'):
            if folder not in folder_notrd:
                for filename in os.listdir(f'scripts/{folder}'):
                    if filename.endswith('.py'):
                        cog= f'scripts.{folder}.{filename[::-3]}'
                        self.initial_extensions.append(cog)
                    
                    
    async def setup_hook(self):
        try:
            for extension in self.extensions:
                await self.load_extension(extension)
                print(extension)
        except Exception as exc:
            print(exc)
        return await super().setup_hook()
    
    async def on_ready(self):
        print("on")
                    
                    
client= InitBot()   
