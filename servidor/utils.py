import uuid
from datetime import datetime

def generate_uuid():
    """Gera uma string UUID única."""
    return str(uuid.uuid4())

def get_current_timestamp():
    """Retorna o timestamp atual no formato ISO 8601."""
    return datetime.now().isoformat()