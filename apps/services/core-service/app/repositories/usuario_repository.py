from uuid import UUID

from sqlalchemy.orm import Session

from app.models.usuario import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_email(self, email: str) -> Usuario | None:
        return (
            self.db.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )

    def buscar_por_id(self, usuario_id: UUID) -> Usuario | None:
        return (
            self.db.query(Usuario)
            .filter(Usuario.id == usuario_id)
            .first()
        )

    def criar(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
