# models.py

from extensions import db

class CountryData(db.Model):
    __tablename__ = 'country_data'
    
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String, nullable=False)
    import_value = db.Column(db.Float)
    export_value = db.Column(db.Float)
    production_value = db.Column(db.Float)
    commercialization_value = db.Column(db.Float)
    processing_value = db.Column(db.Float)
    year = db.Column(db.Integer, nullable=False)

class Arquivo(db.Model):
    __tablename__ = 'arquivos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False, unique=True)
    conteudo = db.Column(db.LargeBinary, nullable=False)  # Armazena o conteúdo do arquivo CSV
    data_upload = db.Column(db.DateTime, default=db.func.current_timestamp())  # Opcional: data do upload
