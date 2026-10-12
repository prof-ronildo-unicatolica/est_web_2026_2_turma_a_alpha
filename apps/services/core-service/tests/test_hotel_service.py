from app.services.hotel_service import CidadeService


def test_criar_cidade_valida(db_session):
    service = CidadeService(db_session)

    cidade = service.criar("Fortaleza")

    assert cidade.id is not None
    assert cidade.nome == "Fortaleza"