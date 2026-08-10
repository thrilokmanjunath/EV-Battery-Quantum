import pytest

@pytest.fixture
def mock_battery_params():
    return {
        "cells_series": 96,
        "cells_parallel": 5,
        "cell_capacity_ah": 5.0,
        "cell_voltage_v": 3.7,
        "chemistry": "NMC811",
        "anode_material": "Graphite",
        "housing_material": "Aluminum",
        "cooling_method": "Liquid",
        "pack_layout": "Modular",
        "max_charge_c_rate": 2.0,
        "internal_resistance_mohm": 15.0,
        "tim_conductivity_w_mk": 3.0,
        "electrolyte": "Liquid",
        "thermal_runaway_mitigation": "Active"
    }

@pytest.fixture
def mock_optimization_config():
    return {
        "optimization": {
            "variables": {
                "chemistry": ["NMC811", "LFP", "NCA", "NMC532", "NMC622"],
                "anode_material": ["Graphite", "Silicon-Graphite", "Lithium-Metal"],
                "housing_material": ["Aluminum", "Steel", "Carbon-Fiber", "Composite"],
                "cooling_method": ["Air", "Liquid", "Immersion", "Phase-Change"],
                "pack_layout": ["Cell-to-Pack", "Modular"]
            }
        }
    }
