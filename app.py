# Flask: própria classe Flask | Response: para criar o retorno da API | request: tratar body enviado pelo cliente
from flask import Flask, Response, request 
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json
from env import mysql_connection

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_connection # mysql://user:passwd@host/database

# Passar a instância do flask para trabalhar juntamente com o DB
db = SQLAlchemy(app)

# CRUD
# Definindo as tabelas com SQLAlchemy
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer)

    def to_json(self):
        return {'id': self.id, 'balance': self.balance}

# para criar a tabela apenas uma vez, basta, via linha de comando, importar o db do app (from app import db) e executar db.create_all()

# Selecionar Todas as Accounts (Rota criada para testes)
@app.route('/accounts', methods=['GET'])
def seleciona_accounts():
    accounts_objs = Account.query.all()
    accounts_json = [account.to_json() for account in accounts_objs]
    
    # precisa dar um dump do json antes de enviar a resposta
    return gera_response_json(200, 'accounts', accounts_json)

# Truncate na tabela simple-api
@app.route('/reset', methods=['POST'])
def api_reset():
    try:
        db.session.query(Account).delete()
        db.session.commit()
    except:
        db.session.rollback()
    return gera_response_simples(200,'OK')

# Seleciona balance de uma determinada conta
@app.route('/balance', methods=['GET'])
def get_balance():
        # Seleciona a conta com o id = account_id
        account_obj = Account.query.filter_by(id=request.args.get('account_id')).first()
        # Se a conta não existir, retorna 404 0
        if account_obj is None:
            return gera_response_simples(404, '0')
        # Se a conta existir, retorna 200 balance
        return gera_response_simples(200, str(account_obj.balance))

# Trata eventos 'deposit', 'transfer
@app.route('/event', methods=['POST'])
def eventos():
        # Verifica se o body da requisição é do tipo json
        if request.is_json:
            request_type = request.json.get('type')
            destination = request.json.get('destination')
            amount = request.json.get('amount')
            if request_type == 'transfer':
                origin = request.json.get('origin')

        # Verifica se request_type é do tipo deposit
        if request_type == 'deposit':
            # Seleciona no banco a conta que recebera o deposito
            account_obj = Account.query.filter_by(id=destination).first()
            # Caso a conta não exista, uma nova conta é criada com o balance recebendo o amount
            if account_obj is None:
                account = Account(id=destination, balance=amount)
                db.session.add(account)
                db.session.commit()
                account.id = str(account.id)
   
                return gera_response_json(201, 'destination', account.to_json())
            # Caso a conta exista, então o novo saldo é a soma do balance com o amount
            else:
                account_obj.balance = account_obj.balance + amount
                db.session.commit()
                account_obj.id = str(account_obj.id)
            
                return gera_response_json(201, 'destination', account_obj.to_json())


        







def gera_response_json(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo
    
    if(mensagem):
        body['mensagem'] = mensagem
    return Response(json.dumps(body), status=status, mimetype='application/json')

def gera_response_simples(status, conteudo):
    return Response(conteudo, status=status)



app.run(host="0.0.0.0")

