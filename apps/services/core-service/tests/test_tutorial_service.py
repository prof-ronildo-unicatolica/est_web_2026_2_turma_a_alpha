import asyncio
from types import SimpleNamespace
from uuid import uuid4

from app.services.tutorial_service import TutorialService


def _professor_payload():
    return SimpleNamespace(
        nome="Prof Teste",
        email="prof@teste.com",
        sala="Sala 1",
        biografia="Bio",
        biografia_mapa=None,
    )


def test_get_sobre_data_sem_dados_devolve_estrutura_vazia(db_session):
    dados = TutorialService(db_session).get_sobre_data()

    assert dados["equipe"] == "Alpha"
    assert dados["professor"] is None
    assert dados["disciplinas"] == []
    assert dados["stacks"] == []


def test_create_professor_e_busca_por_id(db_session):
    service = TutorialService(db_session)
    professor = service.create_professor(_professor_payload())

    encontrado = service.get_professor_by_id(professor.id)

    assert encontrado is not None
    assert encontrado.email == "prof@teste.com"


def test_get_professor_by_id_inexistente_devolve_none(db_session):
    assert TutorialService(db_session).get_professor_by_id(uuid4()) is None


def test_get_sobre_data_com_professor_cadastrado(db_session):
    service = TutorialService(db_session)
    service.create_professor(_professor_payload())

    dados = service.get_sobre_data()

    assert dados["professor"]["nome"] == "Prof Teste"
    assert dados["professor"]["sala"] == "Sala 1"


def test_create_disciplina_publica_evento_de_auditoria(db_session, monkeypatch):
    eventos = []

    async def publish_falso(fila, dados):
        eventos.append((fila, dados))

    monkeypatch.setattr("app.services.tutorial_service.publish_event", publish_falso)
    service = TutorialService(db_session)
    professor = service.create_professor(_professor_payload())
    payload = SimpleNamespace(
        nome="Web", ano=2026, semestre=2, professor_id=professor.id
    )

    disciplina = asyncio.run(service.create_disciplina(payload))

    assert disciplina.nome == "Web"
    assert len(eventos) == 1
    fila, dados = eventos[0]
    assert fila == "audit.logs"
    assert dados["evento"] == "disciplina.criada"
    assert dados["nome"] == "Web"