from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.database import Base

if TYPE_CHECKING:
    from .autor import Autor


class Libro(Base):
    __tablename__ = "libros"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    isbn: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    precio: Mapped[float] = mapped_column(Numeric(10, 2, asdecimal=False), nullable=False)
    stock: Mapped[int] = mapped_column(default=0, nullable=False)
    activo: Mapped[bool] = mapped_column(default=True, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    autor_id: Mapped[int] = mapped_column(
        ForeignKey("autores.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    autor: Mapped["Autor"] = relationship(back_populates="libros")
