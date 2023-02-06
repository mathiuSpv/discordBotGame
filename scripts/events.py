import discord
from discord.ext import commands, tasks
from itertools import cycle

intents= discord.Intents.default()
intents.message_content = True
client= commands.Bot(command_prefix='$', intents= intents)
status= cycle(["Morning", "Midday","Evening" "Night"])

@client.event
async def on_ready():
    await client.change_presence(activity= discord.Game(name= "$start - DSRoleplay" ))
    await appearance.start()
    print(f'{client.user} is on!')

@tasks.loop(hours= 2, minutes= 30)
async def appearance():
    channel= client.get_channel(1055904937575448587)
    await channel.send(f"time day (game): {next(status)}")


if __name__ == "__main__":
    with open("token.txt", mode= "r") as filetext:
        token= filetext.readline()
        filetext.close()
    client.run(token)