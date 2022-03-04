# Flask: própria classe Flask | Response: para criar o retorno da API | request: tratar body enviado pelo cliente
from flask import Flask, Response, request 
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json
from env import mysql_connection

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_connection

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

# Selecionar Tudo
@app.route('/accounts', methods=['GET'])
def seleciona_accounts():
    accounts_objs = Account.query.all()
    accounts_json = [account.to_json() for account in accounts_objs]
    
    # precisa dar um dump do json antes de enviar a resposta
    return Response(json.dumps(accounts_json))

app.run(host="0.0.0.0")

