# App Saúde

Aplicação Flask para cadastro e gestão de pacientes com cálculo de IMC (BMI) e Taxa Metabólica Basal (TMB).

## Visão Geral
- Backend: Flask + SQLite
- Frontend: Jinja2 (templates), CSS modular em `static/css`, JS em `static/js`
- Cálculos: IMC, TMB (Mifflin-St Jeor) e classificação do IMC
- Páginas: Início, Cadastrar, Listar, Visualizar, Deletar, Atualizar

## Estrutura do Projeto
```
App_Saude/
  main.py                # Ponto de entrada da aplicação
  clean.py               # Limpa diretórios __pycache__ ao encerrar
  models/
    database.py          # Inicialização do banco e path do .db
    calculation.py       # Funções de cálculo (idade, BMI, TMB, classificação)
  views/
    router.py            # Rotas das páginas e API REST
  templates/             # Páginas HTML (Jinja2)
  static/
    css/                 # Estilos CSS por página
    js/
      api.js             # Integração com a API via fetch
```

## Banco de Dados
- Arquivo: `database.db` (SQLite)
- Tabela: `patients`
  - `id` (INTEGER, PK)
  - `name` (TEXT)
  - `birth_date` (TEXT, YYYY-MM-DD)
  - `height` (REAL, em metros)
  - `weight` (REAL, em kg)
  - `biological_gender` (TEXT, 'M'|'F')
  - `created_at` (TEXT, datetime SQLite)

## Validações
- Nome: 3 a 100 caracteres
- Idade: 18 a 120 anos (derivada de `birth_date`)
- Altura: 0.63m a 2.51m
- Peso: 6kg a 635kg
- Gênero: 'M' ou 'F'
- Formato de data aceito para criação/atualização: `YYYY-MM-DD`

## Cálculos
- Idade: cálculo preciso considerando mês/dia
- IMC (BMI): peso/(altura^2)
- TMB (Mifflin-St Jeor):
  - Homem: `10*peso + 6.25*altura_cm - 5*idade + 5`
  - Mulher: `10*peso + 6.25*altura_cm - 5*idade - 161`

### Classificação do IMC
- Abaixo do peso: IMC < 18.5
- Normal: 18.5 ≤ IMC < 25
- Sobrepeso: 25 ≤ IMC < 30
- Obeso: IMC ≥ 30

## Rotas Principais (Páginas)
- `GET /` → Início
- `GET /cadastrar` → Formulário de cadastro
- `GET /listar` → Tabela de pacientes
- `GET /visualizar` → Busca por ID e exibição
- `GET /deletar` → Exclusão por ID (com confirmação por nome)
- `GET /atualizar` → Atualização parcial por ID (nome, altura, peso, gênero, birth_date)

## API Endpoints
- `POST /api/paciente/criar`
  - Body JSON: `{"name":"...","birth_date":"YYYY-MM-DD","gender":"M|F","height":1.80,"weight":80}`
- `GET /api/paciente/<id>`
  - Retorna dados + `age`, `bmi`, `bmi_classification`, `basal_metabolic_rate`
- `PUT /api/paciente/<id>/atualizar`
  - Atualização parcial; aceita chaves: `name`, `height`, `weight`, `gender`, `birth_date`
- `DELETE /api/paciente/<id>/deletar`

## Como Executar (Windows PowerShell)
1. Instale o Python 3.x
2. No diretório do projeto, execute:
```powershell
python -m pip install --upgrade pip
# (sem dependências externas além da stdlib)
python main.py
```
- O servidor sobe em `http://127.0.0.1:82`

## Teste Rápido (via UI)
- Abra `http://127.0.0.1:82`
- Cadastre um paciente em `/cadastrar`
- Liste em `/listar` e clique em "Ver"
- Visualize por ID em `/visualizar`
- Atualize em `/atualizar`
- Exclua em `/deletar` (confirmação exibe o nome)

## Notas
- `views/router.py` é tolerante a formatos de data legados ao ler do banco (inclui fallback).
- Pastas `__pycache__` são limpas ao encerrar (`clean_pycache`).
- IDs dos inputs HTML permanecem em PT-BR; as chaves JSON enviadas para API são em inglês.
