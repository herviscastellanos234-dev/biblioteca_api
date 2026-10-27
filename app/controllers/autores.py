from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..core.exceptions import Conflicto, NoEncontrado
from ..models import Autor
from ..schemas.autor import AutorActualizar, AutorCrear


def listar(db: Session) -> list[Autor]:
    return list(db.scalars(select(Autor).order_by(Autor.nombre)))


def obtener(db: Session, autor_id: int) -> Autor:
    autor = db.get(Autor, autor_id)
    if autor is None:
        raise NoEncontrado("Autor no encontrado")
    return autor


def _validar_nombre_unico(db: Session, nombre: str, excluir_id: int | None = None) -> None:
    consulta = select(Autor.id).where(func.lower(Autor.nombre) == nombre.lower())
    if excluir_id is not None:
        consulta = consulta.where(Autor.id != excluir_id)
    if db.scalar(consulta) is not None:
        raise Conflicto(f"Ya existe el autor '{nombre}'")


def crear(db: Session, datos: AutorCrear) -> Autor:
    _validar_nombre_unico(db, datos.nombre)
    autor = Autor(**datos.model_dump())
    db.add(autor)
    db.commit()
    return autor


def actualizar(db: Session, autor_id: int, datos: AutorActualizar) -> Autor:
    autor = obtener(db, autor_id)
    cambios = datos.model_dump(exclude_unset=True, exclude_none=True)

    if "nombre" in cambios:
        _validar_nombre_unico(db, cambios["nombre"], excluir_id=autor_id)

    for campo, valor in cambios.items():
        setattr(autor, campo, valor)

    db.commit()
    return autor


def eliminar(db: Session, autor_id: int) -> None:
    autor = obtener(db, autor_id)
    if autor.libros:
        raise Conflicto("No se puede eliminar un autor que tiene libros asociados")
    db.delete(autor)
    db.commit()
