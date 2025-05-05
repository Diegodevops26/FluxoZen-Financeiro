from flask import Flask
from extensions import db
import os
from flask_migrate import Migrate  # Importe Migrate

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'financeiro.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)  # Inicialize o Migrate com a aplicação e o db

from models import Categoria, Transacao
from routes import transacoes_bp, categorias_bp, relatorios_bp

app.register_blueprint(transacoes_bp, url_prefix='/transacoes')
app.register_blueprint(categorias_bp, url_prefix='/categorias')
app.register_blueprint(relatorios_bp, url_prefix='/relatorios')

# A remoção do db.create_all() aqui é recomendada quando se usa migrations

if __name__ == '__main__':
    app.run(debug=True)