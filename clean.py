"""
Utilitário para limpeza de diretórios __pycache__.

Percorre recursivamente o diretório do projeto removendo pastas __pycache__
criadas pelo interpretador Python, ajudando a manter o workspace limpo.
"""

import os
import shutil


def clean_pycache(root_path=None):
    """Remove todas as pastas __pycache__ a partir de root_path.

    Parâmetros:
    - root_path: diretório raiz para iniciar a varredura. Se None, usa a pasta do arquivo atual.

    Retorna:
    - Lista de caminhos removidos (apenas para fins informativos).
    """
    removed = []
    if root_path is None:
        # Usa a pasta onde este arquivo está como raiz padrão
        root_path = os.path.dirname(os.path.abspath(__file__))

    # os.walk retorna (dirpath, dirnames, filenames) para cada diretório encontrado
    for dirpath, dirnames, _ in os.walk(root_path):
        # copia a lista pois vamos modificá-la durante a iteração
        for d in list(dirnames):
            if d == '__pycache__':
                full = os.path.join(dirpath, d)
                try:
                    shutil.rmtree(full)  # remove a pasta __pycache__ inteira
                    removed.append(full)
                except Exception:
                    # Ignora erros e segue em frente
                    pass
    return removed
