from flask import Flask, request, jsonify
from api.models_persist.modelos import Aluno, Prova, Resposta
from api.models_persist.control import *

app = Flask(__name__)

@app.route('/api/aluno', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def request_aluno():

    '''
    #####################################################################
    # URI de aluno
    # controla chamadas para Aluno tipo GET, POST, PUT, DELETE
    # GET: params -> id:? onde: 0  = todos order id, 
    #                           -1 = todos order nome
    #                           ? = valr numerico indicado o id desejado
    # POST: body -> JSON do aluno para Update no DB
    #               exemplo: { "id" : 1 , "nome" : "Marlon Spiess"}
    # PUT: body -> JSON do aluno para Insert no DB
    #              exemplo: { "id" : 0 , "nome" : "Marlon Spiess"}
    #              retorno do ID gerado ou mesnsagem de erro
    # DELETE: params -> id:? onde ? é o valor do id desejado p/ excluir 
    ##################################################################### 
    '''

    if request.method == 'GET':
        id = 0
        if 'id' in request.args:
            id = int(request.args['id'])
        return jsonify(query_aluno(id)), 200
    elif request.method == 'POST':
        dados = request.get_json()
        aluno = Aluno()
        aluno.fromJson(dados)
        resultado, id = update_aluno(aluno.id, aluno.nome)
        if resultado == 'OK': 
            return jsonify(isError= False,
                        message= f'Aluno alterado com Sucesso {aluno.id} - {aluno.nome}',
                        statusCode= 202), 202
        else:
            return jsonify(isError= True,
                        message= f'Erro ao alterar Aluno: {aluno.id} - {aluno.nome}',
                        statusCode= 400), 400
    elif request.method == 'PUT':
        if query_count_aluno() > 99:
            return jsonify(isError= True,
                        message= f'Erro ao incluir Aluno, não é possível ter mais que 100 alunos',
                        statusCode= 400), 400
        dados = request.get_json()
        aluno = Aluno()
        aluno.fromJson(dados)
        resultado, id_retorno = insert_aluno(aluno.nome) 
        if id_retorno > 0:
            return jsonify(isError= False,
                        message= f'Aluno incuso com Sucesso {id_retorno} - {aluno.nome}',
                        id = id_retorno,
                        statusCode= 202), 202
        else:
            return jsonify(isError= True,
                        message= f'Erro ao incluir Aluno: {aluno.nome}',
                        statusCode= 400), 400
    elif request.method == 'DELETE':
        id = 0
        if 'id' in request.args:
            id = int(request.args['id'])
        resultado, id = delete_aluno(id)
        if resultado == 'OK': 
            return jsonify(isError= False,
                        message= f'Aluno excluido com Sucesso {id} ',
                        statusCode= 202), 202
        else:
            return jsonify(isError= True,
                        message= f'Erro ao excluir Aluno: {id} ',
                        statusCode= 400), 400

@app.route('/api/prova', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def request_prova():
    '''
        #####################################################################
        # URI de prova
        # controla chamadas para Aluno tipo GET, POST, PUT, DELETE
        # GET: params -> id:? onde ? é o valor do id desejado
        # POST: body -> (raw/json) JSON do aluno para Update no DB
        #               exemplo: { "id" : 1 , "nome" : "Python I"}
        # PUT: body -> (raw/json) JSON do aluno para Insert no DB
        #              exemplo: { "id" : 0 , "nome" : "Python inciante"}
        #              retorno do ID gerado ou mesnsagem de erro
        # DELETE: params -> id:? onde ? é o valor do id desejado p/ excluir 
        #####################################################################
    '''
    if request.method == 'GET':
        if 'id' in request.args:
            id = int(request.args['id'])
            resultado = jsonify(query_prova(id)), 200
        else:
            resultado = jsonify(isError= True,
                        message= f'Prova não encontrada',
                        statusCode= 400), 400
        return resultado
    elif request.method == 'POST':
        dados = request.get_json()
        prova = Prova()
        prova.fromJosn(dados)
        resultado, id = update_prova(prova.id, prova.nome)
        if resultado == 'OK': 
            return jsonify(isError= False,
                        message= f'Prova alterado com Sucesso {prova.id} - {prova.nome}',
                        statusCode= 202), 202
        else:
            return jsonify(isError= True,
                        message= f'Erro ao alterar Prova: {prova.id} - {prova.nome}',
                        statusCode= 400), 400
    elif request.method == 'PUT':
        dados = request.get_json()
        prova = Prova()
        prova.fromJson(dados)
        peso_total = 0
        for qt in prova.questoes:
            peso_total += qt.peso
            if qt.peso <0 or qt.peso > 10:
                return jsonify(isError= True,
                            message= f'Erro ao incluir Prova, questão {qt.enunciado} peso fora da faixa: {qt.peso}',
                            statusCode= 400), 400
        if peso_total < 0 or peso_total > 10:
            return jsonify(isError= True,
                        message= f'Erro ao incluir Prova, peso fora da faixa: {peso_total}',
                        statusCode= 400), 400
        nome = prova.nome
        if peso_total == 10:
            prova.situacao = "Liberada"
        resultado, id_retorno = insert_prova(prova) 
        if id_retorno > 0:
            ## loop das questões da prova
            for qt in prova.questoes:
                qt.id_prova = id_retorno
                insert_questao(qt)
            del prova
            return jsonify(isError= False,
                        message= f'Prova incusa com Sucesso {id_retorno} - {nome}',
                        id = id_retorno,
                        statusCode= 202), 202
        else:
            return jsonify(isError= True,
                        message= f'Erro ao incluir Prova: {prova.nome}',
                        statusCode= 400), 400
    elif request.method == 'DELETE':
        id = 0
        if 'id' in request.args:
            id = int(request.args['id'])
        resultado, id = delete_prova(id)
        if resultado == 'OK': 
            return jsonify(isError= False,
                        message= f'Prova excluída com Sucesso {id} ',
                        statusCode= 202), 202
        else:
            return jsonify(isError= True,
                        message= f'Erro ao excluir Prova: {id} ',
                        statusCode= 400), 400



@app.route('/api/resposta', methods=['PUT'])
def request_resposta():
    '''
    #####################################################################
    # URI de resposta       
    # controla chamadas para Aluno tipo PUT - exclusivamente para inclusão
    # PUT: body -> JSON do aluno para Insert no DB
    #              exemplo: { ?????????????????????? }
    #              retorno do ID gerado ou mesnsagem de erro
    #####################################################################
    '''
    dados = request.get_json()
    resposta = Resposta()
    resposta.fromJson(dados)
    resultado, id_retorno = insert_resposta(resposta) 
    if id_retorno > 0:
        return jsonify(isError= False,
                    message= f'Resposta incusa com Sucesso {id_retorno}',
                    id = id_retorno,
                    statusCode= 202), 202
    else:
        return jsonify(isError= True,
                    message= f'Erro ao incluir Resposta',
                    statusCode= 400), 400


@app.route('/api/nota_final', methods=['GET'])
def request_nota_final():
    return jsonify(query_nota_final()), 200


@app.route('/api/aprovados', methods=['GET'])
def request_aprovados():
    return jsonify(query_aprovados()), 200



#####################################################################
# API rodando na porta 5000
#####################################################################

if __name__ == '__main__':
    help(request_aluno)
    help(request_prova)
    help(request_resposta)
    app.run(debug=True, port=5000)

