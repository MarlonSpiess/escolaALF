def test_inicial_ok():
    assert 1==1

import os
path = os.path.dirname(os.path.abspath(__file__))
print('======>  caminho ',path)

from api.models_persist.modelos import Aluno, Prova, Resposta
from api.models_persist.control import *

def test_cria_aluno():
    aluno = Aluno()
    aluno.id = 1
    aluno.nome = 'Marlon'
    print(aluno.nome)
    assert aluno.id == 1
    assert aluno.nome == 'Marlon'

def test_query_count_aluno():
    sql = 'select count(*) from aluno'
    resultado = query(sql)
    print(resultado)
    assert len(resultado) > 0

def test_query_count_alias():
    sql = 'select count(*) as total_alunos from aluno'
    resultado = query(sql)
    qtd_alunos = resultado[0]
    print(resultado)
    assert resultado[0].get('total_alunos') == 92
    assert len(resultado) > 0

def test_aluno_tojson_fromjson():
    aluno = Aluno()
    aluno.fromJson({"id":1, "nome":"Marlon"})
    assert aluno.id == 1
    assert aluno.nome == 'Marlon'

