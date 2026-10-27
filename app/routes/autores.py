from fastapi import APIRouter

from ..controllers import autores as controlador
from ..core.dependencies import SessionDep
from ..schemas.autor import AutorActualizar, AutorCrear, AutorLeer

router = APIRouter(prefix="/autores", tags=["Autores"])


@router.get("", response_model=list[AutorLeer])
def listar_autores(db: SessionDep):
    return controlador.listar(db)


@router.get("/{autor_id}", response_model=AutorLeer)
def obtener_autor(autor_id: int, db: SessionDep):
    return controlador.obtener(db, autor_id)


@router.post("", response_model=AutorLeer, status_code=201)
def crear_autor(datos: AutorCrear, db: SessionDep):
    return controlador.crear(db, datos)


@router.patch("/{autor_id}", response_model=AutorLeer)
def actualizar_autor(autor_id: int, datos: AutorActualizar, db: SessionDep):
    return controlador.actualizar(db, autor_id, datos)


@router.delete("/{autor_id}", status_code=204)
def eliminar_autor(autor_id: int, db: SessionDep):
    controlador.eliminar(db, autor_id)
    return None
