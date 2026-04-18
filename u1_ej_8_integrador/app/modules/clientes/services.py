from typing import List, Optional
from .schemas import ClienteCreate, ClienteRead

db_clientes: List[ClienteRead] = []
id_counter = 1


def numero_contacto_existe(numero_contacto: str, excluir_id: Optional[int] = None) -> bool:
    for c in db_clientes:
        if c.numero_contacto == numero_contacto and c.id != excluir_id:
            return True
    return False


def crear(data: ClienteCreate) -> Optional[ClienteRead]:
    global id_counter
    if numero_contacto_existe(data.numero_contacto):
        return None
    nuevo = ClienteRead(id=id_counter, **data.model_dump())
    db_clientes.append(nuevo)
    id_counter += 1
    return nuevo


def obtener_todos(skip: int = 0, limit: int = 10) -> List[ClienteRead]:
    activos = [c for c in db_clientes if c.activo]
    return activos[skip : skip + limit]


def obtener_por_id(id: int) -> Optional[ClienteRead]:
    for c in db_clientes:
        if c.id == id:
            return c
    return None


def actualizar_total(id: int, data: ClienteCreate) -> Optional[ClienteRead]:
    for index, c in enumerate(db_clientes):
        if c.id == id:
            if numero_contacto_existe(data.numero_contacto, excluir_id=id):
                return None
            actualizado = ClienteRead(id=id, **data.model_dump())
            db_clientes[index] = actualizado
            return actualizado
    return None


def desactivar(id: int) -> Optional[ClienteRead]:
    for index, c in enumerate(db_clientes):
        if c.id == id:
            c_dict = c.model_dump()
            c_dict["activo"] = False
            actualizado = ClienteRead(**c_dict)
            db_clientes[index] = actualizado
            return actualizado
    return None