FARADAY_CONSTANT = 96485.3321  # C/mol or As/mol

def calculate_theoretical_specific_capacity(electrons_transferred: int, molar_mass_g_mol: float) -> float:
    """
    Calculate theoretical specific capacity in mAh/g based on Faraday's law.
    Q = n * F / (3.6 * M)
    """
    if molar_mass_g_mol <= 0:
        raise ValueError("Molar mass must be greater than 0.")
    if electrons_transferred <= 0:
        raise ValueError("Electrons transferred must be greater than 0.")
        
    return (electrons_transferred * FARADAY_CONSTANT) / (3.6 * molar_mass_g_mol)

def calculate_energy(voltage_v: float, capacity_ah: float) -> float:
    """ Energy in Wh = Voltage * Capacity """
    if voltage_v < 0 or capacity_ah < 0:
        raise ValueError("Voltage and capacity cannot be negative.")
    return voltage_v * capacity_ah

def calculate_specific_energy(voltage_v: float, capacity_ah: float, mass_kg: float) -> float:
    """ Specific Energy in Wh/kg """
    if mass_kg <= 0:
        raise ValueError("Mass must be greater than 0.")
    energy_wh = calculate_energy(voltage_v, capacity_ah)
    return energy_wh / mass_kg

def estimate_charging_time(capacity_ah: float, current_a: float, efficiency: float = 0.95) -> float:
    """ Returns charging time in hours. """
    if current_a <= 0:
        raise ValueError("Charging current must be greater than 0.")
    if not (0 < efficiency <= 1.0):
        raise ValueError("Efficiency must be between 0 and 1.0")
    
    # Time = Capacity / (Current * Efficiency)
    return capacity_ah / (current_a * efficiency)

def get_current_from_c_rate(capacity_ah: float, c_rate: float) -> float:
    """ Calculate required current in Amps for a given C-rate. """
    if c_rate <= 0 or capacity_ah < 0:
        raise ValueError("Capacity and C-rate must be positive.")
    return capacity_ah * c_rate
