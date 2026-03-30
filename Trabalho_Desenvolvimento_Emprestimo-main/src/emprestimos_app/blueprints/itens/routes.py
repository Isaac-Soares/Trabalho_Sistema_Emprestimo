from flask import Blueprint, request, jsonify
from src.emprestimos_app.models import db, Item

itens_bp = Blueprint('itens', __name__, url_prefix='/itens')

@itens_bp.route('', methods=['POST'])
def criar():
    data = request.json
    item = Item(
        nome=data['nome'],
        descricao=data.get('descricao'),
        categoria_id=data['categoria_id']
    )
    db.session.add(item)
    db.session.commit()
    return {"msg": "Item criado"}

@itens_bp.route('', methods=['GET'])
def listar():
    itens = Item.query.all()
    return jsonify([
        {
            "id": i.id,
            "nome": i.nome,
            "disponivel": i.disponivel
        } for i in itens
    ])

@itens_bp.route('/<int:id>', methods=['PUT'])
def atualizar(id):
    item = Item.query.get_or_404(id)
    data = request.json

    item.nome = data.get('nome', item.nome)
    item.descricao = data.get('descricao', item.descricao)

    db.session.commit()
    return {"msg": "Atualizado"}

@itens_bp.route('/<int:id>', methods=['DELETE'])
def deletar(id):
    item = Item.query.get_or_404(id)

    if not item.disponivel:
        return {"erro": "Item emprestado"}, 400

    db.session.delete(item)
    db.session.commit()
    return {"msg": "Deletado"}