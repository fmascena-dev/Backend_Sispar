# Responsável pela criação da aplicação
from flask import Flask
from src.controller.colaborador_controller import bp_colaborador
from src.model import db
from config import Config
from flasgger import Swagger

swagger_config = {
    "headers": [],
    "specs": [{
        "endpoint": "apispec",
        "route": "/apispec.json/",
        "rule_filter": lambda rule: True, # Todas as rotas/endpoints serão documentados
        "model_filter": lambda rule: True, # Especificar quais modelos da entidade serão documentados
    }],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}

# Create_app() -> Vai configurar a instância do Flask
def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp_colaborador)
    
    app.config.from_object(Config)
    
    db.init_app(app)
    
    Swagger(app, config=swagger_config)
    
    with app.app_context():
        db.create_all()
    
    return app