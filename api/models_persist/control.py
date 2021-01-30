import os
import json
from .modelos import Aluno, Prova, Questao, Resposta
import sqlite3
from flask import jsonify

###############################################################################
# conexão com DB e funções genericas de SQL
###############################################################################

def conexao():
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        db = os.path.join(path, '..\data\escolaALF.db')

        print('open db', path, db)

        conn = sqlite3.connect(db)        
        #conn = sqlite3.connect('\\api\\data\\escolaALF.db')
        return conn
    except Exception as E:
        print('erro open db', E)
        return E 

def execute(comando = '', tipo = 'I'):
    id_retorno = -1
    if comando == '':
        resultado = 'Não executado'
    else:
        try:
            conn = conexao() 
            sql = conn.cursor()
            sql.execute(comando)
            conn.commit()
            if tipo == 'I':
                id_retorno = sql.lastrowid
            conn.close()
            resultado = 'OK'
        except Exception as E:
            resultado = E
    return resultado, id_retorno

def query(sql = ''):
    if sql == '':
        exit
    try:
        conn = conexao()
        curr = conn.cursor().execute(sql)
        data_json = []
        header = [i[0] for i in curr.description]
        data = curr.fetchall()
        for i in data:
            data_json.append(dict(zip(header, i)))
        resultado = data_json
        conn.close()
    except Exception as E:
        resultado = E
    return resultado
        
###############################################################################
# CRUD - Alunos
###############################################################################

def query_aluno(id = 0):
    if id == 0:
        comando = 'select id, nome from aluno order by id'
    elif id == -1:
        comando = 'select id, nome from aluno order by nome'
    else:
        sid = str(id)
        comando = f'select id, nome from aluno where id={sid}'
    return query(comando)
        
def insert_aluno(nome = ''):
    if query_count_aluno() > 99:
        return 'Não é possívelincluir mais aluns'
    comando = f'insert into aluno(nome) values ("{nome}") '
    return execute(comando, 'I')

def update_aluno(id = 0, nome = ''):
    comando = f'update aluno set nome = "{nome}" where id = {id}'
    return execute(comando, 'U')

def delete_aluno(id = 0):
    comando = f'delete from aluno where id = {id}'
    return execute(comando, 'D')

def query_count_aluno():
    return conexao().cursor().execute('select count(*) as qtd from aluno').fetchone()[0]


###############################################################################
# CRUD - Prova
###############################################################################

def query_prova(id = 0):
    sid = str(id)
    comando = f'select id, nome from prova where id={sid}'
    return query(comando)
        
def insert_prova(prova:Prova):
    nome = prova.nome
    comando = f'insert into prova(nome, situacao) values ("{nome}", "incompleta") '
    ## loop para incluir as questões
    return execute(comando, 'I')

def update_prova(id = 0, nome = '', situacao = ''):
    comando = f'update prova set nome = "{nome}", situacao = "{situacao}" where id = {id}'
    return execute(comando, 'U')

def delete_prova(id = 0):
    comando = f'delete from prova where id = {id}'
    return execute(comando, 'D')



###############################################################################
# CRUD - Questões da prova
###############################################################################

def query_questa(id_prova = 0):
    sid = str(id_prova)
    comando = f'select id, id_prova, enunciado, peso, resposta_correta, resposta1, resposta2, resposta3 from questao where id_prova={sid}'
    return query(comando)
        
def insert_questao(questao:Questao):
    comando = f'''insert into questao(id_prova, enunciado, peso, resposta_correta, resposta1, resposta2, resposta3) 
                              values ( {questao.id_prova},
                                      "{questao.enunciado}",
                                       {questao.peso},
                                       {questao.resposta_correta},
                                      "{questao.resposta1}",
                                      "{questao.resposta2}",
                                      "{questao.resposta3}") '''
    return execute(comando, 'I')

def update_prova(questao: Questao):
    comando = f'''update questao set enunciado = "{questao.enunciado}",
                                   peso = {questao.peso} ,
                                   resposta_correta = "{questao.resposta_correta}" ,
                                   resposta1 = {questao.resposta1} ,
                                   resposta2 = {questao.resposta2} ,
                                   resposta3 = {questao.resposta3}
                                   where id = {id}'''
    return execute(comando, 'U')

def delete_prova(id = 0):
    comando = f'delete from questao where id = {id}'
    return execute(comando, 'D')


###############################################################################
# CRUD - Respostas
###############################################################################

def insert_resposta(resposta:Resposta):
    comando = f'''insert into reposta(id_prova, enunciado, peso, resposta_correta, resposta1, resposta2, resposta3) 
                              values ( {questao.id_prova},
                                      "{questao.enunciado}",
                                       {questao.peso},
                                       {questao.resposta_correta},
                                      "{questao.resposta1}",
                                      "{questao.resposta2}",
                                      "{questao.resposta3}") '''
    return execute(comando, 'I')


###############################################################################
# Rotinas de Resultados
###############################################################################

def query_nota_final():
    comando = '''select aluno_id as id, 
                        aluno_nome as nome,        
                        avg(media) as media_final       
                    from (
                        select al.id as aluno_id, 
                            al.nome as aluno_nome, 
                            pr.id as prova_id, 
                            pr.nome as prova_nome, 
                            ifnull((select sum(qu2.peso)
                                        from questao qu2 
                                        where qu2.id = qu.id 
                                        and qu2.resposta_correta = re.resposta), 0) as soma_pontos, 
                            ifnull(count(pr.id), 1) as qtd,
                            (ifnull((select sum(qu2.peso)
                                        from questao qu2 
                                        where qu2.id = qu.id 
                                        and qu2.resposta_correta = re.resposta), 0) / ifnull(count(pr.id), 1)) as media
                        from aluno al  
                        join resposta re on (re.id_aluno = al.id)  
                        join questao qu on (re.id_questao = qu.id)
                        join prova pr on (qu.id_prova = pr.id)  
                        where pr.situacao = "Liberada" 
                        group by pr.id, al.id     
                    ) group by aluno_id '''
    return query(comando)


def query_aprovados():
    comando = '''select * from (
                    select aluno_id as id, 
                            aluno_nome as nome,        
                            avg(media) as nota_final       
                    from (
                        select al.id as aluno_id, 
                                al.nome as aluno_nome, 
                                pr.id as prova_id, 
                                pr.nome as prova_nome, 
                                ifnull((select sum(qu2.peso)
                                        from questao qu2 
                                        where qu2.id = qu.id 
                                            and qu2.resposta_correta = re.resposta), 0) as soma_pontos, 
                                ifnull(count(pr.id), 1) as qtd,
                                (ifnull((select sum(qu2.peso)
                                        from questao qu2 
                                        where qu2.id = qu.id 
                                            and qu2.resposta_correta = re.resposta), 0) / ifnull(count(pr.id), 1)) as media
                            from aluno al  
                            join resposta re on (re.id_aluno = al.id)  
                            join questao qu on (re.id_questao = qu.id)
                            join prova pr on (qu.id_prova = pr.id)  
                        where pr.situacao = "Liberada" 
                        group by pr.id, al.id     
                    ) group by aluno_id    )
                    where nota_final >= 7 '''
    return query(comando)
