from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from services.user_service import (create_user, get_user, get_user_by_id, get_user_by_email, update_user, delete_user)
from .auth_decorator import login_required

user_bp = Blueprint('user', __name__, url_prefix='/user', template_folder='templates')

@user_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone'] 
        senha = request.form['senha']

        try:
            user = create_user(nome, email, telefone, senha)
            return redirect(url_for('user.servicos'))
        except ValueError as e:
            return str(e)
        
    return render_template('cadastro.html')

@user_bp.route('/dados', methods=['GET'])
@login_required
def meus_dados():

    user_id = session['user_id']
    usuario = get_user_by_id(user_id)

    
    return render_template('dados.html', usuario=usuario)

@user_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return flash("Usuário não encontrado.", "alert-danger")
           

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone'] 
       
        try:
            update_user(user_id, nome, email, telefone)
            return redirect(url_for('user.meus_dados'))
        except ValueError as e:
            return str(e)

    return render_template('edit_user.html', usuario=user)


@user_bp.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def deletar_usuario(user_id):
    try:
        delete_user(user_id)

        session.clear()

        flash("Usuário deletado com sucesso.", "success")

        return redirect(url_for('auth.login'))

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for('user.meus_dados'))
    


@user_bp.route('/servicos')
@login_required
def servicos():
    return render_template('servicos.html') 

@user_bp.route('/configuracoes')
@login_required
def configuracoes():
    return render_template('configuracoes.html')

#rota livre
@user_bp.route('/contato')
def contato():
    return render_template('contato.html')   




