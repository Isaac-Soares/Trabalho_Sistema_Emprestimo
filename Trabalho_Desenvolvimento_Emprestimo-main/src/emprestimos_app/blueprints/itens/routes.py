from flask import Blueprint, render_template, request, redirect, url_for, flash
from ... import db
from ...models import Item, Categoria

itens_bp = Blueprint('itens', __name__, url_prefix='/itens')


@itens_bp.route('', methods=['GET'])
def listar_itens():
    itens = Item.query.all()
    categorias = Categoria.query.all()

    return render_template(
        'itens/itens.html',
        itens=itens,
        categorias=categorias
    )


@itens_bp.route('/novo', methods=['POST'])
def criar_item():
    nome = request.form['nome']
    descricao = request.form['descricao']
    categoria_id = request.form['categoria_id']

    item = Item(
        nome=nome,
        descricao=descricao,
        categoria_id=categoria_id,
        disponivel=True
    )

    db.session.add(item)
    db.session.commit()

    flash('Item criado com sucesso!', 'sucesso')
    return redirect(url_for('itens.listar_itens'))


@itens_bp.route('/editar/<int:id>', methods=['POST'])
def atualizar_item(id):
    item = Item.query.get_or_404(id)

    item.nome = request.form['nome']
    item.descricao = request.form['descricao']
    item.categoria_id = request.form['categoria_id']

    db.session.commit()
    flash('Item atualizado com sucesso!', 'sucesso')
    return redirect(url_for('itens.listar_itens'))


@itens_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar_item(id):
    item = Item.query.get_or_404(id)

    if not item.disponivel:
        flash('Não é possível excluir: item está emprestado.', 'erro')
        return redirect(url_for('itens.listar_itens'))

    db.session.delete(item)
    db.session.commit()

    flash('Item deletado com sucesso!', 'sucesso')
    return redirect(url_for('itens.listar_itens'))