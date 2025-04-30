from .controller_log_bot import start_log_bot, stop_log_bot


class MainController:
    def start_bot(self):
        start_log_bot()
        
    def stop_bot(self):
        stop_log_bot()
