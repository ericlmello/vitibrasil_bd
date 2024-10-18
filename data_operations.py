# data_operations.py
from app import db
from models import CountryData

def add_country_data(country, import_value, export_value, production_value, commercialization_value, processing_value, year):
    new_data = CountryData(
        country=country,
        import_value=import_value,
        export_value=export_value,
        production_value=production_value,
        commercialization_value=commercialization_value,
        processing_value=processing_value,
        year=year
    )
    db.session.add(new_data)
    db.session.commit()

def get_country_data(country):
    return CountryData.query.filter_by(country=country).all()
