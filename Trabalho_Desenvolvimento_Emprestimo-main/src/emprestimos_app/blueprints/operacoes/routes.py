from flask import Blueprint, request, jsonify
from src.emprestimos_app.models import db, Emprestimo, Item

from datetime import datetime

operacoes_bp = Blueprint('operacoes', __name__, url_prefix='/emprestimos')

@operacoes_bp.route('', methods=['POST'])
def emprestar():
    data = request.json

    item = Item.query.get(data['item_id'])

    if not item or not item.disponivel:
        return {"erro": "Item indisponível"}, 400

    emprestimo = Emprestimo(
        usuario_id=data['usuario_id'],
        item_id=data['item_id']
    )

    item.disponivel = False

    db.session.add(emprestimo)
    db.session.commit()

    return {"msg": "Empréstimo realizado"}

@operacoes_bp.route('', methods=['GET'])
def listar():
    emprestimos = Emprestimo.query.all()
    return jsonify([
        {
            "id": e.id,
            "usuario_id": e.usuario_id,
            "item_id": e.item_id,
            "devolvido": e.data_devolucao is not None
        } for e in emprestimos
    ])

@operacoes_bp.route('/<int:id>/devolver', methods=['POST'])
def devolver(id):
    data = request.json
    emprestimo = Emprestimo.query.get_or_404(id)

    # ✅ REGRA IMPORTANTE
    if emprestimo.usuario_id != data['usuario_id']:
        return {"erro": "Apenas quem emprestou pode devolver"}, 403

    if emprestimo.data_devolucao:
        return {"erro": "Já devolvido"}, 400

    emprestimo.data_devolucao = datetime.utcnow()
    emprestimo.item.disponivel = True

    db.session.commit()
    return {"msg": "Devolvido com sucesso"}

@operacoes_bp.route('/<int:id>', methods=['DELETE'])
def deletar(id):
    emprestimo = Emprestimo.query.get_or_404(id)
    db.session.delete(emprestimo)
    db.session.commit()
    return {"msg": "Removido"}