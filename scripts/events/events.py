import discord
import random
from discord.ext import commands, tasks
from itertools import cycle

intents= discord.Intents.default()
intents.message_content = True
client= commands.Bot(command_prefix='$', intents= intents)
status= cycle(["Morning", "Midday", "Night"])

@client.event
async def on_ready():
    await my_task.start()
    print(f'        evernts.py is on!')

@tasks.loop(seconds=1)
async def my_task():
    interval = random.randint(30, 60)
    print(f"This task will run every {interval} seconds")
    my_task.change_interval(seconds= interval)


if __name__ == "__main__":
    with open("token.txt", mode= "r") as filetext:
        token= filetext.readline()
        filetext.close()
    client.run(token)