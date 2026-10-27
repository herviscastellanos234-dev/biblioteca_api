from fastapi import APIRouter, Query

from ..controllers import libros as controlador
from ..core.dependencies import SessionDep
from ..schemas.libro import LibroActualizar, LibroCrear, LibroLeer

router = APIRouter(prefix="/libros", tags=["Libros"])


@router.get("", response_model=list[LibroLeer])
def listar_libros(
    db: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    autor_id: int | None = Query(None, gt=0),
    buscar: str | None = Query(None, description="Texto para buscar por título"),
    solo_activos: bool = False,
):
    return controlador.listar(db, skip, limit, autor_id, buscar, solo_activos)


@router.get("/{libro_id}", response_model=LibroLeer)
def obtener_libro(libro_id: int, db: SessionDep):
    return controlador.obtener(db, libro_id)


@router.post("", response_model=LibroLeer, status_code=201)
def crear_libro(datos: LibroCrear, db: SessionDep):
    return controlador.crear(db, datos)


@router.patch("/{libro_id}", response_model=LibroLeer)
def actualizar_libro(libro_id: int, datos: LibroActualizar, db: SessionDep):
    return controlador.actualizar(db, libro_id, datos)


@router.delete("/{libro_id}", status_code=204)
def eliminar_libro(libro_id: int, db: SessionDep):
    controlador.eliminar(db, libro_id)
    return None
