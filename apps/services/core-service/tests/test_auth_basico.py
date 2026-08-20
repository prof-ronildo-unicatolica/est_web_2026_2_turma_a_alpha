"""Testes da suíte de autenticação real (JWT / Bcrypt / RBAC)."""

import pytest
from app.core.security import get_password_hash
from app.models.usuario import Usuario

BASE = "/api/v1/auth"


@pytest.fixture
def auth_usuarios(db_session):
    """Popula os usuários de teste no banco isolado de cada teste."""
    admin = Usuario(
        nome="Administrador da Franquia",
        email="admin@hotel.com",
        senha_hash=get_password_hash("admin123"),
        is_admin=True,
    )
    cliente = Usuario(
        nome="Cliente Demonstracao",
        email="cliente@hotel.com",
        senha_hash=get_password_hash("cliente123"),
        is_admin=False,
    )
    db_session.add(admin)
    db_session.add(cliente)
    db_session.commit()
    return {"admin": admin, "cliente": cliente}


def test_cadastrar_novo_usuario(client, db_session):
    resp = client.post(
        f"{BASE}/register",
        json={"nome": "Novo Usuario", "email": "novo@hotel.com", "senha": "senha123"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == "novo@hotel.com"
    assert "senha" not in body


def test_login_valido_retorna_token(client, auth_usuarios):
    resp = client.post(
        f"{BASE}/login", json={"email": "cliente@hotel.com", "senha": "cliente123"}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_invalido_retorna_401(client, auth_usuarios):
    resp = client.post(
        f"{BASE}/login", json={"email": "cliente@hotel.com", "senha": "errada"}
    )
    assert resp.status_code == 401


def test_rota_protegida_sem_token_e_bloqueada(client, auth_usuarios):
    resp = client.get(f"{BASE}/me")
    assert resp.status_code in (401, 403)


def test_rota_protegida_com_token_retorna_perfil(client, auth_usuarios):
    token = client.post(
        f"{BASE}/login", json={"email": "cliente@hotel.com", "senha": "cliente123"}
    ).json()["access_token"]
    resp = client.get(f"{BASE}/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["email"] == "cliente@hotel.com"
    assert body["is_admin"] is False
    assert "senha" not in body


def test_cliente_nao_acessa_rota_admin(client, auth_usuarios):
    token = client.post(
        f"{BASE}/login", json={"email": "cliente@hotel.com", "senha": "cliente123"}
    ).json()["access_token"]
    resp = client.get(
        f"{BASE}/admin/verificacao", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 403


def test_admin_acessa_rota_admin(client, auth_usuarios):
    token = client.post(
        f"{BASE}/login", json={"email": "admin@hotel.com", "senha": "admin123"}
    ).json()["access_token"]
    resp = client.get(
        f"{BASE}/admin/verificacao", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
