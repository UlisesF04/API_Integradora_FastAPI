from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import List
from . import schemas, services

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post(
    "/", response_model=schemas.ClienteRead, status_code=status.HTTP_201_CREATED
)
def alta_cliente(cliente: schemas.ClienteCreate):
    nuevo = services.crear(cliente)
    if nuevo is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El número de contacto '{cliente.numero_contacto}' ya está registrado"
        )
    return nuevo


@router.get(
    "/", response_model=List[schemas.ClienteRead], status_code=status.HTTP_200_OK
)
def listar_clientes(skip: int = Query(0, ge=0), limit: int = Query(10, le=50)):
    return services.obtener_todos(skip, limit)


@router.get(
    "/{id}", response_model=schemas.ClienteRead, status_code=status.HTTP_200_OK
)
def detalle_cliente(id: int = Path(..., gt=0)):
    cliente = services.obtener_por_id(id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
        )
    return cliente


@router.put(
    "/{id}", response_model=schemas.ClienteRead, status_code=status.HTTP_200_OK
)
def actualizar_cliente(cliente: schemas.ClienteCreate, id: int = Path(..., gt=0)):
    if not services.obtener_por_id(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
        )
    actualizado = services.actualizar_total(id, cliente)
    if actualizado is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El número de contacto '{cliente.numero_contacto}' ya está registrado"
        )
    return actualizado


@router.put(
    "/{id}/desactivar",
    response_model=schemas.ClienteRead,
    status_code=status.HTTP_200_OK,
)
def borrado_logico(id: int = Path(..., gt=0)):
    desactivado = services.desactivar(id)
    if not desactivado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
        )
    return desactivado