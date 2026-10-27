from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .autor import AutorResumen


class LibroCrear(BaseModel):
    titulo: str = Field(min_length=2, max_length=150)
    isbn: str = Field(min_length=10, max_length=30)
    precio: float = Field(gt=0, le=100000)
    stock: int = Field(default=0, ge=0)
    activo: bool = True
    autor_id: int = Field(gt=0)

    @field_validator("titulo")
    @classmethod
    def validar_titulo(cls, valor: str) -> str:
        return " ".join(valor.split()).title()


class LibroActualizar(BaseModel):
    titulo: str | None = Field(default=None, min_length=2, max_length=150)
    isbn: str | None = Field(default=None, min_length=10, max_length=30)
    precio: float | None = Field(default=None, gt=0, le=100000)
    stock: int | None = Field(default=None, ge=0)
    activo: bool | None = None
    autor_id: int | None = Field(default=None, gt=0)

    @field_validator("titulo")
    @classmethod
    def validar_titulo(cls, valor: str | None) -> str | None:
        if valor is None:
            return valor
        return " ".join(valor.split()).title()


class LibroLeer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    isbn: str
    precio: float
    stock: int
    activo: bool
    creado_en: datetime
    autor: AutorResumen
