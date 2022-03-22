from flask import Flask
from flask_restx import Api

class Server():
    def __init__(self):
        self.app = Flask(__name__,template_folder="templates")
        self.api = Api(self.app,
            version='1.0',
            title='Simple API',
            description='A Simple API',
            doc='/docs'
        )
    
    def run(self,):
        self.app.run(
            # Para desenvolvimento usamos debug True, para deploy é False
            debug=True
        )


server = Server()
