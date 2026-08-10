import pytest
from src.engineering.battery_model import BatterySimulator

def test_battery_model_objectives(mock_battery_params):
    sim = BatterySimulator()
    results = sim.simulate(mock_battery_params)
    
    expected_objectives = [
        "weight_kg",
        "cost_usd",
        "max_temperature_c",
        "manufacturing_complexity",
        "carbon_footprint_kg_co2",
        "charging_time_10_80_min",
        "capacity_kwh",
        "cycle_life_to_80_soh",
        "energy_density_wh_l",
        "safety_margin",
        "range_km",
        "power_density_w_kg"
    ]
    
    # Assert all 12 objectives are present
    for obj in expected_objectives:
        assert obj in results
        
    assert len(results) == 12
    
    # Assert physical constraints
    assert results["weight_kg"] > 0
    assert results["cost_usd"] > 0
    assert results["max_temperature_c"] > 0
    assert results["capacity_kwh"] > 0
    assert results["cycle_life_to_80_soh"] > 0
    assert results["energy_density_wh_l"] > 0
    assert 0 <= results["safety_margin"] <= 1.0
    assert results["range_km"] > 0
    assert results["power_density_w_kg"] > 0
