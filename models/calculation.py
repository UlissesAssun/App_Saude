"""
Funções de cálculo e classificação de dados de saúde.

Inclui:
- Idade precisa a partir da data de nascimento
- Cálculo de IMC (BMI)
- Taxa Metabólica Basal (Mifflin-St Jeor)
- Classificação do IMC conforme faixas da OMS
"""

from datetime import datetime

def bmi_calc(weight, height):
    """Calcula o IMC (BMI) a partir do peso (kg) e altura (m)."""
    if weight is None or height is None or height == 0:
        return None
    try:
        return float(weight) / (float(height) ** 2)
    except (ValueError, TypeError, ZeroDivisionError):
        return None

def calc_age(date_of_birth):
    """Calcula a idade considerando corretamente ano, mês e dia."""
    if isinstance(date_of_birth, str):
        birth_date = datetime.strptime(date_of_birth[:10], "%Y-%m-%d").date()
    else:
        birth_date = date_of_birth
    
    today = datetime.now().date()
    age = today.year - birth_date.year
    
    # Se o aniversário ainda não ocorreu neste ano, subtrai 1
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return age

def basal_metabolic_rate(weight, height, age, gender):
    """Calcula a TMB usando a equação de Mifflin-St Jeor."""
    if None in (weight, height, age, gender):
        return None
    
    try:
        weight = float(weight)
        height = float(height)
        age = int(age)
        gender = str(gender).upper()
        
        if gender == "M":
            bmr = (10 * weight) + (6.25 * height * 100) - (5 * age) + 5
        elif gender == "F":
            bmr = (10 * weight) + (6.25 * height * 100) - (5 * age) - 161
        else:
            return None
        
        return bmr
    except (ValueError, TypeError):
        return None

def classification(bmi):
    """Classifica o IMC em quatro faixas padronizadas.

    Faixas utilizadas:
    - Abaixo do peso: IMC < 18.5
    - Normal: 18.5 <= IMC < 25
    - Sobrepeso: 25 <= IMC < 30
    - Obeso: IMC >= 30
    """
    if bmi is None:
        return None
    try:
        bmi = float(bmi)
    except (TypeError, ValueError):
        return None
    if bmi < 18.5:
        return "Abaixo do peso"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Sobrepeso"
    return "Obeso"
    

