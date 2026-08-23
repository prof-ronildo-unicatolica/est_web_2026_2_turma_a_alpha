from uuid import UUID

from sqlalchemy.orm import Session

from app.models.hotel import Hotel


class HotelRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[Hotel]:
        return self.db.query(Hotel).order_by(Hotel.nome).all()

    def buscar_por_id(self, hotel_id: UUID) -> Hotel | None:
        return (
            self.db.query(Hotel)
            .filter(Hotel.id == hotel_id)
            .first()
        )

    def listar_por_cidade(self, cidade_id: UUID) -> list[Hotel]:
        return (
            self.db.query(Hotel)
            .filter(Hotel.cidade_id == cidade_id)
            .order_by(Hotel.nome)
            .all()
        )

    def criar(self, hotel: Hotel) -> Hotel:
        self.db.add(hotel)
        self.db.commit()
        self.db.refresh(hotel)
        return hotel

    def atualizar(self, hotel: Hotel) -> Hotel:
        self.db.commit()
        self.db.refresh(hotel)
        return hotel

    def remover(self, hotel: Hotel) -> None:
        self.db.delete(hotel)
        self.db.commit()
