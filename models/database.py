"""
Camada de acesso a dados: inicialização e configuração da base SQLite.

Exposição:
- DB_PATH: caminho do arquivo .db
- init_database(): cria a tabela "patients" caso não exista
"""

import sqlite3 as sq

# Caminho do arquivo de banco de dados SQLite
DB_PATH = 'database.db'


def init_database():
    """Cria a tabela `patients` se ainda não existir."""
    with sq.connect(DB_PATH) as con:
        cur = con.cursor()
        # Estrutura da tabela com validações mínimas via NOT NULL/DEFAULT
        cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL DEFAULT '',
                    birth_date TEXT NOT NULL,
                    height REAL NOT NULL,
                    weight REAL NOT NULL,
                    biological_gender TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        """)
    
