from flask import Flask, render_template, request, jsonify, send_file, abort
from flask_jwt_extended import JWTManager, jwt_required
import logging
from flasgger import Swagger
from config import Config
from download import download_file, read_csv_as_html_table
from auth import login
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from io import BytesIO
from utils import gerar_dimensao_pais
from extensions import db  # Usando o db do extensions.py

from models import CountryData
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
jwt = JWTManager(app)
swagger = Swagger(app)
#db = SQLAlchemy(app)
db.init_app(app)

# Função para gerar e salvar o gráfico com dados do banco de dados
def generate_plot():
    # Consultar dados do banco de dados
    data = CountryData.query.all()
    if not data:
        logging.error("Nenhum dado encontrado para gerar o gráfico.")
        abort(404, description="Dados não encontrados.")

    # Converter os dados em um DataFrame
    df = pd.DataFrame([{
        'País': d.country,
        'Tipo': 'Importação',
        d.year: d.import_value
    } for d in data] + [{
        'País': d.country,
        'Tipo': 'Exportação',
        d.year: d.export_value
    } for d in data] + [{
        'País': d.country,
        'Tipo': 'Produção',
        d.year: d.production_value
    } for d in data] + [{
        'País': d.country,
        'Tipo': 'Comercialização',
        d.year: d.commercialization_value
    } for d in data] + [{
        'País': d.country,
        'Tipo': 'Processamento',
        d.year: d.processing_value
    } for d in data])

    # Filtrar para os 10 principais países em importação no último ano
    ultimo_ano = max(df.columns[df.columns.str.isdigit()])
    df_importacao = df[df['Tipo'] == 'Importação'].sort_values(by=ultimo_ano, ascending=False)
    top_paises_importacao = df_importacao['País'].head(10)
    df_filtered = df[df['País'].isin(top_paises_importacao)]

    # Criar o gráfico
    plt.figure(figsize=(12, 6))
    sns.barplot(x='País', y=ultimo_ano, hue='Tipo', data=df_filtered, order=top_paises_importacao)
    plt.xticks(rotation=45, ha='right')
    plt.title(f'Comparação de Importação e Exportação - Top 10 Países ({ultimo_ano})')
    plt.yscale('log')
    plt.xlabel('País')
    plt.ylabel('Quantidade (Kg) [escala logarítmica]')
    plt.legend(loc='upper right')
    plt.tight_layout()

    # Salvar o gráfico em memória e retornar
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

@app.route('/analises', methods=['GET'])
def analises():
    """
    Visualizar gráfico de análise de dados
    ---
    tags:
      - Analises
    responses:
      200:
        description: Gráfico gerado com sucesso
    """
    return generate_plot()

# Função para download do arquivo de dimensão País
@app.route('/download/dimensao_pais', methods=['GET'])
def download_dimensao_pais():
    try:
        csv_content = gerar_dimensao_pais()
        return send_file(csv_content, as_attachment=True, download_name='dimensao_pais.csv', mimetype='text/csv')
    except Exception as e:
        logging.error(f"Erro ao enviar o arquivo: {e}")
        abort(500, description="Erro ao enviar o arquivo.")

# Endpoint para visualizar o arquivo CSV como tabela HTML
@app.route('/view_csv/<file_type>', methods=['GET'])
@jwt_required()
def view_csv(file_type):
    """
    Visualizar arquivo CSV como tabela HTML
    ---
    tags:
      - Files
    parameters:
      - name: file_type
        in: path
        type: string
        required: true
        description: Tipo de arquivo CSV a ser visualizado
    responses:
      200:
        description: Tabela HTML com os dados do arquivo CSV
      404:
        description: Arquivo não encontrado
    """
    table_html = read_csv_as_html_table(file_type)
    if table_html:
        return jsonify({'table_html': table_html}), 200
    return jsonify({"msg": "Arquivo não encontrado"}), 404

# Endpoint de login
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        return login()
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=False)
