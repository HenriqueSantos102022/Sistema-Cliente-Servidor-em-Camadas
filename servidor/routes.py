import os
import shutil
from flask import Blueprint, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename

# Importa funções dos outros módulos do servidor
from . import database as db
from . import storage
from . import utils
from . import video_processor

# Cria um Blueprint para organizar as rotas
bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    """Renderiza a página HTML principal que lista os vídeos."""
    videos_from_db = db.get_all_videos()
    
    # --- INÍCIO DA CORREÇÃO ---
    # Prepara os dados para o template, convertendo os caminhos do OS para URLs válidas.
    # Usar os.sep garante que funcione tanto em Windows ('\') quanto em Linux/Mac ('/').
    for video in videos_from_db:
        # Cria chaves novas no dicionário para não alterar os dados originais do DB
        video['url_original'] = video['path_original'].replace(os.sep, '/')
        video['url_processed'] = video['path_processed'].replace(os.sep, '/')

        # Gera o caminho da thumbnail de forma robusta e o converte para URL
        thumb_dir = os.path.dirname(os.path.dirname(video['path_original']))
        thumb_path_os = os.path.join(thumb_dir, 'thumbs', 'frame_0001.jpg')
        video['url_thumbnail'] = thumb_path_os.replace(os.sep, '/')
    # --- FIM DA CORREÇÃO ---

    # Envia a lista de vídeos já processada para o template
    return render_template('index.html', videos=videos_from_db)

@bp.route('/upload', methods=['POST'])
def upload_video():
    """Rota para receber o upload de um vídeo do cliente."""
    if 'video' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['video']
    filter_name = request.form.get('filter')

    if file.filename == '' or not filter_name:
        return jsonify({'error': 'Nome de arquivo ou filtro inválido'}), 400
        
    original_filename = secure_filename(file.filename)
    original_name, original_ext = os.path.splitext(original_filename)
    original_ext = original_ext.lstrip('.')

    # 1. Salva o arquivo temporariamente
    incoming_path = os.path.join(storage.MEDIA_ROOT, 'incoming', original_filename)
    file.save(incoming_path)

    try:
        # 2. Gera UUID e timestamp
        video_uuid = utils.generate_uuid()
        timestamp = utils.get_current_timestamp()

        # 3. Cria a estrutura de pastas, especificando a extensão '.webm' para o arquivo processado
        output_extension = 'webm'
        paths = storage.create_video_storage_path(video_uuid, original_ext, filter_name, processed_ext=output_extension)

        # 4. Move o arquivo original para o destino final
        shutil.move(incoming_path, paths['original'])
        
        # 5. Extrai metadados do vídeo
        video_meta = video_processor.get_video_metadata(paths['original'])
        file_size = os.path.getsize(paths['original'])

        # 6. Aplica o filtro
        print(f"Aplicando filtro '{filter_name}' para gerar um arquivo .webm...")
        
        # A função apply_filter agora salva em paths['processed'], que já tem a extensão .webm
        success = video_processor.apply_filter(paths['original'], paths['processed'], filter_name)
        
        # A verificação de sucesso agora é confiável
        if not success:
            raise Exception("Falha ao processar e salvar o vídeo. O codec VP8 pode não estar disponível.")
        
        print("Filtro aplicado e arquivo .webm salvo com sucesso.")

        # 7. Gera thumbnail e preview
        video_processor.generate_thumbnail(paths['original'], paths['thumbnail'])
        video_processor.generate_preview_gif(paths['original'], paths['preview'])
        
        # 8. Prepara metadados para o banco de dados
        db_metadata = {
            'id': video_uuid,
            'original_name': original_name,
            'original_ext': original_ext,
            'mime_type': file.mimetype,
            'size_bytes': file_size,
            'duration_sec': video_meta.get('duration_sec'),
            'fps': video_meta.get('fps'),
            'width': video_meta.get('width'),
            'height': video_meta.get('height'),
            'filter': filter_name,
            'created_at': timestamp,
            'path_original': os.path.relpath(paths['original'], storage.MEDIA_ROOT),
            'path_processed': os.path.relpath(paths['processed'], storage.MEDIA_ROOT)
        }
        
        # 9. Salva metadados no banco
        db.add_video_record(db_metadata)
        
        # 10. Salva metadados extras no meta.json
        storage.save_meta_json(paths['meta'], {'checksum': 'TODO', 'filter_params': {}})

        return jsonify({'message': 'Upload e processamento concluídos com sucesso!', 'id': video_uuid}), 201

    except Exception as e:
        # Em caso de erro, limpa o arquivo temporário se ele ainda existir
        if os.path.exists(incoming_path):
            os.remove(incoming_path)
        print(f"ERRO: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/videos', methods=['GET'])
def get_videos():
    """Retorna uma lista de todos os vídeos registrados no banco."""
    videos = db.get_all_videos()
    return jsonify(videos)

@bp.route('/media/<path:filename>')
def serve_media(filename):
    """Serve os arquivos de mídia (vídeos, thumbs) para o cliente."""
    return send_from_directory(storage.MEDIA_ROOT, filename)