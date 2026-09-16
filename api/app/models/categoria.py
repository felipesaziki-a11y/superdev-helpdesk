from datetime import datetime
from sqlalchemy import Boolean, DateTime, String
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from app.core.tempo import agora


class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    descricao: Mapped[str] = mapped_column(String(120), nullable=False)
    ativa: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=agora, nullable=False)