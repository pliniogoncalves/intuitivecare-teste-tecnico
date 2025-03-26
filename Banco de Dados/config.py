import os
from pathlib import Path

# Configurações de diretórios
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DEMONSTRACOES_DIR = DATA_DIR / "demonstracoes_contabeis"
SQL_SCRIPTS_DIR = BASE_DIR / "scripts" / "sql"

# Configurações de banco de dados
DB_CONFIG = {
    'dbname': 'ans_database',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

# URLs para download
URLS = {
    'operadoras': 'https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/',
    'demonstracoes': 'https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/'
}

# Garante que os diretórios existam
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DEMONSTRACOES_DIR, exist_ok=True)
os.makedirs(SQL_SCRIPTS_DIR, exist_ok=True)