import json
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

usuario = requests.get('https://sic.cercos.com.br/sic/bandeiras_tarifarias/', verify=False)

conteudo = BeautifulSoup(usuario.text, 'html.parser')

dados = []

for i in range(1,13):
    id_cor = f'id_sc_field_bandeira_{i}'    
    id_valor = f'id_sc_field_valor_{i}'    
    id_mes = f'id_sc_field_mes_{i}'    
    id_ano = f'id_sc_field_ano_{i}'   

    dados.append({
        "cor" : conteudo.find(id=id_cor).get_text(),
        "valor" : conteudo.find(id=id_valor).get_text(),
        "mes" : conteudo.find(id=id_mes).get_text(),
        "ano" : conteudo.find(id=id_ano).get_text(),  
    })

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify(dados)

app.run()