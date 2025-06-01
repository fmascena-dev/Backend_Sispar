# Armazenar as configurações do ambiente de desenvolvimento
from os import environ # Esse arquivo tem acesso as varíaveis de ambiente

class Config():
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')  # Puxa a variável e utiliza para a conexão
    SQLALCHEMY_TRACK_MODIFICATIONS=False # OTIMIZA as querys no banco de dados
    SECRET_KEY = environ.get('SECRET_KEY')
    FRONTEND_URL = environ.get('FRONTEND_URL', 'http://localhost:3000')