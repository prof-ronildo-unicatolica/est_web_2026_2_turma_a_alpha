from uuid import uuid4

import pytest

from app.services.hotel_service import (
    CidadeJaExisteError,
    CidadeNaoEncontradaError,
    CidadeService,
    HotelService,
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


def test_criar_hotel_vinculado_a_cidade_existente(db_session):
    cidade_service = CidadeService(db_session)
    hotel_service = HotelService(db_session)

    cidade = cidade_service.criar("Fortaleza")

    hotel = hotel_service.criar(
        nome="Hotel Central",
        cidade_id=cidade.id,
    )

    assert hotel.id is not None
    assert hotel.nome == "Hotel Central"
    assert hotel.cidade_id == cidade.id


def test_criar_hotel_normaliza_nome(db_session):
    cidade_service = CidadeService(db_session)
    hotel_service = HotelService(db_session)

    cidade = cidade_service.criar("Fortaleza")

    hotel = hotel_service.criar(
        nome="  Hotel Central  ",
        cidade_id=cidade.id,
    )

    assert hotel.nome == "Hotel Central"


@pytest.mark.parametrize("nome", ["", "   "])
def test_criar_hotel_rejeita_nome_vazio_ou_espacos(db_session, nome):
    cidade_service = CidadeService(db_session)
    hotel_service = HotelService(db_session)

    cidade = cidade_service.criar("Fortaleza")

    with pytest.raises(NomeInvalidoError):
        hotel_service.criar(
            nome=nome,
            cidade_id=cidade.id,
        )


def test_criar_hotel_rejeita_cidade_inexistente(db_session):
    hotel_service = HotelService(db_session)
    cidade_id_inexistente = uuid4()

    with pytest.raises(CidadeNaoEncontradaError):
        hotel_service.criar(
            nome="Hotel Central",
            cidade_id=cidade_id_inexistente,
        )


def test_listar_hoteis(db_session):
    cidade_service = CidadeService(db_session)
    hotel_service = HotelService(db_session)

    cidade = cidade_service.criar("Fortaleza")

    hotel_service.criar("Hotel Central", cidade.id)
    hotel_service.criar("Hotel Praia", cidade.id)

    hoteis = hotel_service.listar()

    assert len(hoteis) == 2
    assert {hotel.nome for hotel in hoteis} == {
        "Hotel Central",
        "Hotel Praia",
    }


def test_listar_hoteis_filtra_por_cidade(db_session):
    cidade_service = CidadeService(db_session)
    hotel_service = HotelService(db_session)

    fortaleza = cidade_service.criar("Fortaleza")
    aquiraz = cidade_service.criar("Aquiraz")

    hotel_service.criar("Hotel Central", fortaleza.id)
    hotel_service.criar("Hotel Praia", fortaleza.id)
    hotel_service.criar("Pousada Aquiraz", aquiraz.id)

    hoteis = hotel_service.listar(cidade_id=fortaleza.id)

    assert len(hoteis) == 2
    assert {hotel.nome for hotel in hoteis} == {
        "Hotel Central",
        "Hotel Praia",
    }
    assert all(hotel.cidade_id == fortaleza.id for hotel in hoteis)


def test_listar_hoteis_rejeita_cidade_inexistente(db_session):
    hotel_service = HotelService(db_session)
    cidade_id_inexistente = uuid4()

    with pytest.raises(CidadeNaoEncontradaError):
        hotel_service.listar(cidade_id=cidade_id_inexistente)
