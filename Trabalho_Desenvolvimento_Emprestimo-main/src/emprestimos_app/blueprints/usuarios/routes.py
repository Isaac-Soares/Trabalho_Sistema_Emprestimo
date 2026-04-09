from flask import Blueprint, render_template, request, redirect, url_for, flash
from ... import db
from ...models import Usuario

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')


@usuarios_bp.route('', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/usuarios.html', usuarios=usuarios)


@usuarios_bp.route('/novo', methods=['POST'])
def criar_usuario():
    nome = request.form['nome']
    email = request.form['email']

    if Usuario.query.filter_by(email=email).first():
        flash('Email já cadastrado!', 'erro')
        return redirect(url_for('usuarios.listar_usuarios'))

    usuario = Usuario(nome=nome, email=email)
    db.session.add(usuario)
    db.session.commit()

    flash('Usuário criado com sucesso!', 'sucesso')
    return redirect(url_for('usuarios.listar_usuarios'))


@usuarios_bp.route('/editar/<int:id>', methods=['POST'])
def atualizar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    usuario.nome = request.form['nome']
    usuario.email = request.form['email']

    db.session.commit()
    flash('Usuário atualizado com sucesso!', 'sucesso')
    return redirect(url_for('usuarios.listar_usuarios'))


@usuarios_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if usuario.emprestimos:
        flash('Usuário possui empréstimos e não pode ser excluído.', 'erro')
        return redirect(url_for('usuarios.listar_usuarios'))

    db.session.delete(usuario)
    db.session.commit()

    flash('Usuário deletado com sucesso!', 'sucesso')
    return redirect(url_for('usuarios.listar_usuarios'))