from flask import Blueprint, request, jsonify
from src.emprestimos_app.models import db, Categoria
from ... import db

categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias')

@categorias_bp.route('', methods=['POST'])
def criar():
    data = request.json
    categoria = Categoria(nome=data['nome'])
    db.session.add(categoria)
    db.session.commit()
    return {"msg": "Criado"}

@categorias_bp.route('', methods=['GET'])
def listar():
    categorias = Categoria.query.all()
    return jsonify([{"id": c.id, "nome": c.nome} for c in categorias])

@categorias_bp.route('/<int:id>', methods=['PUT'])
def atualizar(id):
    categoria = Categoria.query.get_or_404(id)
    categoria.nome = request.json['nome']
    db.session.commit()
    return {"msg": "Atualizado"}

@categorias_bp.route('/<int:id>', methods=['DELETE'])
def deletar(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    return {"msg": "Deletado"}