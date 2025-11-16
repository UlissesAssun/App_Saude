"""
Script auxiliar para testar parsing de datas com diferentes formatos.

Objetivo: validar que as tentativas de formatos e o fallback por "split"
convertem corretamente strings como "YYYY-MM-DD", "YYYY-MM-DD HH:MM:SS"
e "YYYY-MM-DDTHH:MM:SS" para um objeto date.
"""

from datetime import datetime

# Exemplo de string com separador 'T' e horário zero
s = '1960-08-05T00:00:00'

# Conjunto de formatos a testar diretamente via strptime
fmts = ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S']

for fmt in fmts:
    try:
        d = datetime.strptime(s, fmt).date()
        print('fmt', fmt, '->', d)
    except Exception as e:
        print('fmt', fmt, 'err', e)

# Fallback: extrai somente a porção de data (antes de 'T' ou espaço)
try:
    date_part = s.split('T')[0].split(' ')[0]
    d2 = datetime.strptime(date_part, '%Y-%m-%d').date()
    print('split->', d2)
except Exception as e:
    print('split err', e)
