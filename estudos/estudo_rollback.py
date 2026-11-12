from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from portaria.orm import Setor, criar_engine

engine = criar_engine()

with Session(engine) as sessao:
    try:
        with sessao.begin():  # commit no fim do bloco, rollback se houver exceção
            sessao.add(Setor(nome="Recepção", lotacao_maxima=3, ativo=1))
            sessao.add(Setor(nome="Secretaria", lotacao_maxima=9, ativo=1))  # nome repetido
    except IntegrityError as erro:
        print("rollback:", erro.orig)

    existe = sessao.scalar(select(Setor).where(Setor.nome == "Recepção")) is not None
    print("Recepção ficou gravada?", existe)
