from flask import json
import json


class JsonSerializable(object):

    # @classmethod
    # def fromJson(cls, json_str):
    #     json_dict = json.loads(json_str)
    #     return cls(**json_dict)

    @classmethod
    def toJson(self):
       return json.dumps(self.__dict__)
        # return json.dumps(self, default=lambda o: o.__dict__,)

    def __repr__(self):
        return self.toJson()


class Aluno(JsonSerializable):

    id = 0
    nome = ''

    def fromJson(self, json):
        self.id = json.get('id')
        self.nome = json.get('nome')

class Prova(JsonSerializable):

    id = 0
    nome = ''
    questoes = []
    situacao = ''

    def fromJson(self, json):
        self.id = json.get('id')
        self.nome = json.get('nome')
        qts = json.get('questoes')
        for qt in qts:
            lqt = Questao()
            lqt.fromJson(qt)
            self.questoes.append(lqt)

class Questao(JsonSerializable):

    id = 0
    id_prova = 0
    enunciado = ''
    peso = 0
    resposta_correta = 0
    resposta1 = ''
    resposta2 = ''
    resposta3 = ''

    def fromJson(self, json):
        self.id = json.get('id')
        self.id_prova = json.get('id_prova')
        self.enunciado = json.get('enunciado')
        self.peso = json.get('peso')
        self.resposta_correta = json.get('resposta_correta')
        self.resposta1 = json.get('resposta1')
        self.resposta2 = json.get('resposta2')
        self.resposta3 = json.get('resposta3')

    def toJson(self):
       return json.dumps(self)


class Resposta(JsonSerializable):

    id = 0
    id_questao = 0
    id_aluno = 0
    resposta = 0

    def fromJosn(self, json):
        self.id = json.get('id')
        self.id_questao = json.get('id_questao')
        self.id_aluno = json.get('id_aluno')
        self.resposta = json.get('resposta')

