import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv
load_dotenv()
import config
import uuid
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from data_model import DataModel
import datetime

def get_connection():
    engine = create_engine(config.db_url)
    Session = sessionmaker(bind = engine)
    session = Session()

    return session


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

    if(response.status_code != 200): return False

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


def save_data_db(data, session):
    for d in data:
        result = session.query(DataModel).filter_by(mes=d['mes'], ano = d['ano']).first()       

        if(result == None):
            event = DataModel(id = str(uuid.uuid4()), 
                ano = d['ano'], 
                bandeira = d['bandeira'], 
                mes = d['mes'], 
                numero_mes = d['numero_mes'], 
                valor = d['valor'], 
                created_at = datetime.datetime.now())

            session.add(event)
            session.commit()


def get_data_db(session):
    result = session.query(DataModel).order_by(DataModel.ano.desc()).order_by(DataModel.numero_mes.desc())

    data = []

    for r in result:
        data.append({
            "ano" : r.ano,
            "bandeira" : r.bandeira,
            "mes" : r.mes,
            "valor" : r.valor           
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
    session = get_connection()
    data = get_data()
    save_data_db(data, session)
    data_db = get_data_db(session)
    return jsonify(data_db)

if __name__ == "__main__":    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    