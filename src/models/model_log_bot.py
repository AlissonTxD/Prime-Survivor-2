import discord
from tokens import TOKEN
from discord.ext import tasks, commands
INDEX = 0
CHANNEL_ID = 1361092497383755876

def start_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        channel = client.get_channel(CHANNEL_ID)
        await channel.send('Bot is online!')
        if not printer.is_running():
            printer.start()
        
    @tasks.loop(seconds=5.0)
    async def printer():
        global INDEX
        channel = client.get_channel(CHANNEL_ID)
        print(INDEX)
        await channel.send(f'Index: {INDEX}')
        INDEX += 1

    client.run(TOKEN)