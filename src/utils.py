import os
import sys


def resource_path(relative_path: str) -> str:
    """
    Retorna o caminho absoluto para um recurso, compatível tanto com desenvolvimento
    local quanto com a execução de um aplicativo empacotado pelo PyInstaller.

    Quando o aplicativo é empacotado pelo PyInstaller, os arquivos temporários são
    armazenados em uma pasta temporária e o caminho base é armazenado na variável
    _MEIPASS. Esta função tenta obter o caminho base dessa variável.

    Se a variável _MEIPASS não estiver presente (como no caso de um ambiente de
    desenvolvimento local), o caminho base será definido como o diretório atual.

    Outputs:
    String:
    -O caminho absoluto para o recurso.
    """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # No ambiente de desenvolvimento, usa o diretório atual como caminho base
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
