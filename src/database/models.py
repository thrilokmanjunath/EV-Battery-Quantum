from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class OptimizationRun(Base):
    __tablename__ = "optimization_runs"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pending")
    parameters = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # The 12 objectives
    weight = Column(Float, nullable=True)
    cost = Column(Float, nullable=True)
    energy_density = Column(Float, nullable=True)
    power_density = Column(Float, nullable=True)
    cycle_life = Column(Float, nullable=True)
    safety_score = Column(Float, nullable=True)
    charging_time = Column(Float, nullable=True)
    temperature_tolerance = Column(Float, nullable=True)
    material_sustainability = Column(Float, nullable=True)
    internal_resistance = Column(Float, nullable=True)
    voltage_stability = Column(Float, nullable=True)
    manufacturing_complexity = Column(Float, nullable=True)
