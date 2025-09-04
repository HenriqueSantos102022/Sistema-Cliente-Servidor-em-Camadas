import os
import json
from datetime import datetime

# Diretório raiz para todos os arquivos de mídia, localizado na raiz do projeto
MEDIA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'media'))

def setup_directories():
    """Cria os diretórios base para o armazenamento de mídia."""
    os.makedirs(os.path.join(MEDIA_ROOT, 'incoming'), exist_ok=True)
    os.makedirs(os.path.join(MEDIA_ROOT, 'videos'), exist_ok=True)
    os.makedirs(os.path.join(MEDIA_ROOT, 'trash'), exist_ok=True)
    print(f"Diretórios de mídia configurados em: {MEDIA_ROOT}")

def create_video_storage_path(video_uuid, original_ext, filter_name, processed_ext=None):
    """
    Cria a estrutura de pastas para um novo vídeo e retorna os caminhos.
    Permite uma extensão de arquivo diferente para o vídeo processado.
    """
    # Se nenhuma extensão processada for fornecida, usa a original
    if processed_ext is None:
        processed_ext = original_ext

    now = datetime.now()
    date_path = now.strftime('%Y/%m/%d')
    
    base_path = os.path.join(MEDIA_ROOT, 'videos', date_path, video_uuid)
    
    # Cria os subdiretórios
    original_dir = os.path.join(base_path, 'original')
    processed_dir = os.path.join(base_path, 'processed', filter_name)
    thumbs_dir = os.path.join(base_path, 'thumbs')
    
    for d in [original_dir, processed_dir, thumbs_dir]:
        os.makedirs(d, exist_ok=True)
        
    # Define os caminhos completos dos arquivos
    paths = {
        'original': os.path.join(original_dir, f'video.{original_ext}'),
        'processed': os.path.join(processed_dir, f'video.{processed_ext}'), # <-- USA A NOVA EXTENSÃO
        'thumbnail': os.path.join(thumbs_dir, 'frame_0001.jpg'),
        'preview': os.path.join(base_path, 'preview.gif'),
        'meta': os.path.join(base_path, 'meta.json')
    }
    
    return paths

def save_meta_json(path, data):
    """Salva um dicionário de metadados em um arquivo meta.json."""
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar meta.json: {e}")