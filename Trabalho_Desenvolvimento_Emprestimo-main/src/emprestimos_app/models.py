from flask_sqlalchemy import SQLAlchemy
from . import db
from datetime import datetime

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    emprestimos = db.relationship('Emprestimo', backref='usuario', lazy=True)


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    itens = db.relationship('Item', backref='categoria', lazy=True)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    disponivel = db.Column(db.Boolean, default=True)

    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)


class Emprestimo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    data_emprestimo = db.Column(db.DateTime, default=datetime.utcnow)
    data_devolucao = db.Column(db.DateTime, nullable=True)

    item = db.relationship('Item')