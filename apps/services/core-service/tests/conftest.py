import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import get_db
from app.core.security import gerar_hash_senha
from app.main import app
from app.models.tutorial import Base
from app.models.usuario import Usuario

# Banco SQLite em arquivo temporario para os testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def seed_usuarios(db_session):
    """Semeia admin e cliente de demonstracao no banco de teste."""
    admin = Usuario(
        nome="Administrador da Franquia",
        email="admin@hotel.com",
        senha_hash=gerar_hash_senha("admin123"),
        is_admin=True,
    )
    cliente = Usuario(
        nome="Cliente Demonstracao",
        email="cliente@hotel.com",
        senha_hash=gerar_hash_senha("cliente123"),
        is_admin=False,
    )
    db_session.add(admin)
    db_session.add(cliente)
    db_session.commit()
    return {"admin": admin, "cliente": cliente}


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    # Desativamos raise_server_exceptions para validar retornos de erro 500
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()