from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
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

class BatteryChemistry(Base):
    __tablename__ = "battery_chemistries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    family = Column(String, index=True) # e.g. Lithium-ion, Solid-State
    
    cathode = Column(String)
    anode = Column(String)
    electrolyte = Column(String)
    separator = Column(String)
    
    nominal_voltage = Column(Float) # V
    specific_capacity = Column(Float) # mAh/g
    energy_density = Column(Float) # Wh/kg
    power_density = Column(Float) # W/kg
    cycle_life = Column(Integer)
    efficiency = Column(Float) # % (0-100)
    thermal_stability = Column(String)
    safety_rating = Column(Float) # 1-10

    advantages = Column(JSON)
    disadvantages = Column(JSON)
    
    reactions = relationship("Reaction", back_populates="chemistry", cascade="all, delete-orphan")

class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    chemistry_id = Column(Integer, ForeignKey("battery_chemistries.id"))
    reaction_type = Column(String) # 'discharge_anode', 'discharge_cathode', 'discharge_overall'
    equation = Column(String)
    electrons_transferred = Column(Integer)
    description = Column(String)

    chemistry = relationship("BatteryChemistry", back_populates="reactions")

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    formula = Column(String)
    molar_mass = Column(Float) # g/mol
    material_type = Column(String) # 'cathode', 'anode', 'electrolyte', 'element'
    atomic_number = Column(Integer, nullable=True) # For pure elements
    symbol = Column(String, nullable=True) # For pure elements
    oxidation_states = Column(String, nullable=True)
    abundance = Column(String, nullable=True)
    supply_risk = Column(Float, nullable=True) # 1-10
    toxicity = Column(String, nullable=True)
