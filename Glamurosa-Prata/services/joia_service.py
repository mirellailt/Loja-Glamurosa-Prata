from models.models import Joia, db

CATEGORIAS = ["Anel", "Brinco", "Colar", "Pulseira", "Pingente", "Tornozeleira", "Conjunto", "Outro"]
TIPOS_PRATA = ["Prata 925", "Prata 950", "Prata 1000", "Prata Banhada"]


def _converter_numeros(preco, estoque, peso_gramas):
    try:
        preco = float(str(preco).replace(",", "."))
    except (TypeError, ValueError):
        raise ValueError("Preço inválido.")
    if preco < 0:
        raise ValueError("O preço não pode ser negativo.")

    try:
        estoque = int(estoque)
    except (TypeError, ValueError):
        raise ValueError("Estoque inválido.")
    if estoque < 0:
        raise ValueError("O estoque não pode ser negativo.")

    if peso_gramas in (None, ""):
        peso_gramas = None
    else:
        try:
            peso_gramas = float(str(peso_gramas).replace(",", "."))
        except ValueError:
            raise ValueError("Peso inválido.")
        if peso_gramas < 0:
            raise ValueError("O peso não pode ser negativo.")

    return preco, estoque, peso_gramas


def _validar_textos(codigo, nome, categoria, tipo_prata):
    if not codigo or not nome or not categoria or not tipo_prata:
        raise ValueError("Por favor, preencha todos os campos obrigatórios.")
    if categoria not in CATEGORIAS:
        raise ValueError("Categoria inválida.")
    if tipo_prata not in TIPOS_PRATA:
        raise ValueError("Tipo de prata inválido.")


def create_joia(codigo: str, nome: str, categoria: str, tipo_prata: str, preco, estoque,
                peso_gramas=None, tamanho: str = "", descricao: str = "", imagem_url: str = "") -> Joia:
    codigo = (codigo or "").strip().upper()
    nome = (nome or "").strip()
    _validar_textos(codigo, nome, categoria, tipo_prata)
    preco, estoque, peso_gramas = _converter_numeros(preco, estoque, peso_gramas)

    if Joia.query.filter_by(codigo=codigo).first():
        raise ValueError("Já existe uma joia com este código.")

    joia = Joia(codigo=codigo, nome=nome, categoria=categoria, tipo_prata=tipo_prata,
                preco=preco, estoque=estoque, peso_gramas=peso_gramas,
                tamanho=(tamanho or "").strip() or None,
                descricao=(descricao or "").strip() or None,
                imagem_url=(imagem_url or "").strip() or None)
    db.session.add(joia)
    db.session.commit()
    return joia


def get_joias(busca: str = "", categoria: str = "") -> list[Joia]:
    query = db.session.query(Joia)
    if busca:
        termo = f"%{busca.strip()}%"
        query = query.filter(Joia.nome.ilike(termo) | Joia.codigo.ilike(termo))
    if categoria:
        query = query.filter_by(categoria=categoria)
    return query.order_by(Joia.nome).limit(100).all()


def get_joia_by_id(joia_id: int) -> Joia:
    return db.session.query(Joia).filter_by(id=joia_id).first()


def get_joia_by_codigo(codigo: str) -> Joia:
    return db.session.query(Joia).filter_by(codigo=codigo.strip().upper()).first()


def update_joia(joia_id: int, codigo: str, nome: str, categoria: str, tipo_prata: str, preco, estoque,
                peso_gramas=None, tamanho: str = "", descricao: str = "", imagem_url: str = "") -> Joia:
    joia = get_joia_by_id(joia_id)
    if not joia:
        raise ValueError("Joia não encontrada.")

    codigo = (codigo or "").strip().upper()
    nome = (nome or "").strip()
    _validar_textos(codigo, nome, categoria, tipo_prata)
    preco, estoque, peso_gramas = _converter_numeros(preco, estoque, peso_gramas)

    existente = Joia.query.filter_by(codigo=codigo).first()
    if existente and existente.id != joia_id:
        raise ValueError("Já existe outra joia com este código.")

    joia.codigo = codigo
    joia.nome = nome
    joia.categoria = categoria
    joia.tipo_prata = tipo_prata
    joia.preco = preco
    joia.estoque = estoque
    joia.peso_gramas = peso_gramas
    joia.tamanho = (tamanho or "").strip() or None
    joia.descricao = (descricao or "").strip() or None
    joia.imagem_url = (imagem_url or "").strip() or None
    db.session.commit()
    return joia


def delete_joia(joia_id: int) -> None:
    joia = get_joia_by_id(joia_id)
    if not joia:
        raise ValueError("Joia não encontrada.")

    db.session.delete(joia)
    db.session.commit()
