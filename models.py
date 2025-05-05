from datetime import datetime
from extensions import db  # Importe db de extensions.py

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    transacoes = db.relationship('Transacao', backref='categoria', lazy=True)
    orcamento = db.Column(db.Float)  # Adicionando um campo para orçamento

    def __repr__(self):
        return f'<Categoria {self.nome}>'

class Transacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(80), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tipo = db.Column(db.String(10), nullable=False)  # 'receita' ou 'despesa'
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

    def __repr__(self):
        return f'<Transacao {self.descricao} ({self.valor})>'