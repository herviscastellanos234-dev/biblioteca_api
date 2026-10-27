from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from ..core.exceptions import Conflicto, NoEncontrado
from ..models import Libro
from ..schemas.libro import LibroActualizar, LibroCrear
from . import autores as autores_ctrl


def _consulta_base():
    return select(Libro).options(selectinload(Libro.autor))


def listar(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    autor_id: int | None = None,
    buscar: str | None = None,
    solo_activos: bool = False,
) -> list[Libro]:
    consulta = _consulta_base()

    if autor_id is not None:
        consulta = consulta.where(Libro.autor_id == autor_id)

    if buscar:
        consulta = consulta.where(Libro.titulo.ilike(f"%{buscar}%"))

    if solo_activos:
        consulta = consulta.where(Libro.activo.is_(True))

    consulta = consulta.order_by(Libro.titulo).offset(skip).limit(limit)
    return list(db.scalars(consulta))


def obtener(db: Session, libro_id: int) -> Libro:
    libro = db.scalar(_consulta_base().where(Libro.id == libro_id))
    if libro is None:
        raise NoEncontrado("Libro no encontrado")
    return libro


def _validar_titulo_unico(db: Session, titulo: str, excluir_id: int | None = None) -> None:
    consulta = select(Libro.id).where(func.lower(Libro.titulo) == titulo.lower())
    if excluir_id is not None:
        consulta = consulta.where(Libro.id != excluir_id)
    if db.scalar(consulta) is not None:
        raise Conflicto(f"Ya existe el libro '{titulo}'")


def _validar_isbn_unico(db: Session, isbn: str, excluir_id: int | None = None) -> None:
    consulta = select(Libro.id).where(func.lower(Libro.isbn) == isbn.lower())
    if excluir_id is not None:
        consulta = consulta.where(Libro.id != excluir_id)
    if db.scalar(consulta) is not None:
        raise Conflicto(f"Ya existe el ISBN '{isbn}'")


def crear(db: Session, datos: LibroCrear) -> Libro:
    autores_ctrl.obtener(db, datos.autor_id)
    _validar_titulo_unico(db, datos.titulo)
    _validar_isbn_unico(db, datos.isbn)

    libro = Libro(**datos.model_dump())
    db.add(libro)
    db.commit()
    return obtener(db, libro.id)


def actualizar(db: Session, libro_id: int, datos: LibroActualizar) -> Libro:
    libro = obtener(db, libro_id)
    cambios = datos.model_dump(exclude_unset=True, exclude_none=True)

    if "autor_id" in cambios:
        autores_ctrl.obtener(db, cambios["autor_id"])

    if "titulo" in cambios:
        _validar_titulo_unico(db, cambios["titulo"], excluir_id=libro_id)

    if "isbn" in cambios:
        _validar_isbn_unico(db, cambios["isbn"], excluir_id=libro_id)

    for campo, valor in cambios.items():
        setattr(libro, campo, valor)

    db.commit()
    db.expire(libro)
    return obtener(db, libro_id)


def eliminar(db: Session, libro_id: int) -> None:
    libro = obtener(db, libro_id)
    db.delete(libro)
    db.commit()
