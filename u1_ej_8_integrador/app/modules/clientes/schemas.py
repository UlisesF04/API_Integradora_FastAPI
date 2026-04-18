from pydantic import BaseModel, Field
from typing import Optional


class ClienteBase(BaseModel):
    nombre: str = Field(..., max_length=50, example="Juan Pérez")
    numero_contacto: str = Field(..., max_length=20, example="1122334455")
    activo: bool = True


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=50)
    numero_contacto: Optional[str] = Field(None, max_length=20)
    activo: Optional[bool] = None


class ClienteRead(ClienteBase):
    id: int