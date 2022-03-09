import json
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv
load_dotenv()
import config
import mysql.connector
import uuid

def get_connection():
    cnct = mysql.connector.connect(host=config.db_host, user=config.db_user, port=int(config.db_port), password=config.db_password, database=config.db_database)
    cursor = cnct.cursor()

    return cnct, cursor


def get_number_month(month):
    months = {
        "Janeiro": 1,
        "Fevereiro": 2,
        "Março": 3,
        "Abril": 4,
        "Maio": 5,
        "Junho": 6,
        "Julho": 7,
        "Agosto": 8,
        "Setembro": 9,
        "Outubro": 10,
        "Novembro": 11,
        "Dezembro": 12,
    }

    return months.get(month, 0)


def get_data():
    response = requests.get(config.url_source, verify=False)
    content = BeautifulSoup(response.text, 'html.parser')
    data = []

    for i in range(1,13):
        id_cor = f'id_sc_field_bandeira_{i}'    
        id_valor = f'id_sc_field_valor_{i}'    
        id_mes = f'id_sc_field_mes_{i}'    
        id_ano = f'id_sc_field_ano_{i}'   

        data.append({
            "id" : str(uuid.uuid4()),
            "bandeira" : content.find(id=id_cor).get_text(),
            "valor" : content.find(id=id_valor).get_text(),
            "mes" : content.find(id=id_mes).get_text(),
            "numero_mes" : get_number_month(content.find(id=id_mes).get_text()),
            "ano" : content.find(id=id_ano).get_text(),  
        })

    return data


def save_data_db(data, cnct, cursor):
    for d in data:        
        sql_query = """SELECT 1 FROM dados_bandeira WHERE ano=%(ano)s AND mes=%(mes)s"""
        cursor.execute(sql_query, d)
        response = cursor.fetchall()

        if(response == []):
            sql_query = """INSERT INTO dados_bandeira (id, ano, bandeira, mes, numero_mes, valor) VALUES (%(id)s, %(ano)s, %(bandeira)s, %(mes)s, %(numero_mes)s, %(valor)s)"""
            cursor.execute(sql_query, d)
            cnct.commit()


def get_data_db(cnct, cursor):
    data = []

    sql_query = """SELECT ano, bandeira, mes, valor FROM dados_bandeira ORDER BY ano desc, numero_mes desc"""
    cursor.execute(sql_query)
    response = cursor.fetchall()

    for d in response:
        data.append({
            "ano" : d[0],
            "bandeira" : d[1],
            "mes" : d[2],
            "valor":  d[3]           
        })

    return data


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_pyfile('config.py')
app.debug = config.debug_mode

@app.route('/')
@cross_origin()
def index():
    cnct, cursor = get_connection()
    data = get_data()
    save_data_db(data, cnct, cursor)
    data_db = get_data_db(cnct, cursor)
    return jsonify(data_db)

if __name__ == "__main__":    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    