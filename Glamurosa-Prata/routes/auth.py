from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from services.user_service import authenticate_user, get_user_by_email
from .auth_decorator import login_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')

@auth_bp.route('/submit-login', methods=['GET', 'POST'])
def submit_login():

    if request.method == 'POST':

        email = request.form['login']
        senha = request.form['senha']

        if not email or not senha:
            return "Por favor, preencha todos os campos."

        user = authenticate_user(email, senha)

        if not user:
            flash("Email ou senha inválidos.", "danger")
            return redirect(url_for('auth.login'))
            
        session.permanent = True # Define a sessão como permanente para que ela dure mesmo após o fechamento do navegador
        session['user_id'] = user.id
        session['user_nome'] = user.nome

        return redirect(url_for('user.meus_dados'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@auth_bp.route('/login')
def login():
    return render_template('login.html')
