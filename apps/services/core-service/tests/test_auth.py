"""Suite de testes da autenticacao real (JWT + bcrypt + RBAC via banco)."""

BASE = "/api/v1/auth"


def test_login_valido_retorna_token_jwt(client, seed_usuarios):
    resp = client.post(
        f"{BASE}/login", json={"email": "cliente@hotel.com", "senha": "cliente123"}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    # Um JWT tem 3 partes separadas por ponto: header.payload.assinatura
    assert body["access_token"].count(".") == 2


def test_login_invalido_retorna_401(client, seed_usuarios):
    resp = client.post(
        f"{BASE}/login", json={"email": "cliente@hotel.com", "senha": "errada"}
    )
    assert resp.status_code == 401


def test_login_email_inexistente_retorna_401(client, seed_usuarios):
    resp = client.post(
        f"{BASE}/login", json={"email": "naoexiste@hotel.com", "senha": "qualquer"}
    )
    assert resp.status_code == 401


def test_rota_protegida_sem_token_e_bloqueada(client):
    resp = client.get(f"{BASE}/me")
    assert resp.status_code in (401, 403)


def test_rota_protegida_com_token_retorna_perfil(client, seed_usuarios):
    token = client.post(
        f"{BASE}/login", json={"email": "cliente@hotel.com", "senha": "cliente123"}
    ).json()["access_token"]
    resp = client.get(f"{BASE}/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["email"] == "cliente@hotel.com"
    assert body["is_admin"] is False
    assert "senha" not in body
    assert "senha_hash" not in body  # o hash tambem nunca deve vazar


def test_cliente_nao_acessa_rota_admin(client, seed_usuarios):
    token = client.post(
        f"{BASE}/login", json={"email": "cliente@hotel.com", "senha": "cliente123"}
    ).json()["access_token"]
    resp = client.get(
        f"{BASE}/admin/verificacao", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 403


def test_admin_acessa_rota_admin(client, seed_usuarios):
    token = client.post(
        f"{BASE}/login", json={"email": "admin@hotel.com", "senha": "admin123"}
    ).json()["access_token"]
    resp = client.get(
        f"{BASE}/admin/verificacao", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200


def test_registro_cria_usuario_com_sucesso(client):
    resp = client.post(
        f"{BASE}/register",
        json={
            "nome": "Hospede Teste",
            "email": "hospede.teste@hotel.com",
            "senha": "senha123",
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == "hospede.teste@hotel.com"
    assert body["is_admin"] is False
    assert "senha" not in body
    assert "senha_hash" not in body


def test_registro_com_email_duplicado_retorna_409(client, seed_usuarios):
    resp = client.post(
        f"{BASE}/register",
        json={
            "nome": "Outro Cliente",
            "email": "cliente@hotel.com",  # ja existe via seed_usuarios
            "senha": "outrasenha",
        },
    )
    assert resp.status_code == 409


def test_usuario_registrado_consegue_logar(client):
    client.post(
        f"{BASE}/register",
        json={
            "nome": "Novo Hospede",
            "email": "novo.hospede@hotel.com",
            "senha": "minhasenha",
        },
    )
    resp = client.post(
        f"{BASE}/login",
        json={"email": "novo.hospede@hotel.com", "senha": "minhasenha"},
    )
    assert resp.status_code == 200
    assert resp.json()["access_token"]