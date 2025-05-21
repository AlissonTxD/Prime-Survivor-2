import re
import asyncio

import discord
from discord.ext import tasks
import pywhatkit

from src.models.entities.macrobase import MacroBase


class LogBotModel(MacroBase):
    def __init__(self, image_generator_model, ocr_model=None, config=None, testmode=False):
        super().__init__()
        self.ocr = ocr_model
        self.generator = image_generator_model
        self.testmode = testmode
        self.load_config(config)
        self.event_counter = 0
        self.reset_counter = 0
        self.client = None
        self.printer = None
        self.loop = None
        self.events = []
        

    def run(self):
        self.focus_in_window("ArkAscended")
        intents = discord.Intents.default()
        intents.message_content = True

        self.client = discord.Client(intents=intents)

        @self.client.event
        async def on_ready():
            print(f"Login as {self.client.user}")
            channel = self.client.get_channel(self.CHANNEL_ID)
            try:
                await channel.send("Log Bot Started!")
            except Exception as e:
                self.error.emit(f"Bot Sem Acesso ao Canal: {e}")
                self.finished.emit()
                return
            if not self.printer.is_running():
                self.printer.start()

        @tasks.loop(seconds=5.0)
        async def printer():
            loops_for_minute = 60 / 5  # 12
            channel = self.client.get_channel(self.CHANNEL_ID)
            self.generator.generate_image()
            text = self.__read_img_ocr("temp/subimage.png")
            if text == None or not text.strip():
                text = "No text detected"
            print(text)
            is_new_event = self.__validate_log(text)

            if self.testmode:
                is_new_event = True
                text = f"Test Event: {text}"

            if is_new_event:
                message = text
                if self.event_counter > 5:
                    message = f"@everyone {text}"
                    self.event_counter = 0
                    if self.GROUP_ID != "none":
                        pywhatkit.sendwhats_image(
                            self.GROUP_ID, "temp/subimage.png", text, 20, True, 3
                        )
                    self.focus_in_window("ArkAscended")
                elif self.event_counter >= 3:
                    message = f"@here {text}"
                await channel.send(f"{message}", file=discord.File("temp/subimage.png"))
                self.event_counter += 1
                self.reset_counter = loops_for_minute * 10

            if self.reset_counter >= (loops_for_minute * 20):
                self.event_counter = 0
                self.reset_counter = 0

            self.reset_counter += 1

        self.printer = printer

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        try:
            self.loop.run_until_complete(self.client.start(self.TOKEN))
        except Exception as e:
            print(f"Error starting the bot: {e}")
            self.error.emit(f"Erro Iniciando o Log Bot: {e}")
        finally:
            try:
                if self.client and self.client.is_closed() is False:
                    self.loop.run_until_complete(self.client.close())
                self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            except Exception as e:
                print(f"Error during shutdown: {e}")
            finally:
                self.loop.close()
                self.finished.emit()

    def stop(self):
        if self.client and self.loop and not self.loop.is_closed():
            try:
                asyncio.run_coroutine_threadsafe(self.client.close(), self.loop)
            except Exception as e:
                print(f"[Erro ao tentar fechar o bot]: {e}")
        else:
            print("[INFO] Loop já está fechado ou não existe.")

    def __read_img_ocr(self, path):
        try:
            result = self.ocr.ocr(path, cls=True)
            words = []
            for line in result:
                for word_info in line:
                    text = word_info[1][0]
                    words.append(text)
            final_text = " ".join(words)
            return final_text
        except Exception as e:
            print(f"Error reading image: {e}")

    def __validate_log(self, text):
        try:
            match = re.match(r"Day (\d+), (\d{2}:\d{2}:\d{2}): (.+)", text)
            if match:
                day = match.group(1)
                hour = match.group(2)
                message = match.group(3)

                ignore_words = ["Baby", "decay", "Karkinos"]

                if (
                    "Your" in message
                    and ("destroyed" in message or "killed" in message)
                    and not any(word in message for word in ignore_words)
                ):
                    event_id = f"{day} {hour}"
                    if event_id not in self.events:
                        self.events.append(event_id)
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

    def load_config(self, config):
        try:
            self.TOKEN = config["token"]
            self.CHANNEL_ID = config["channel_id"]
            self.GROUP_ID = config["whatsapp"]
        except KeyError as e:
            self.error.emit(f"Erro ao carregar configuração: {e}")
        