"""Configurações globais e mapeamento de diretórios do projeto."""
import os
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent
RUNTIME_DIR = BASE_PATH / 'runtime'

# Detecção resiliente do diretório de dados para Docker e execuções locais (pytest/scripts)
_custom_data_dir = os.getenv('DATA_DIR')
if _custom_data_dir:
    DATA_DIR = Path(_custom_data_dir)
else:
    # 1. Se montado diretamente pelo Docker em /app/data ou se arquivos estiverem na raiz de data
    default_data = BASE_PATH / 'data'
    if (default_data / 'document_map.json').exists():
        DATA_DIR = default_data
    else:
        # 2. Se executando no host/WSL fora do container, busca na subpasta do ambiente (dev ou prod)
        env = os.getenv('ENVIRONMENT', 'development').lower()
        subfolder = 'prod' if 'prod' in env else 'dev'
        env_data = default_data / subfolder
        DATA_DIR = env_data if env_data.exists() else default_data

DOCUMENT_MAP_PATH = DATA_DIR / 'document_map.json'
POSTINGS_BIN_PATH = DATA_DIR / 'postings.bin'
VOCAB_PATH = DATA_DIR / 'vocabulario.json'
IDF_PATH = DATA_DIR / 'idf.json'
NORMS_PATH = DATA_DIR / 'norms.json'

SECRETS_FILE = RUNTIME_DIR / 'secrets'

INDEX_ARTIFACTS_DIR = DATA_DIR
LOG_DIR_OUTPUT = DATA_DIR
LOG_FILES_DIR = LOG_DIR_OUTPUT
