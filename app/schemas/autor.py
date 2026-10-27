from pydantic import BaseModel, ConfigDict, Field, field_validator


def limpiar_nombre(valor: str | None) -> str | None:
    if not valor:
        return valor
    return " ".join(valor.split()).title()


class AutorCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    nacionalidad: str | None = Field(default=None, max_length=80)

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor: str) -> str:
        return limpiar_nombre(valor)


class AutorActualizar(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=100)
    nacionalidad: str | None = Field(default=None, max_length=80)

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor: str | None) -> str | None:
        if valor is None:
            return valor
        return limpiar_nombre(valor)


class AutorLeer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    nacionalidad: str | None


class AutorResumen(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
