from flask import request 
from model.Account import *
from response import *

account = Account()
# Truncate na tabela simple-api
@app.route('/reset', methods=['POST'])
def api_reset():
    account.reset()
    return response(200,'OK')

# Seleciona balance de uma determinada conta
@app.route('/balance', methods=['GET'])
def get_balance():
        # Seleciona a conta com o id = account_id
        account_obj = account.read(request.args.get('account_id'))
        # Se a conta não existir, retorna 404 0
        if account_obj is None:
            return response(404, '0')
        # Se a conta existir, retorna 200 balance
        return response(200, str(account_obj.balance))

# Trata eventos 'deposit', 'withdraw' e 'transfer'
@app.route('/event', methods=['POST'])
def eventos():
        # Verifica se o body da requisição é do tipo json
        if request.is_json:
            request_type = request.json.get('type')
            destination = request.json.get('destination')
            amount = request.json.get('amount')
            if request_type == 'transfer' or request_type == 'withdraw':
                origin = request.json.get('origin')

        # Verifica se request_type é do tipo deposit
        if request_type == 'deposit':
            # Seleciona no banco a conta que recebera o deposito
            account_obj = account.read(destination)
            # Caso a conta não exista, uma nova conta é criada com o balance recebendo o amount
            if account_obj is None:
                account_obj = account.create(destination, amount)
                return response_json(201, 'destination', account_obj.to_json())
            # Caso a conta exista, então o novo saldo é a soma do balance com o amount
            else:
                account_obj.update(amount)
                return response_json(201, 'destination', account_obj.to_json())

        # Verifica se request_type é do tipo withdraw
        elif request_type == 'withdraw':
            # Seleciona no banco a conta em que o saque será realizado
            account_obj = account.read(origin)
            # Se a conta não existir, retorna 404 0
            if account_obj is None:
                return response(404, '0')
            # Caso a conta exista, então o novo saldo é a subtração do balance com o amount
            # Necessario verificar se o saldo existente é maior que o que sera sacado [to do]
            else:
                account_obj.update(-amount)
                return response_json(201, 'origin', account_obj.to_json())

        # Verifica se request_type é do tipo transfer
        elif request_type == 'transfer':
            # Seleciona no banco a conta em que o saque será realizado
            account_obj = account.read(origin)
            if account_obj is None:
                return response(404, '0')
            else:
                # Remove o valor do balance da conta de origem
                account_obj.update(-amount)

                # Adiciona o valor removida da conta de origem no balance da conta de destino
                account_dest_obj = account.read(destination)
                if account_dest_obj is None:
                    # caso o destino nao exista, cria-se um novo registro com id = destination e balance=amount
                    account_dest_obj = account.create(destination, amount)
                else:
                    account_dest_obj.update(amount)

                account_obj.id = str(account_obj.id)
                return response_transfer_json(201, account_obj.to_json(), account_dest_obj.to_json())