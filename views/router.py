"""
Módulo de rotas da aplicação Flask.

Responsável por:
- Renderizar páginas (rotas GET)
- Expor API REST (criar, listar, visualizar, atualizar, deletar pacientes)
- Realizar validações e cálculos auxiliares (idade, IMC, TMB)
"""

from flask import render_template, request, jsonify, redirect, url_for
from main import app
import sqlite3 as sq
import traceback
from datetime import datetime
from models.database import DB_PATH
from models.calculation import classification, calc_age, bmi_calc, basal_metabolic_rate

# ROTAS GET - Renderização das páginas HTML
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/cadastrar")
def cadastrar():
    return render_template('create.html')

@app.route("/listar")
def listar():
    try:
        with sq.connect(DB_PATH) as con:
            con.row_factory = sq.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM patients ORDER BY name")
            patients = cur.fetchall()
        return render_template('list.html', patients=patients)
    except Exception as e:
        return render_template('list.html', patients=[], error=str(e))

@app.route("/visualizar")
def visualizar():
    patient_id = request.args.get('id', None)
    return render_template('show.html', patient_id=patient_id)

@app.route("/deletar")
def deletar():
    return render_template('delete.html')

@app.route("/atualizar")
def atualizar():
    return render_template('update.html')

# ROTAS API - POST, PUT, DELETE
@app.route("/api/paciente/criar", methods=['POST'])
def api_create_patient():
    """Cria um novo paciente após validar os campos de entrada."""
    data = request.get_json()
    
    if not data.get('name') or len(data.get('name', '')) < 3 or len(data.get('name', '')) > 100:
        return jsonify({'success': False, 'error': 'Nome deve ter entre 3 e 100 caracteres'}), 400
    
    # Valida data de nascimento (YYYY-MM-DD) e faixa de idade
    try:
        birth_date_str = data.get('birth_date')
        date_of_birth = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        age = calc_age(birth_date_str)
        if age < 18 or age > 120:
            return jsonify({'success': False, 'error': 'Idade deve estar entre 18 e 120 anos'}), 400
    except:
        return jsonify({'success': False, 'error': 'Data de nascimento inválida'}), 400
    
    # Converte e valida altura
    try:
        height = float(data.get('height', 0))
        if height < 0.63 or height > 2.51:
            return jsonify({'success': False, 'error': 'Altura deve estar entre 0.63m e 2.51m'}), 400
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Altura inválida'}), 400
    # Converte e valida peso
    try:
        weight = float(data.get('weight', 0))
        if weight < 6 or weight > 635:
            return jsonify({'success': False, 'error': 'Peso deve estar entre 6kg e 635kg'}), 400
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Peso inválido'}), 400
    
    # Valida gênero biológico (M/F)
    gender = data.get('gender', '').upper()
    if gender not in ['M', 'F']:
        return jsonify({'success': False, 'error': 'Gênero deve ser M ou F'}), 400
    
    try:
        # Insere o novo paciente no banco de dados
        with sq.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute("""INSERT INTO patients (name, birth_date, height, weight, biological_gender)
                VALUES (?, ?, ?, ?, ?)""", (data['name'], date_of_birth, height, weight, gender))
            con.commit()
        return jsonify({'success': True, 'message': 'Paciente criado com sucesso'}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route("/api/paciente/<int:patient_id>", methods=['GET'])
def api_get_patient(patient_id):
    """Retorna dados do paciente e cálculos derivados (idade, IMC, TMB)."""
    try:
        with sq.connect(DB_PATH) as con:
            con.row_factory = sq.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
            patient = cur.fetchone()
        
        if not patient:
            return jsonify({'success': False, 'error': 'Paciente não encontrado'}), 404
        
        patient_dict = dict(patient)
        # Interpreta diferentes formatos de data que podem estar no banco
        birth_date_str = patient_dict.get('birth_date')
        birth_date = None
        for fmt in ('%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S'):
            try:
                birth_date = datetime.strptime(birth_date_str, fmt).date()
                break
            except Exception:
                continue
        if birth_date is None:
            # Fallback: extrai apenas a parte da data (caso haja horário anexado)
            try:
                date_part = birth_date_str.split('T')[0].split(' ')[0]
                birth_date = datetime.strptime(date_part, '%Y-%m-%d').date()
            except Exception:
                birth_date = None

        # Calcula idade a partir da data de nascimento
        age = None
        if birth_date:
            age = calc_age(birth_date)

        # Calcula IMC a partir de peso e altura
        weight = patient_dict.get('weight')
        height = patient_dict.get('height')
        bmi = bmi_calc(weight, height)

        # Classifica o IMC
        bmi_classification = classification(bmi)

        # Calcula a Taxa Metabólica Basal (TMB)
        gender = patient_dict.get('biological_gender')
        bmr = basal_metabolic_rate(weight, height, age, gender)
        
        return jsonify({
            'success': True,
            'patient': patient_dict,
            'age': age,
            'bmi': round(bmi, 2) if bmi is not None else None,
            'bmi_classification': bmi_classification,
            'basal_metabolic_rate': round(bmr, 2) if bmr is not None else None
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route("/api/paciente/<int:patient_id>/deletar", methods=['DELETE'])
def api_delete_patient(patient_id):
    """Remove um paciente pelo ID (se existir)."""
    try:
        with sq.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute("SELECT id FROM patients WHERE id = ?", (patient_id,))
            if not cur.fetchone():
                return jsonify({'success': False, 'error': 'Paciente não encontrado'}), 404
            
            cur.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
            con.commit()
        
        return jsonify({'success': True, 'message': 'Paciente deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route("/api/paciente/<int:patient_id>/atualizar", methods=['PUT'])
def api_update_patient(patient_id):
    """Atualiza campos permitidos do paciente (nome, altura, peso, gênero, data de nascimento)."""
    data = request.get_json()
    
    try:
        with sq.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
            patient = cur.fetchone()
            if not patient:
                return jsonify({'success': False, 'error': 'Paciente não encontrado'}), 404
            
            updates = []
            params = []
            
            # Atualiza nome (3 a 100 caracteres)
            if 'name' in data and data['name']:
                if len(data['name']) < 3 or len(data['name']) > 100:
                    return jsonify({'success': False, 'error': 'Nome deve ter entre 3 e 100 caracteres'}), 400
                updates.append("name = ?")
                params.append(data['name'])
            
            # Atualiza altura, validando faixa e tipo
            if 'height' in data and data['height']:
                try:
                    height = float(data['height'])
                    if height < 0.63 or height > 2.51:
                        return jsonify({'success': False, 'error': 'Altura deve estar entre 0.63m e 2.51m'}), 400
                    updates.append("height = ?")
                    params.append(height)
                except (ValueError, TypeError):
                    return jsonify({'success': False, 'error': 'Altura inválida'}), 400
            
            # Atualiza peso, validando faixa e tipo
            if 'weight' in data and data['weight']:
                try:
                    weight = float(data['weight'])
                    if weight < 6 or weight > 635:
                        return jsonify({'success': False, 'error': 'Peso deve estar entre 6kg e 635kg'}), 400
                    updates.append("weight = ?")
                    params.append(weight)
                except (ValueError, TypeError):
                    return jsonify({'success': False, 'error': 'Peso inválido'}), 400
            
            # Atualiza gênero biológico (M/F)
            if 'gender' in data and data['gender']:
                gender = data['gender'].upper()
                if gender not in ['M', 'F']:
                    return jsonify({'success': False, 'error': 'Sexo deve ser M ou F'}), 400
                updates.append("biological_gender = ?")
                params.append(gender)

            # Permite atualizar data de nascimento diretamente (YYYY-MM-DD)
            if 'birth_date' in data and data['birth_date']:
                try:
                    # Valida o formato e checa a idade resultante
                    bd = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
                    age_tmp = None
                    today = datetime.now().date()
                    age_tmp = (today - bd).days // 365
                    if age_tmp < 0 or age_tmp > 120:
                        return jsonify({'success': False, 'error': 'Data de nascimento inválida para idade aceitável'}), 400
                    updates.append("birth_date = ?")
                    params.append(bd.strftime('%Y-%m-%d'))
                except Exception:
                    return jsonify({'success': False, 'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400

            # Nota: atualização por idade foi removida — use apenas birth_date
            
            if not updates:
                return jsonify({'success': False, 'error': 'Nenhum campo para atualizar'}), 400
            
            params.append(patient_id)
            query = f"UPDATE patients SET {', '.join(updates)} WHERE id = ?"
            cur.execute(query, params)
            con.commit()
        
        return jsonify({'success': True, 'message': 'Paciente atualizado com sucesso'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
