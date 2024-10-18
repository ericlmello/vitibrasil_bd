# create_tables.py
from app import app, db
from models import CountryData

with app.app_context():
    db.create_all()
    print("Tabelas criadas com sucesso.")
