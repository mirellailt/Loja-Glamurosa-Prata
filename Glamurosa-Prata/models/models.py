from datetime import datetime
from sqlalchemy import String, Integer, Column, Float, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

db = SQLAlchemy(model_class=Base)

def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=True)
    senha = db.Column(db.String(100), nullable=False)


class Joia(db.Model):
    __tablename__ = 'joias'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(30), nullable=False, unique=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(30), nullable=False)
    tipo_prata = db.Column(db.String(30), nullable=False, default='Prata 925')
    peso_gramas = db.Column(db.Float, nullable=True)
    tamanho = db.Column(db.String(30), nullable=True)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False, default=0)
    descricao = db.Column(db.String(500), nullable=True)
    imagem_url = db.Column(db.String(300), nullable=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.now)
