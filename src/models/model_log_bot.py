import re

import discord
from discord.ext import tasks
from PyQt5.QtCore import QObject, pyqtSignal
from paddleocr import PaddleOCR

from tokens import TOKEN
from src.models.model_image_generator import ImageGerenatorModel


class LogBotModel(QObject):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.EVENTCOUNTER = 1
        self.CHANNEL_ID = 1352626736491270227
        self.client = None
        self.printer = None
        self.ocr = PaddleOCR(use_angle_cls=True, lang="en")
        self.generator = ImageGerenatorModel()
        self.events = []

    def run(self):
        intents = discord.Intents.default()
        intents.message_content = True

        self.client = discord.Client(intents=intents)

        @self.client.event
        async def on_ready():
            print(f"Login as {self.client.user}")
            channel = self.client.get_channel(self.CHANNEL_ID)
            await channel.send("Bot is online! activated by: omigadortxd")

            if not self.printer.is_running():
                self.printer.start()

        @tasks.loop(seconds=5.0)
        async def printer():
            channel = self.client.get_channel(self.CHANNEL_ID)
            reset_counter = 0
            self.generator.generate_image()
            text = self.__read_img_ocr("temp/subimage.png")
            print(text)
            is_new_event = self.__validate_log(text)
            if is_new_event:
                message = text
                if self.EVENTCOUNTER > 5:
                    message = f"@everyone {text}"
                    self.EVENTCOUNTER = 1
                elif self.EVENTCOUNTER >= 3:
                    message = f"@here {text}"
                await channel.send(f"{message}", file=discord.File("temp/subimage.png"))
                self.EVENTCOUNTER += 1
                reset_counter -= 120
            reset_counter += 1
            if reset_counter >= 240:
                self.EVENTCOUNTER = 1
                reset_counter = 0

        self.printer = printer
        try:
            self.client.run(TOKEN)
        except Exception as e:
            print(f"Error starting the bot: {e}")
        finally:
            self.finished.emit()

    def stop(self):
        if self.client:
            self.client.close()

    def __read_img_ocr(self, path):
        try:
            img_path = path
            result = self.ocr.ocr(img_path, cls=True)
            palavras = []
            for line in result:
                for word_info in line:
                    text = word_info[1][0]
                    palavras.append(text)
            texto_final = " ".join(palavras)
            return texto_final
        except Exception as e:
            print(f"Error reading image: {e}")

    def __validate_log(self, text):
        try:
            match = re.match(r"Day (\d+), (\d{2}:\d{2}:\d{2}): (.+)", text)
            if match:
                dia = match.group(1)
                hora = match.group(2)
                mensagem = match.group(3)

                if (
                    "Your" in mensagem
                    and ("destroyed" in mensagem or "killed" in mensagem)
                    and "Baby" not in mensagem
                ):
                    evento_id = f"{dia} {hora}"

                    if evento_id not in self.events:
                        self.events.append(evento_id)
                        print(f"New Event: {text}")
                        return True
                    else:
                        print(f"event already registered: {text}")
                        return False
                else:
                    print(f"event ignored: {text}")
                    return False
            else:
                print(f"invalid log format: {text}")
                return False
        except Exception as e:
            print("Error validating log:", e)
            return False
