import pytest
from fastapi import HTTPException

from app.schemas.usuario import UsuarioCreate
from app.services.auth_service import AuthService


def _dados(email="ana@hotel.com", senha="senha123"):
    return UsuarioCreate(nome="Ana", email=email, senha=senha)


def test_registrar_cria_cliente_com_senha_criptografada(db_session):
    usuario = AuthService(db_session).registrar(_dados())

    assert usuario.id is not None
    assert usuario.email == "ana@hotel.com"
    assert usuario.is_admin is False
    assert usuario.senha_hash != "senha123"


def test_registrar_rejeita_email_duplicado(db_session):
    service = AuthService(db_session)
    service.registrar(_dados())

    with pytest.raises(HTTPException) as erro:
        service.registrar(_dados())

    assert erro.value.status_code == 409


def test_autenticar_com_credenciais_validas(db_session):
    service = AuthService(db_session)
    criado = service.registrar(_dados())

    usuario = service.autenticar("ana@hotel.com", "senha123")

    assert usuario.id == criado.id


def test_autenticar_rejeita_senha_errada(db_session):
    service = AuthService(db_session)
    service.registrar(_dados())

    with pytest.raises(HTTPException) as erro:
        service.autenticar("ana@hotel.com", "errada")

    assert erro.value.status_code == 401


def test_autenticar_rejeita_email_inexistente(db_session):
    with pytest.raises(HTTPException) as erro:
        AuthService(db_session).autenticar("ninguem@hotel.com", "qualquer")

    assert erro.value.status_code == 401


def test_gerar_token_devolve_jwt_bearer(db_session):
    service = AuthService(db_session)
    usuario = service.registrar(_dados())

    token = service.gerar_token(usuario)

    assert token.token_type == "bearer"
    assert token.access_token.count(".") == 2