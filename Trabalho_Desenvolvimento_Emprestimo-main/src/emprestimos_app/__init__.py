import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    app.secret_key = os.getenv('SECRET_KEY', 'dev')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .models import Usuario, Item, Emprestimo, Categoria

    from src.emprestimos_app.blueprints.usuarios.routes import usuarios_bp
    from src.emprestimos_app.blueprints.itens.routes import itens_bp
    from src.emprestimos_app.blueprints.categorias.routes import categorias_bp
    from src.emprestimos_app.blueprints.operacoes.routes import operacoes_bp

    app.register_blueprint(usuarios_bp)
    app.register_blueprint(itens_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(operacoes_bp)

    @app.route('/')
    def home():
        return render_template('home.html')

    return app