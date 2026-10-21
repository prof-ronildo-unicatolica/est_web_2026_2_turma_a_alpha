import pytest

from app.services.hotel_service import (
    CidadeJaExisteError,
    CidadeService,
    NomeInvalidoError,
)


def test_criar_cidade_valida(db_session):
    service = CidadeService(db_session)

    cidade = service.criar("Fortaleza")

    assert cidade.id is not None
    assert cidade.nome == "Fortaleza"


def test_criar_cidade_normaliza_nome(db_session):
    service = CidadeService(db_session)

    cidade = service.criar("  Fortaleza  ")

    assert cidade.nome == "Fortaleza"


@pytest.mark.parametrize("nome", ["", "   "])
def test_criar_cidade_rejeita_nome_vazio_ou_espacos(db_session, nome):
    service = CidadeService(db_session)

    with pytest.raises(NomeInvalidoError):
        service.criar(nome)


def test_criar_cidade_rejeita_duplicada(db_session):
    service = CidadeService(db_session)

    service.criar("Fortaleza")

    with pytest.raises(CidadeJaExisteError):
        service.criar("Fortaleza")


def test_criar_cidade_rejeita_duplicada_apos_normalizacao(db_session):
    service = CidadeService(db_session)

    service.criar("Fortaleza")

    with pytest.raises(CidadeJaExisteError):
        service.criar("  Fortaleza  ")


def test_listar_cidades(db_session):
    service = CidadeService(db_session)

    service.criar("Fortaleza")
    service.criar("Aquiraz")

    cidades = service.listar()

    assert len(cidades) == 2
    assert {cidade.nome for cidade in cidades} == {"Fortaleza", "Aquiraz"}
