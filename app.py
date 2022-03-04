# Flask: própria classe Flask | Response: para criar o retorno da API | request: tratar body enviado pelo cliente
from controller.Account import *

# para criar a tabela apenas uma vez, basta, via linha de comando, importar o db do app (from app import db) e executar db.create_all()
app.run(host="0.0.0.0")

