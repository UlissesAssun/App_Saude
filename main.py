"""
Ponto de entrada da aplicação Flask.

Responsabilidades:
- Inicializar o banco de dados na primeira execução.
- Subir o servidor Flask na porta 82.
- Limpar diretórios __pycache__ ao encerrar a aplicação.
"""

import models.database as db
from flask import Flask
from clean import clean_pycache

# Cria a instância do app Flask informando onde estão templates e arquivos estáticos
app = Flask(__name__, template_folder='templates', static_folder='static')

# Importa as rotas após criar o app (evita import circular)
from views.router import * 

def main():
    """Função principal: garante que a base esteja criada/atualizada."""
    db.init_database()

if __name__ == "__main__":
    try:
        # Inicializa banco e inicia servidor web
        main()
        # Executa o servidor Flask em http://127.0.0.1:82
        app.run(port=82)
    finally:
        # Independentemente de erro/encerramento, remove __pycache__
        clean_pycache()

