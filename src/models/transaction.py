from flask_sqlalchemy import SQLAlchemy
from src.server.instance import server

app = server.app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://remoteuser:passwd@localhost/user_account'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class UserBalance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer)

    def __init__(self, id=None, balance=None):
        self.id = id
        self.balance = balance

    def get(self, account_id):
        account = UserBalance.query.filter_by(id=account_id).first()
        return account.balance

    def create(self, account_id, balance):
        new_account = UserBalance(account_id, balance)
        db.session.add(new_account)
        db.session.commit()
