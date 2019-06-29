import discord
from utilities import utilities

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('Hello world!')
    print('---------')
    await client.change_presence(activity=discord.Game('Watching Chat | $help'))


@client.event
async def on_message(message):
    await utilities.execute_commands(message, client)


# Add Client Token Here
client.run('')