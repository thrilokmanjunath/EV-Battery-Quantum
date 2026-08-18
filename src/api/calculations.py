from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ..engineering.electrochemistry import (
    calculate_theoretical_specific_capacity,
    calculate_energy,
    calculate_specific_energy,
    estimate_charging_time,
    get_current_from_c_rate
)

router = APIRouter(prefix="/api/calculations")

class CapacityRequest(BaseModel):
    electrons_transferred: int = Field(..., gt=0)
    molar_mass: float = Field(..., gt=0)

class EnergyRequest(BaseModel):
    voltage: float = Field(..., gt=0)
    capacity: float = Field(..., gt=0)
    mass: float = None

class ChargeTimeRequest(BaseModel):
    capacity: float = Field(..., gt=0)
    c_rate: float = Field(None, gt=0)
    current: float = Field(None, gt=0)
    efficiency: float = Field(0.95, gt=0, le=1.0)

@router.post("/theoretical-capacity")
def api_theoretical_capacity(req: CapacityRequest):
    cap = calculate_theoretical_specific_capacity(req.electrons_transferred, req.molar_mass)
    return {"theoretical_specific_capacity_mah_g": round(cap, 2)}

@router.post("/energy")
def api_energy(req: EnergyRequest):
    energy = calculate_energy(req.voltage, req.capacity)
    resp = {"energy_wh": round(energy, 2)}
    if req.mass:
        spec_energy = calculate_specific_energy(req.voltage, req.capacity, req.mass)
        resp["specific_energy_wh_kg"] = round(spec_energy, 2)
    return resp

@router.post("/charging-time")
def api_charging_time(req: ChargeTimeRequest):
    if req.current is None and req.c_rate is None:
        raise HTTPException(status_code=400, detail="Must provide either current or c_rate")
    
    current = req.current if req.current else get_current_from_c_rate(req.capacity, req.c_rate)
    time_h = estimate_charging_time(req.capacity, current, req.efficiency)
    return {
        "charging_time_hours": round(time_h, 2),
        "current_a": round(current, 2)
    }
