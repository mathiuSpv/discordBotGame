import discord
import os
from discord.ext import commands

class runBot(commands.Bot):
    def __init__(self) -> None:
        intents= discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix= '$',intents= intents) #Might be useful user intents= discord.Intents.all()
        self.initial_extensions= list()
        
        folder_notrd= ['database','test.py','main.py']
        for folder in os.listdir('scripts'):
            if folder not in folder_notrd:
                for filename in os.listdir(f'scripts/{folder}'):
                    if filename.endswith('.py'):
                        cog= f'{folder}.{filename[:-3]}'
                        self.initial_extensions.append(cog)
                    
    async def setup_hook(self) -> None:
        try:
            for extension in self.initial_extensions:
                await self.load_extension(extension)
                print(f'>>      {extension} is loading...')
        except Exception as exc:
            print(f'>>      {exc} Raise error in {extension}')
    
    async def on_ready(self) -> None:
        await client.change_presence(activity= discord.Game(name= "PLAY RPG \U000027A1  $newstart" ))

if __name__ == '__main__':
    client= runBot()
    TOKEN= open('token.txt', mode='r').readline()
    client.run(TOKEN)
