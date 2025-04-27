from PyQt5.QtCore import QThread
from src.models.model_log_bot import LogBotModel

class WorkerThread(QThread):
    def __init__(self, log_bot_model):
        super().__init__()
        self.log_bot_model = log_bot_model

    def run(self):
        self.log_bot_model.run()  # Roda o método `run()` de forma simples

# Variáveis globais para gerenciar a instância do bot e a thread
thread = None
log_bot = None

def start_log_bot():
    global thread, log_bot
    log_bot = LogBotModel()  # Cria a instância do modelo
    thread = WorkerThread(log_bot)  # Cria o WorkerThread com o modelo

    # Conectar o sinal de término à função bot_terminou
    log_bot.finished.connect(bot_terminou)

    thread.start()  # Inicia a thread

def stop_log_bot():
    if log_bot:
        log_bot.stop()  # Chama a função para parar o bot de forma segura
    if thread:
        thread.quit()  # Finaliza a thread de forma segura
        thread.wait()  # Aguarda a thread ser finalizada antes de destruí-la

def bot_terminou():
    from src.views.view_main import MainWindow
    view = MainWindow()
    global thread, log_bot
    thread = None  # Limpa a referência da thread
    log_bot = None  # Limpa a referência do bot
    print("Bot terminou!")
    view.btn_iniciar_log_bot.setEnabled(True)  # Reabilita o botão no UI
    # Esta função será chamada quando o bot terminar
