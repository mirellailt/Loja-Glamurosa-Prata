from flask import flash
from models.models import Usuario, db

def create_user(nome: str, email: str, telefone: str, senha: str) -> Usuario:
    if not nome or not email or not telefone or not senha:
        raise ValueError("Por favor, preencha todos os campos.")
    
    existing_email_user = Usuario.query.filter_by(email=email).first()
    if existing_email_user:
        raise ValueError("Email já cadastrado.")
    
    user = Usuario(nome=nome, email=email, telefone=telefone, senha=senha)
    db.session.add(user)
    db.session.commit()
    return user

def get_user() -> list[Usuario]:
    return db.session.query(Usuario).limit(25).all()

def get_user_by_id(user_id: int) -> Usuario:
    return db.session.query(Usuario).filter_by(id=user_id).first()

def get_user_by_email(email: str) -> Usuario:
    return db.session.query(Usuario).filter_by(email=email).first()

def update_user(user_id: int, nome: str, email: str, telefone: str) -> Usuario:
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("Usuário não encontrado.")
    
    if not nome or not email or not telefone:
        raise ValueError("Por favor, preencha todos os campos.")
    
    existing_email_user = Usuario.query.filter_by(email=email).first()
    if existing_email_user and existing_email_user.id != user_id:
        raise ValueError("Email já cadastrado por outro usuário.")
    
    user.nome = nome
    user.email = email
    user.telefone = telefone
    db.session.commit()
    return user, flash("Dados atualizados com sucesso!", "success")

def delete_user(user_id: int) -> None:
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("Usuário não encontrado.")
    
    db.session.delete(user)
    db.session.commit()

def authenticate_user(email, senha):

    user = Usuario.query.filter_by(email=email).first()

    if not user:
        return None

    if user.senha != senha:
        flash("Email ou senha inválidos.", "danger")
        return None

    flash("Login realizado com sucesso!", "success")
    return user 