from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# --- ESQUEMAS DE AUTENTICACIÓN ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- ESQUEMAS DE ALERTA ---
class AlertaBase(BaseModel):
    nivel: str
    tipo: str
    valor_velocidad: float
    valor_bpm: float
    parpadeos_por_minuto: float
    conductor_id: int
    vehiculo_id: int

class AlertaCreate(AlertaBase):
    pass

class AlertaOut(AlertaBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# --- ESQUEMAS DE VEHÍCULO ---
class VehiculoBase(BaseModel):
    placa: str
    modelo: str
    conductor_id: int

class VehiculoCreate(VehiculoBase):
    pass

class VehiculoOut(VehiculoBase):
    id: int

    class Config:
        from_attributes = True

# --- ESQUEMAS DE CONDUCTOR ---
class ConductorBase(BaseModel):
    nombre: str
    licencia: str

class ConductorCreate(ConductorBase):
    pass

class ConductorOut(ConductorBase):
    id: int
    vehiculos: List[VehiculoOut] = []

    class Config:
        from_attributes = True

# Alias de seguridad por si alguna otra parte de tu código (como crud.py) 
# llama a las clases sin el sufijo "Out"
Alerta = AlertaOut
Vehiculo = VehiculoOut
Conductor = ConductorOut