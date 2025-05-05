from pynput import keyboard
import threading
import re

class HotkeysModel:
    def __init__(self):
        self.listener = None

    def set_hotkeys(self, hotkeys_and_callbacks: dict):
        self.hotkeys_and_callbacks = hotkeys_and_callbacks
        try:
            hotkey_map = {}
            for key_str, callback in self.hotkeys_and_callbacks.items():
                if key_str.strip():
                    valid_key = self._format_key(key_str)
                    if valid_key:
                        hotkey_map[valid_key] = callback

            if not hotkey_map:
                print("[AVISO] Nenhuma hotkey válida para ativar.")
                return

            self.listener = keyboard.GlobalHotKeys(hotkey_map)
            threading.Thread(target=self.listener.run, daemon=True).start()
            print("Hotkeys ativas:", list(hotkey_map.keys()))
        except Exception as e:
            print(f"[ERRO] ao configurar hotkeys: {e}")

    def stop(self):
        if self.listener:
            self.listener.stop()
            self.listener = None

    def _format_key(self, key: str) -> str:
        """
        Converte 'Ctrl+Alt+F1' → '<ctrl>+<alt>+f1'
        Converte 'F1' → '<f1>'
        Converte 'c' → 'c'
        """
        key = key.strip().lower()
        parts = re.split(r'\s*\+\s*', key)

        converted = []
        for part in parts:
            part = part.strip()

            if part in ['ctrl', 'alt', 'shift', 'cmd', 'win']:
                converted.append(f"<{part}>")
            elif re.match(r'^f\d{1,2}$', part):  # F1 até F12
                converted.append(f"<{part}>")
            elif len(part) == 1 and part.isalnum():  # letras e números
                converted.append(part)
            else:
                print(f"[AVISO] Tecla desconhecida ou inválida: {part}")
                return None  # Invalida a sequência

        return '+'.join(converted)
