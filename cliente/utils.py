import os
import subprocess
import sys

def play_video_from_url(video_url):
    """
    Abre uma URL de vídeo no player padrão do sistema.
    """
    try:
        if sys.platform == "win32":
            os.startfile(video_url)
        elif sys.platform == "darwin": # macOS
            subprocess.Popen(["open", video_url])
        else: # linux
            subprocess.Popen(["xdg-open", video_url])
    except Exception as e:
        print(f"Não foi possível abrir o player de vídeo: {e}")
        # Poderia mostrar um popup de erro aqui