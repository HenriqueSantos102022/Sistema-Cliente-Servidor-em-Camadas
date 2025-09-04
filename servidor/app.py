from flask import Flask
from . import database as db
from . import storage
from .routes import bp

def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)
    
    # Registra o Blueprint com as rotas
    app.register_blueprint(bp)
    
    with app.app_context():
        # Inicializa o banco de dados e as pastas na primeira execução
        storage.setup_directories()
        db.init_db()
        
    return app

if __name__ == '__main__':
    app = create_app()
    # Executa o servidor em todas as interfaces de rede na porta 5000
    app.run(host='0.0.0.0', port=5000, debug=True)