import os
from pathlib import Path
from runtime.core.Config import DATA_DIR, BASE_PATH


def test_data_dir_resolution():
    """
    Garante que o DATA_DIR aponte para um diretório existente (seja data, data/dev ou data/prod).
    """
    assert DATA_DIR is not None
    assert isinstance(DATA_DIR, Path)
    assert DATA_DIR.exists(), f"O diretório de dados {DATA_DIR} deve existir no ambiente de execução."
