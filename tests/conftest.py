import os
import sys
import json
import sqlite3
import tempfile
from pathlib import Path
import pytest
from unittest.mock import AsyncMock, MagicMock

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "runtime") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "runtime"))

os.environ.setdefault("ENVIRONMENT", "development")

# Se os dados reais de 14GB não existirem (ex: no runner de CI do GitHub Actions),
# gera automaticamente artefatos sintéticos mínimos para viabilizar os testes sem erros.
real_data_dir = PROJECT_ROOT / "data" / "dev"
if not (real_data_dir / "document_map.json").exists() and not (PROJECT_ROOT / "data" / "document_map.json").exists():
    ci_test_dir = Path(tempfile.mkdtemp(prefix="phishio_ci_data_"))
    
    # 1. document_map.json
    with open(ci_test_dir / "document_map.json", "w", encoding="utf-8") as f:
        json.dump({"1": "https://example.com/safe", "2": "https://example.com/phishing"}, f)
        
    # 2. norms.json
    with open(ci_test_dir / "norms.json", "w", encoding="utf-8") as f:
        json.dump({"1": 1.0, "2": 1.0}, f)
        
    # 3. idf_warm.db (SQLite)
    conn = sqlite3.connect(ci_test_dir / "idf_warm.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS term_idf (termo TEXT PRIMARY KEY, idf REAL, offset_bin INTEGER, len_bin INTEGER)")
    cursor.execute("INSERT OR REPLACE INTO term_idf VALUES ('gratis', 1.5, 0, 8)")
    cursor.execute("INSERT OR REPLACE INTO term_idf VALUES ('promo', 1.2, 8, 8)")
    conn.commit()
    conn.close()
    
    # 4. postings.bin (dummy binary postings)
    with open(ci_test_dir / "postings.bin", "wb") as f:
        f.write(b"\x00" * 32)
        
    os.environ["DATA_DIR"] = str(ci_test_dir)


@pytest.fixture(autouse=True)
def mock_mongo(monkeypatch):
    """
    Mock global do MongoDB para todos os testes.
    Permite executar a suíte de testes de forma rápida e isolada sem depender
    de um servidor MongoDB real rodando em background.
    """
    mock_col = MagicMock()
    mock_col.find_one = AsyncMock(return_value=None)
    mock_col.update_one = AsyncMock()
    mock_col.insert_one = AsyncMock()

    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_col

    monkeypatch.setattr("runtime.main.db", mock_db)
    monkeypatch.setattr("runtime.main.col_reputacao", mock_col)
    monkeypatch.setattr("runtime.main.col_reports", mock_col)
    monkeypatch.setattr("runtime.main.col_consent", mock_col)
    return mock_col
