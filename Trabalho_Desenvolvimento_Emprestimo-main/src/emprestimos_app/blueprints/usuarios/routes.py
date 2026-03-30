from flask import Blueprint, request, jsonify
from src.emprestimos_app.models import db,  Usuario
from ... import db

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route('', methods=['POST'])
def criar_usuario():
    data = request.json
    if Usuario.query.filter_by(email=data['email']).first():
        return {"erro": "Email já cadastrado"}, 400

    usuario = Usuario(nome=data['nome'], email=data['email'])
    db.session.add(usuario)
    db.session.commit()
    return {"msg": "Usuário criado"}

@usuarios_bp.route('', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{"id": u.id, "nome": u.nome, "email": u.email} for u in usuarios])

@usuarios_bp.route('/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    data = request.json

    usuario.nome = data.get('nome', usuario.nome)
    usuario.email = data.get('email', usuario.email)

    db.session.commit()
    return {"msg": "Atualizado"}

@usuarios_bp.route('/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if usuario.emprestimos:
        return {"erro": "Usuário possui empréstimos"}, 400

    db.session.delete(usuario)
    db.session.commit()
    return {"msg": "Deletado"}