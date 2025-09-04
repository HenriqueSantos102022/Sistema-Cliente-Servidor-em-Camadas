import requests
import os

# Configure o endereço do servidor. Use o IP da máquina do servidor se estiver em outra máquina.
SERVER_URL = "http://192.168.1.28:5000"

def upload_video(file_path, filter_name, progress_callback):
    """Envia um vídeo para o servidor e reporta o progresso."""
    try:
        url = f"{SERVER_URL}/upload"
        with open(file_path, 'rb') as f:
            files = {'video': (os.path.basename(file_path), f)}
            data = {'filter': filter_name}
            
            # O upload é feito em um único POST. Para um progresso real, seria
            # necessário streaming ou uma biblioteca como requests-toolbelt.
            # Aqui, simulamos o progresso antes e depois da chamada.
            progress_callback(10) # Início
            response = requests.post(url, files=files, data=data, timeout=300) # Timeout de 5 mins
            progress_callback(100) # Fim
            
        response.raise_for_status()  # Lança exceção para respostas de erro (4xx ou 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão com o servidor: {e}")
        return {'error': f"Não foi possível conectar ao servidor: {e}"}

def get_video_history():
    """Busca o histórico de vídeos do servidor."""
    try:
        url = f"{SERVER_URL}/videos"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar histórico: {e}")
        return []