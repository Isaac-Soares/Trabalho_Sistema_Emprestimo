from flask import Blueprint, render_template, request, redirect, url_for, flash
from ... import db
from ...models import Categoria

categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias')


@categorias_bp.route('', methods=['GET'])
def listar_categorias():
    categorias = Categoria.query.all()
    return render_template('categorias/categorias.html', categorias=categorias)


@categorias_bp.route('/novo', methods=['POST'])
def criar_categoria():
    nome = request.form['nome']

    categoria = Categoria(nome=nome)
    db.session.add(categoria)
    db.session.commit()

    flash('Categoria criada com sucesso!', 'sucesso')
    return redirect(url_for('categorias.listar_categorias'))


@categorias_bp.route('/editar/<int:id>', methods=['POST'])
def atualizar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    categoria.nome = request.form['nome']

    db.session.commit()
    flash('Categoria atualizada com sucesso!', 'sucesso')
    return redirect(url_for('categorias.listar_categorias'))


@categorias_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar_categoria(id):
    categoria = Categoria.query.get_or_404(id)

    if categoria.itens:
        flash('Não é possível excluir: categoria possui itens cadastrados.', 'erro')
        return redirect(url_for('categorias.listar_categorias'))

    db.session.delete(categoria)
    db.session.commit()

    flash('Categoria deletada com sucesso!', 'sucesso')
    return redirect(url_for('categorias.listar_categorias'))