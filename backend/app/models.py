from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

# Manejo de importación dependiendo de desde dónde ejecutes uvicorn
try:
    from .database import Base
except ImportError:
    from database import Base

class Conductor(Base):
    __tablename__ = "conductores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    licencia = Column(String, unique=True, index=True)

    vehiculos = relationship("Vehiculo", back_populates="conductor")
    alertas = relationship("Alerta", back_populates="conductor")


class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String, unique=True, index=True)
    modelo = Column(String)
    conductor_id = Column(Integer, ForeignKey("conductores.id"))

    conductor = relationship("Conductor", back_populates="vehiculos")
    alertas = relationship("Alerta", back_populates="vehiculo")


class Alerta(Base):
    __tablename__ = "alertas"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, index=True)
    nivel = Column(String, index=True)
    valor_velocidad = Column(Float)
    
    # --- NUEVOS CAMPOS BIOMÉTRICOS ---
    valor_bpm = Column(Float)
    parpadeos_por_minuto = Column(Float)
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    conductor_id = Column(Integer, ForeignKey("conductores.id"))
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"))

    conductor = relationship("Conductor", back_populates="alertas")
    vehiculo = relationship("Vehiculo", back_populates="alertas")