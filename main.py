''' 
from flask import Flask
# instanciar um app que vem do objeto flask, chamando o mesmo arquivo passando __name__
app = Flask(__name__)

# decorator do app com uma rota
@app.route('/')
def hello_world():
    return "Hello World."
'''

from src.server.instance import server 
# IMPORTAR OS CONTROLLERS (CLASSES)
from src.controllers.transaction import *

server.run()
