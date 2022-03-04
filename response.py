import json
from flask import Response 
def response_json(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo
    
    if(mensagem):
        body['mensagem'] = mensagem
    return Response(json.dumps(body), status=status, mimetype='application/json')

# função criada para receber dois parametros separados, origem e destino
def response_transfer_json(status, conteudo_origem, conteudo_destino, mensagem=False):
    body = {}
    body['origin'] = conteudo_origem
    body['destination'] = conteudo_destino
    
    if(mensagem):
        body['mensagem'] = mensagem
    return Response(json.dumps(body), status=status, mimetype='application/json')

# seria melhor criar um parametro na função gera_response_json para verificar o tipo de resposta (erro, normal ou transfer)
def response(status, conteudo):
    return Response(conteudo, status=status)
