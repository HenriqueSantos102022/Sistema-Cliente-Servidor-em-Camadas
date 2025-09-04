import sqlite3
import os

# Define o caminho do banco de dados na pasta do servidor
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'videos.db')

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return conn

def init_db():
    """Inicializa o banco de dados, criando a tabela de vídeos se não existir."""
    if os.path.exists(DATABASE_PATH):
        print("Banco de dados já existe.")
        return

    print("Criando banco de dados...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Script SQL para criar a tabela conforme especificado
    cursor.execute("""
    CREATE TABLE videos (
        id TEXT PRIMARY KEY,
        original_name TEXT NOT NULL,
        original_ext TEXT NOT NULL,
        mime_type TEXT,
        size_bytes INTEGER,
        duration_sec REAL,
        fps REAL,
        width INTEGER,
        height INTEGER,
        filter TEXT,
        created_at TEXT NOT NULL,
        path_original TEXT NOT NULL,
        path_processed TEXT NOT NULL
    );
    """)
    
    conn.commit()
    conn.close()
    print("Banco de dados e tabela 'videos' criados com sucesso.")

def add_video_record(metadata):
    """Adiciona um novo registro de vídeo ao banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO videos (
        id, original_name, original_ext, mime_type, size_bytes, duration_sec, 
        fps, width, height, filter, created_at, path_original, path_processed
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        metadata['id'],
        metadata['original_name'],
        metadata['original_ext'],
        metadata.get('mime_type'),
        metadata.get('size_bytes'),
        metadata.get('duration_sec'),
        metadata.get('fps'),
        metadata.get('width'),
        metadata.get('height'),
        metadata.get('filter'),
        metadata['created_at'],
        metadata['path_original'],
        metadata['path_processed']
    ))
    
    conn.commit()
    conn.close()

def get_all_videos():
    """Retorna todos os registros de vídeos do banco de dados."""
    conn = get_db_connection()
    videos = conn.execute('SELECT * FROM videos ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(video) for video in videos]