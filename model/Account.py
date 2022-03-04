# Flask: própria classe Flask | Response: para criar o retorno da API | request: tratar body enviado pelo cliente
from flask import Flask, Response, request 
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from env import mysql_connection

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_connection # mysql://user:passwd@host/database

# Passar a instância do flask para trabalhar juntamente com o DB
db = SQLAlchemy(app)
# para criar a tabela apenas uma vez, basta, via linha de comando, importar o db do app (from app import db) e executar db.create_all()

# CRUD
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer)

    def to_json(self):
        return {'id': self.id, 'balance': self.balance}

    def create(self, account_id, amount):
        account = Account(id=account_id, balance=amount)
        db.session.add(account)
        db.session.commit()
        account.id = str(account.id)
        return account
    
    def read(self, account_id):
        account_obj = Account.query.filter_by(id=account_id).first()
        return account_obj

    def delete(self):
        pass

    def update(self, amount):
        self.balance = self.balance + amount
        db.session.commit()
        self.id = str(self.id)
        return self

    def reset(self):
        print('PASSEI POR AQUI')
        try:
            db.session.query(Account).delete()
            db.session.commit()
        except:
            db.session.rollback()
        pass

