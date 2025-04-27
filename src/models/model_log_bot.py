import discord
from discord.ext import tasks
from PyQt5.QtCore import QObject, pyqtSignal

from tokens import TOKEN


class LogBotModel(QObject):
    finished = pyqtSignal()  # Sinal para quando o bot terminar

    def __init__(self):
        super().__init__()
        self.INDEX = 0
        self.CHANNEL_ID = 1361092497383755876
        self.client = None
        self.printer = None

    def run(self):
        intents = discord.Intents.default()
        intents.message_content = True

        self.client = discord.Client(intents=intents)

        @self.client.event
        async def on_ready():
            print(f"We have logged in as {self.client.user}")
            channel = self.client.get_channel(self.CHANNEL_ID)
            await channel.send("Bot is online!")

            if not self.printer.is_running():
                self.printer.start()

        @self.client.event
        async def on_disconnect():
            print("Bot disconnected!")
            self.finished.emit()  # Emite o sinal quando o bot desconectar (terminar)

        @tasks.loop(seconds=1.0)
        async def printer():
            channel = self.client.get_channel(self.CHANNEL_ID)
            print(self.INDEX)
            await channel.send(f"Index: {self.INDEX}")
            self.INDEX += 1

            if self.INDEX > 10:
                await channel.send("Bot is shutting down!")
                await self.client.close()

        self.printer = printer
        self.client.run(TOKEN)  # Aqui chamamos o loop do client diretamente

    def stop(self):
        if self.client:
            self.client.close()  # Fechar o client de forma segura
