from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from ... import db
from ...models import Usuario, Item, Emprestimo

operacoes_bp = Blueprint('operacoes', __name__, url_prefix='/emprestimos')


@operacoes_bp.route('', methods=['GET'])
def listar_emprestimos():
    usuarios = Usuario.query.all()
    itens_disponiveis = Item.query.filter_by(disponivel=True).all()
    emprestimos_ativos = Emprestimo.query.filter_by(data_devolucao=None).all()

    return render_template(
        'operacoes/emprestimo_devolucao.html',
        usuarios=usuarios,
        itens_disponiveis=itens_disponiveis,
        emprestimos_ativos=emprestimos_ativos
    )


@operacoes_bp.route('/novo', methods=['POST'])
def emprestar():
    usuario_id = request.form['usuario_id']
    item_id = request.form['item_id']

    item = Item.query.get_or_404(item_id)

    if not item.disponivel:
        flash('Item indisponível para empréstimo.', 'erro')
        return redirect(url_for('operacoes.listar_emprestimos'))

    emprestimo = Emprestimo(
        usuario_id=usuario_id,
        item_id=item_id
    )

    item.disponivel = False

    db.session.add(emprestimo)
    db.session.commit()

    flash('Empréstimo realizado com sucesso!', 'sucesso')
    return redirect(url_for('operacoes.listar_emprestimos'))


@operacoes_bp.route('/devolver/<int:id>', methods=['POST'])
def devolver(id):
    emprestimo = Emprestimo.query.get_or_404(id)

    if emprestimo.data_devolucao:
        flash('Esse item já foi devolvido.', 'erro')
        return redirect(url_for('operacoes.listar_emprestimos'))

    emprestimo.data_devolucao = datetime.utcnow()
    emprestimo.item.disponivel = True

    db.session.commit()

    flash('Devolução registrada com sucesso!', 'sucesso')
    return redirect(url_for('operacoes.listar_emprestimos'))


@operacoes_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar_emprestimo(id):
    emprestimo = Emprestimo.query.get_or_404(id)

    if emprestimo.data_devolucao is None:
        flash('Não é possível remover um empréstimo ainda ativo.', 'erro')
        return redirect(url_for('operacoes.listar_emprestimos'))

    db.session.delete(emprestimo)
    db.session.commit()

    flash('Registro removido com sucesso!', 'sucesso')
    return redirect(url_for('operacoes.listar_emprestimos'))