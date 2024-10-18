import os

class Config:
    JWT_SECRET_KEY = 'super-secret-key'

    # Lista de arquivos CSV para download
    FILES = [
        {'url': 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02', 'name': 'Producao.csv'},
        {'url': 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03', 'name': 'Processamento.csv'},
        {'url': 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04', 'name': 'Comercializacao.csv'},
        {'url': 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05', 'name': 'Importacao.csv'},
        {'url': 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06', 'name': 'Exportacao.csv'},
    ]

    # Configuração do banco de dados
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://vitibrasil_user:7uS3ssQ3DrDgazgLeZ66PzuYX94Mhfoq@dpg-cs82ui5umphs73fvedsg-a.oregon-postgres.render.com/vitibrasil')

    # Configuração SQLAlchemy
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False



