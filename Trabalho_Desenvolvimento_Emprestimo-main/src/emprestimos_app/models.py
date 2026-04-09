from datetime import datetime
from . import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    emprestimos = db.relationship('Emprestimo', backref='usuario', lazy=True)

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    itens = db.relationship('Item', backref='categoria', lazy=True)

class Item(db.Model):
    __tablename__ = 'itens'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    disponivel = db.Column(db.Boolean, default=True)

    categoria_id = db.Column(
    db.Integer,
    db.ForeignKey('categorias.id'),
    nullable=True
    )

    emprestimos = db.relationship('Emprestimo', backref='item', lazy=True)

class Emprestimo(db.Model):
    __tablename__ = 'emprestimos'

    id = db.Column(db.Integer, primary_key=True)
    data_emprestimo = db.Column(db.DateTime, default=datetime.utcnow)
    data_devolucao = db.Column(db.DateTime, nullable=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('itens.id'), nullable=False)