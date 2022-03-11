from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class DataModel(db.Model):
    __tablename__ = 'dados_bandeira'
 
    id = db.Column(db.String(), primary_key = True)
    ano = db.Column(db.String())
    bandeira = db.Column(db.String())
    mes = db.Column(db.String())
    numero_mes = db.Column(db.Integer())
    valor = db.Column(db.String())   
    created_at = db.Column(db.DateTime()) 
    
    def __repr__(self):
        return "<DataModel(id='%s', ano='%s', bandeira='%s', mes='%s', numero_mes='%s', valor='%s', created_at='%s')>" % (
                                self.id, self.ano, self.bandeira, self.mes, self.numero_mes, self.valor, self.created_at)
