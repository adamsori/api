# ENDPOINT 
from flask import Flask, Response, request
from flask_restx import Api, Resource, reqparse
import json
from src.server.instance import server


app, api = server.app, server.api

# Mock Data
accounts_db = []

# Herda da classe Resource (responsável por todos os recursos de GET, POST, PUT e DELETE)
# ENDPOIT reset
@api.route('/reset', endpoint='reset')
class Reset(Resource):
    # Método post que representa o método HTTP POST
    def post(self,):
        # Payload vem todos os parametros que vem no body da requisicao
        global accounts_db
        accounts_db.clear()
        return Response('OK', mimetype='application/json')

# ENDPOIT balance

@api.route('/balance', endpoint='balance')
@api.doc(params={'account_id': 'An account ID'}) # Falta implementar a documentação (Configurar os parametros para o swagger)
class Balance(Resource):
    
    # Método get que representa o método HTTP GET
    def get(self):
        global accounts_db
        # Agora temos o id enviado via GET
        
        id = request.args.get("account_id")
        # Fazemos a busca na lista de dicionarios do account_id desejado
        #index = next(iter(index for (index,d) in enumerate(accounts_db) if d['id'] == id), None)
        index = None
        for idx,acc in enumerate(accounts_db):
            if acc['id'] == id:
                index = idx
        # Caso a conta não exista, retorna 404. Se existir retorna o balance, 200
        if index == None:
            return 0, 404
        else:
            return accounts_db[index]['balance'], 200
            

# ENDPOIT event

@api.route('/event')
class Event(Resource):
    # Método post que representa o método HTTP POST
    def post(self):
        global accounts_db
        response_body = {}
        # Payload: body da requisição
        req_body = api.payload
        
        # Caso event == DEPOSIT
        if req_body['type'] == 'deposit':

            id = req_body['destination']
            amount = req_body['amount']
            account = next(iter(item for item in accounts_db if item['id'] == id), None)
            index = next(iter(index for (index,d) in enumerate(accounts_db) if d['id'] == id), None)
            # Se account não existir, cria-se uma nova com id e amount enviados
            if account is None:
                new_account = {"id": id, "balance": amount}
                print(new_account)
                accounts_db.append(new_account)
                response_body["destination"] = new_account
                return response_body, 201
            # Caso contrário, faz soma o valor do amount com o balance atual
            else:
               accounts_db[index]['balance'] = accounts_db[index]['balance'] + amount
               response_body['destination'] = accounts_db[index]
               return response_body, 201

        # Caso event == WITHDRAW
        elif req_body['type'] == 'withdraw':

            id = req_body['origin']
            amount = req_body['amount']
            account = next(iter(item for item in accounts_db if item['id'] == id), None)
            index = next(iter(index for (index,d) in enumerate(accounts_db) if d['id'] == id), None)
            # Se account não existir, retorna 0 404
            if account is None:
                return 0, 404
            # Caso contrário, subtrai do balance atual o amount
            else:
               accounts_db[index]['balance'] = accounts_db[index]['balance'] - amount
               response_body['origin'] = accounts_db[index]
               return response_body, 201


        # Caso event == TRANSFER
        elif req_body['type'] == 'transfer':
            origin_id = req_body['origin']
            destination_id = req_body['destination']
            amount = req_body['amount']
            
            orig_account = next(iter(item for item in accounts_db if item['id'] == origin_id), None)
            orig_index = next(iter(index for (index,d) in enumerate(accounts_db) if d['id'] == origin_id), None)

            if orig_account is not None:
                dest_account = next(iter(item for item in accounts_db if item['id'] == destination_id), None)
                dest_index = next(iter(index for (index,d) in enumerate(accounts_db) if d['id'] == destination_id), None)

                if dest_account is not None:
                    accounts_db[orig_index]['balance'] = accounts_db[orig_index]['balance'] - amount
                    accounts_db[dest_index]['balance'] = accounts_db[dest_index]['balance'] + amount
                    response_body['origin'] = accounts_db[orig_index]
                    response_body['destination'] = accounts_db[dest_index]
                    return response_body, 201
                else:
                    accounts_db[orig_index]['balance'] = accounts_db[orig_index]['balance'] - amount
                    new_account = {"id": destination_id, "balance": amount}
                    accounts_db.append(new_account)
                    response_body['origin'] = accounts_db[orig_index]
                    response_body['destination'] = new_account
                    return response_body, 201
            else:
                return 0,404



    
    