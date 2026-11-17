from flask import Blueprint, flash, render_template, request, redirect, url_for
from services.joia_service import (create_joia, get_joias, get_joia_by_id, update_joia, delete_joia,
                                   CATEGORIAS, TIPOS_PRATA)
from .auth_decorator import login_required

joia_bp = Blueprint('joia', __name__, url_prefix='/joias', template_folder='templates')


def _dados_do_formulario():
    f = request.form
    return dict(
        codigo=f.get('codigo', ''),
        nome=f.get('nome', ''),
        categoria=f.get('categoria', ''),
        tipo_prata=f.get('tipo_prata', ''),
        preco=f.get('preco', ''),
        estoque=f.get('estoque', ''),
        peso_gramas=f.get('peso_gramas', ''),
        tamanho=f.get('tamanho', ''),
        descricao=f.get('descricao', ''),
        imagem_url=f.get('imagem_url', ''),
    )


# READ (catálogo livre, qualquer visitante pode ver)
@joia_bp.route('/', methods=['GET'])
def listar_joias():
    busca = request.args.get('busca', '')
    categoria = request.args.get('categoria', '')
    joias = get_joias(busca, categoria)
    return render_template('joias_lista.html', joias=joias, categorias=CATEGORIAS,
                           busca=busca, categoria_atual=categoria)


@joia_bp.route('/<int:joia_id>', methods=['GET'])
def detalhe_joia(joia_id):
    joia = get_joia_by_id(joia_id)
    if not joia:
        flash("Joia não encontrada.", "danger")
        return redirect(url_for('joia.listar_joias'))
    return render_template('joia_detalhe.html', joia=joia)


# CREATE
@joia_bp.route('/cadastro', methods=['GET', 'POST'])
@login_required
def cadastrar_joia():
    if request.method == 'POST':
        dados = _dados_do_formulario()
        try:
            joia = create_joia(**dados)
            flash("Joia cadastrada com sucesso!", "success")
            return redirect(url_for('joia.detalhe_joia', joia_id=joia.id))
        except ValueError as e:
            flash(str(e), "danger")
            return render_template('joia_form.html', joia=dados, categorias=CATEGORIAS,
                                   tipos_prata=TIPOS_PRATA, modo='cadastro')

    return render_template('joia_form.html', joia=None, categorias=CATEGORIAS,
                           tipos_prata=TIPOS_PRATA, modo='cadastro')


# UPDATE
@joia_bp.route('/editar/<int:joia_id>', methods=['GET', 'POST'])
@login_required
def editar_joia(joia_id):
    joia = get_joia_by_id(joia_id)
    if not joia:
        flash("Joia não encontrada.", "danger")
        return redirect(url_for('joia.listar_joias'))

    if request.method == 'POST':
        dados = _dados_do_formulario()
        try:
            update_joia(joia_id, **dados)
            flash("Joia atualizada com sucesso!", "success")
            return redirect(url_for('joia.detalhe_joia', joia_id=joia_id))
        except ValueError as e:
            flash(str(e), "danger")
            return render_template('joia_form.html', joia=dados, joia_id=joia_id, categorias=CATEGORIAS,
                                   tipos_prata=TIPOS_PRATA, modo='edicao')

    return render_template('joia_form.html', joia=joia, joia_id=joia_id, categorias=CATEGORIAS,
                           tipos_prata=TIPOS_PRATA, modo='edicao')


# DELETE
@joia_bp.route('/deletar/<int:joia_id>', methods=['POST'])
@login_required
def deletar_joia(joia_id):
    try:
        delete_joia(joia_id)
        flash("Joia removida com sucesso.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for('joia.listar_joias'))
