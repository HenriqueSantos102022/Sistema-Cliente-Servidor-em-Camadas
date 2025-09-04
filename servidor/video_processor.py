import cv2
import os
from PIL import Image
import subprocess # <--- Importe o módulo subprocess

def get_video_metadata(video_path):
    """Extrai metadados de um vídeo usando OpenCV."""
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return {}
            
        metadata = {
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        }
        metadata['duration_sec'] = metadata['frame_count'] / metadata['fps'] if metadata['fps'] > 0 else 0
        cap.release()
        return metadata
    except Exception as e:
        print(f"Erro ao extrair metadados: {e}")
        return {}

def generate_thumbnail(video_path, output_path):
    """Gera um thumbnail (primeiro frame) de um vídeo."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return False
    
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(output_path, frame)
    
    cap.release()
    return ret

def generate_preview_gif(video_path, output_path, num_frames=30, resize_factor=0.3):
    """Gera um GIF animado de preview."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return False

    frames = []
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # Seleciona frames espaçados uniformemente
    frame_indices = [int(i * total_frames / num_frames) for i in range(num_frames)]

    for i in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            # Converte de BGR (OpenCV) para RGB (Pillow)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Redimensiona para o GIF ser menor
            h, w, _ = frame_rgb.shape
            new_size = (int(w * resize_factor), int(h * resize_factor))
            img = Image.fromarray(frame_rgb).resize(new_size, Image.Resampling.LANCZOS)
            frames.append(img)
    
    cap.release()

    if frames:
        frames[0].save(output_path, save_all=True, append_images=frames[1:], optimize=False, duration=100, loop=0)
        return True
    return False


def apply_filter(input_path, output_path, filter_name):
    """Aplica um filtro e salva o resultado no formato WebM com codec VP8."""
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Erro: Não foi possível abrir o vídeo de entrada.")
        return False

    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # fps = cap.get(cv2.CAP_PROP_FPS)

    # # --- INÍCIO DA CORREÇÃO ---
    # # Define o FourCC para o codec VP8, compatível com o contêiner WebM.
    # fourcc = cv2.VideoWriter_fourcc(*'VP80')
    
    # # Inicializa o VideoWriter
    # out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # --- OTIMIZAÇÃO: DEFINIR UMA RESOLUÇÃO MÁXIMA ---
    target_width = 1280  # Alvo: 720p de largura
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Se o vídeo for maior que o alvo, calcula as novas dimensões mantendo a proporção
    if original_width > target_width:
        aspect_ratio = original_height / original_width
        height = int(target_width * aspect_ratio)
        width = target_width
    else:
        width = original_width
        height = original_height

    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'VP80')
    # fourcc = cv2.VideoWriter_fourcc(*'VP90') # Usando VP9 como sugestão
    
    # Usa as novas dimensões (width, height) para inicializar o VideoWriter
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Verifica se o VideoWriter foi inicializado com sucesso.
    # Se o codec VP8 não estiver disponível, isOpened() retornará False.
    if not out.isOpened():
        print("ERRO CRÍTICO: Não foi possível inicializar o VideoWriter com o codec VP8.")
        print("Verifique a instalação do OpenCV e do backend FFmpeg.")
        cap.release()
        return False
    # --- FIM DA CORREÇÃO ---

    print(f"VideoWriter inicializado com sucesso para '{output_path}' usando o codec VP8.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Redimensiona o frame ANTES de aplicar o filtro
        if width != original_width:
            frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

        # ... (lógica dos filtros permanece a mesma) ...
        processed_frame = None
        if filter_name == 'grayscale':
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            processed_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
        elif filter_name == 'pixelize':
            h, w, _ = frame.shape
            pixel_size = 16
            small = cv2.resize(frame, (w // pixel_size, h // pixel_size), interpolation=cv2.INTER_LINEAR)
            processed_frame = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
        elif filter_name == 'edges':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            processed_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        else:
            processed_frame = frame

        out.write(processed_frame)

    print("Processamento de frames concluído. Finalizando o arquivo de vídeo...")
    cap.release()
    out.release()
    print("Arquivo de vídeo salvo com sucesso.")
    return True