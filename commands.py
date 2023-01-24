import discord

intents = discord.Intents.default()
intents.message_content = True

class discordBot(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        
    async def on_message(self, message):
        if message.author == self.user:
            return
        if "$start" == message.content.lower():
            await message.channel.send("Funcaaaaaaaa")