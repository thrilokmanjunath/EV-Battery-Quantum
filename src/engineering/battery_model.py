import numpy as np

class BatterySimulator:
    """
    Simulator that computes deterministic engineering objectives based on 30+ input battery parameters.
    Uses heuristic and physics-inspired approximations suitable for generating QML optimization targets.
    """
    def __init__(self):
        # Base property dictionaries
        self.chemistry_density = {
            "NMC811": 2.8, "LFP": 2.2, "NCA": 2.7, "NMC532": 2.6, "NMC622": 2.65
        }
        self.chemistry_cost = {
            "NMC811": 130, "LFP": 90, "NCA": 135, "NMC532": 110, "NMC622": 120
        }
        self.anode_factor = {
            "Graphite": 1.0, "Silicon-Graphite": 1.2, "Lithium-Metal": 1.5
        }
        self.housing_weight_factor = {
            "Aluminum": 1.0, "Steel": 2.0, "Carbon-Fiber": 0.5, "Composite": 0.8
        }
        self.cooling_efficiency = {
            "Air": 0.5, "Liquid": 0.8, "Immersion": 0.95, "Phase-Change": 0.85
        }
        self.layout_complexity = {
            "Cell-to-Pack": 0.7, "Modular": 1.0
        }

    def simulate(self, params: dict) -> dict:
        """
        Takes 30+ parameters (dict) and returns deterministic engineering objectives.
        Returns a dictionary of objectives.
        """
        # Parse basic parameters
        cells_s = params.get("cells_series", 100)
        cells_p = params.get("cells_parallel", 5)
        total_cells = cells_s * cells_p
        
        cell_cap = params.get("cell_capacity_ah", 4.0)
        cell_vol = params.get("cell_voltage_v", 3.7)
        
        chemistry = params.get("chemistry", "NMC811")
        anode = params.get("anode_material", "Graphite")
        housing = params.get("housing_material", "Aluminum")
        cooling = params.get("cooling_method", "Liquid")
        layout = params.get("pack_layout", "Modular")
        
        c_rate = params.get("max_charge_c_rate", 2.0)
        
        # 1. Capacity (kWh)
        pack_voltage = cells_s * cell_vol
        pack_capacity_ah = cells_p * cell_cap
        capacity_kwh = (pack_voltage * pack_capacity_ah) / 1000.0
        
        # 2. Weight (kg)
        cell_weight = cell_cap * 0.05 * self.chemistry_density.get(chemistry, 2.5)
        pack_cell_weight = total_cells * cell_weight
        housing_weight = 50 * self.housing_weight_factor.get(housing, 1.0)
        cooling_weight = 20 * (1.0 if cooling == "Liquid" else 0.5)
        weight_kg = pack_cell_weight + housing_weight + cooling_weight
        
        # 3. Cost (USD)
        cell_cost = capacity_kwh * self.chemistry_cost.get(chemistry, 120) * self.anode_factor.get(anode, 1.0)
        pack_overhead = 500 * self.layout_complexity.get(layout, 1.0)
        cost_usd = cell_cost + pack_overhead
        
        # 4. Energy Density (Wh/L and Wh/kg equivalent, using volumetric approx based on weight)
        volume_l = weight_kg * 0.8 # rough approx
        energy_density_wh_l = (capacity_kwh * 1000) / volume_l if volume_l > 0 else 0
        
        # 5. Max Temperature (C)
        # Heat generated roughly proportional to internal resistance and C-rate
        int_res = params.get("internal_resistance_mohm", 20.0) / 1000.0
        heat_gen = (c_rate * pack_capacity_ah)**2 * int_res * total_cells
        cooling_factor = self.cooling_efficiency.get(cooling, 0.5) * params.get("tim_conductivity_w_mk", 2.0)
        max_temperature_c = 25.0 + (heat_gen / (100 * cooling_factor))
        max_temperature_c = min(max_temperature_c, 120.0) # cap
        
        # 6. Cycle Life
        # Degrades with higher max temp, higher C-rate, and depends on chemistry
        base_life = 3000 if chemistry == "LFP" else 1500
        temp_penalty = max(0, max_temperature_c - 35) * 20
        c_rate_penalty = (c_rate - 1.0) * 100
        cycle_life_to_80_soh = max(300, base_life - temp_penalty - c_rate_penalty)
        
        # 7. Charging Time (10% to 80% SOC)
        soc_window = 0.7 # 80% - 10%
        ideal_time_h = soc_window / c_rate if c_rate > 0 else 10
        # Add thermal bottleneck penalty
        thermal_bottleneck = max(0, max_temperature_c - 45) / 10.0 
        charging_time_10_80_min = (ideal_time_h + thermal_bottleneck) * 60
        
        # 8. Carbon Footprint (kg CO2)
        # Driven by chemistry and total capacity
        co2_per_kwh = 100 if chemistry == "NMC811" else 80
        carbon_footprint_kg_co2 = capacity_kwh * co2_per_kwh * (1.2 if anode == "Silicon-Graphite" else 1.0)
        
        # 9. Manufacturing Complexity (scale 1-10)
        complexity = 3.0
        if layout == "Cell-to-Pack": complexity += 2.0
        if anode == "Lithium-Metal": complexity += 3.0
        if params.get("electrolyte", "Liquid") == "Solid-State": complexity += 4.0
        manufacturing_complexity = min(10.0, complexity)
        
        # 10. Safety Margin (scale 0-1)
        safety_score = 1.0
        if chemistry in ["NMC811", "NCA"]: safety_score -= 0.2
        if params.get("electrolyte") == "Solid-State": safety_score += 0.3
        if max_temperature_c > 60: safety_score -= 0.3
        if params.get("thermal_runaway_mitigation") == "Active": safety_score += 0.2
        safety_margin = max(0.0, min(1.0, safety_score))
        
        # 11. Range (km)
        # Assuming an average EV efficiency of 150 Wh/km
        range_km = (capacity_kwh * 1000) / 150.0
        
        # 12. Power Density (W/kg)
        # Power = Voltage * Max Current (C-rate * capacity)
        max_power_w = pack_voltage * (pack_capacity_ah * c_rate)
        power_density_w_kg = max_power_w / weight_kg if weight_kg > 0 else 0
        
        return {
            # Minimize objectives
            "weight_kg": float(weight_kg),
            "cost_usd": float(cost_usd),
            "max_temperature_c": float(max_temperature_c),
            "manufacturing_complexity": float(manufacturing_complexity),
            "carbon_footprint_kg_co2": float(carbon_footprint_kg_co2),
            "charging_time_10_80_min": float(charging_time_10_80_min),
            # Maximize objectives
            "capacity_kwh": float(capacity_kwh),
            "cycle_life_to_80_soh": float(cycle_life_to_80_soh),
            "energy_density_wh_l": float(energy_density_wh_l),
            "safety_margin": float(safety_margin),
            "range_km": float(range_km),
            "power_density_w_kg": float(power_density_w_kg)
        }

if __name__ == "__main__":
    # Test the simulator with default synthetic data
    sim = BatterySimulator()
    test_params = {
        "cells_series": 96, "cells_parallel": 5, "cell_capacity_ah": 5.0, 
        "cell_voltage_v": 3.7, "chemistry": "NMC811", "anode_material": "Graphite",
        "housing_material": "Aluminum", "cooling_method": "Liquid",
        "pack_layout": "Modular", "max_charge_c_rate": 2.0,
        "internal_resistance_mohm": 15.0, "tim_conductivity_w_mk": 3.0,
        "electrolyte": "Liquid", "thermal_runaway_mitigation": "Active"
    }
    results = sim.simulate(test_params)
    for k, v in results.items():
        print(f"{k}: {v:.2f}")
