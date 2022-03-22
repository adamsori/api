# API
Essa é uma API simples feita em python3, flask_restx, sqlalchemy e mysql

## SETUP
É necessário o package manager [pip3](https://pip.pypa.io/en/stable/) para concluir a instalação.

Instalar python-venv
```bash
sudo apt install python3.8-venv
```
Criar ambiente virtual para o projeto (executar dentro do diretório onde o repositório foi clonado)
```bash
python3 -m venv venv
```
Ativar o ambiente virtual
```bash
source venv/bin/activate
```
Instalar os módulos necessários (requirements.txt)
```bash
pip3 install -r requirements.txt
```
Criar uma variável de ambiente dizendo qual é o nosso aplicativo FLASK 
```bash
export FLASK_APP=main.py
```
## EXECUÇÃO
Depois é só executar o app
```bash
python3 -m flask run
```