import sys
import os

# Add src to Python path so we can import the models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, BatteryChemistry, Reaction, Material

# We will connect to the postgres database using the DATABASE_URL environment variable,
# or default to the standard docker compose postgres URL for local execution.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/ev_battery_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_database():
    print("Creating tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    print("Clearing existing chemistry data...")
    db.query(Reaction).delete()
    db.query(BatteryChemistry).delete()
    db.query(Material).delete()
    
    print("Seeding elements and materials...")
    materials = [
        Material(name="Lithium", formula="Li", molar_mass=6.94, material_type="element", atomic_number=3, symbol="Li", oxidation_states="+1", abundance="0.0017%", supply_risk=7.5, toxicity="Low"),
        Material(name="Cobalt", formula="Co", molar_mass=58.93, material_type="element", atomic_number=27, symbol="Co", oxidation_states="+2, +3", abundance="0.0025%", supply_risk=9.0, toxicity="High"),
        Material(name="Nickel", formula="Ni", molar_mass=58.69, material_type="element", atomic_number=28, symbol="Ni", oxidation_states="+2, +3", abundance="0.0084%", supply_risk=6.5, toxicity="Moderate"),
        Material(name="Manganese", formula="Mn", molar_mass=54.94, material_type="element", atomic_number=25, symbol="Mn", oxidation_states="+2, +3, +4", abundance="0.1%", supply_risk=4.0, toxicity="Low"),
        Material(name="Iron", formula="Fe", molar_mass=55.84, material_type="element", atomic_number=26, symbol="Fe", oxidation_states="+2, +3", abundance="5.0%", supply_risk=1.0, toxicity="Low"),
        Material(name="Phosphorus", formula="P", molar_mass=30.97, material_type="element", atomic_number=15, symbol="P", oxidation_states="-3, +3, +5", abundance="0.1%", supply_risk=3.0, toxicity="Moderate"),
        Material(name="Sodium", formula="Na", molar_mass=22.99, material_type="element", atomic_number=11, symbol="Na", oxidation_states="+1", abundance="2.3%", supply_risk=1.0, toxicity="Low"),
        Material(name="Graphite", formula="C", molar_mass=12.01, material_type="anode", atomic_number=6, symbol="C", oxidation_states="-4, +2, +4", abundance="0.02%", supply_risk=5.0, toxicity="Low"),
        Material(name="Silicon", formula="Si", molar_mass=28.08, material_type="anode", atomic_number=14, symbol="Si", oxidation_states="-4, +4", abundance="27.7%", supply_risk=2.0, toxicity="Low")
    ]
    db.add_all(materials)

    print("Seeding Battery Chemistries...")
    
    lfp = BatteryChemistry(
        name="Lithium Iron Phosphate (LFP)",
        family="Lithium-ion",
        cathode="LiFePO4",
        anode="Graphite (C6)",
        electrolyte="LiPF6 in EC/DMC",
        separator="Polyolefin",
        nominal_voltage=3.2,
        specific_capacity=170.0,
        energy_density=160.0,
        power_density=2000.0,
        cycle_life=4000,
        efficiency=95.0,
        thermal_stability="Very High",
        safety_rating=9.5,
        advantages=["Excellent thermal stability", "High cycle life", "Cobalt-free (lower cost)", "Safer against thermal runaway"],
        disadvantages=["Lower energy density than NMC", "Poor low-temperature performance", "Flat voltage curve complicates SoC estimation"]
    )
    
    nmc = BatteryChemistry(
        name="Nickel Manganese Cobalt (NMC 811)",
        family="Lithium-ion",
        cathode="LiNi0.8Mn0.1Co0.1O2",
        anode="Graphite (C6) or Silicon-Graphite",
        electrolyte="LiPF6 in EC/DMC",
        separator="Polyethylene/Polypropylene",
        nominal_voltage=3.6,
        specific_capacity=200.0,
        energy_density=270.0,
        power_density=1500.0,
        cycle_life=2000,
        efficiency=96.0,
        thermal_stability="Moderate",
        safety_rating=7.0,
        advantages=["High energy density", "Good rate capability", "Versatile tuning (by changing Ni:Mn:Co ratios)"],
        disadvantages=["Relies on scarce Co and Ni", "Lower thermal stability than LFP", "Higher cost per kWh"]
    )
    
    nca = BatteryChemistry(
        name="Nickel Cobalt Aluminum (NCA)",
        family="Lithium-ion",
        cathode="LiNi0.85Co0.10Al0.05O2",
        anode="Graphite (C6)",
        electrolyte="LiPF6 in EC/DMC",
        separator="Polyolefin",
        nominal_voltage=3.6,
        specific_capacity=200.0,
        energy_density=260.0,
        power_density=1800.0,
        cycle_life=1500,
        efficiency=96.0,
        thermal_stability="Low",
        safety_rating=6.5,
        advantages=["Very high specific energy", "Good specific power", "Long lifecycle if managed thermally"],
        disadvantages=["High cost due to Cobalt", "Requires sophisticated thermal management", "Lower safety margins"]
    )

    solid_state = BatteryChemistry(
        name="Solid-State Lithium-Metal",
        family="Solid-State",
        cathode="NMC or NCA",
        anode="Lithium Metal (Li)",
        electrolyte="Solid Ceramic (LLZO) or Polymer",
        separator="None (Electrolyte acts as separator)",
        nominal_voltage=3.8,
        specific_capacity=3860.0,  # Li-metal theoretical anode capacity
        energy_density=400.0,
        power_density=1000.0,
        cycle_life=1000,
        efficiency=98.0,
        thermal_stability="High",
        safety_rating=8.5,
        advantages=["Eliminates flammable liquid electrolytes", "Allows use of lithium metal anode", "Massively increased energy density"],
        disadvantages=["High manufacturing complexity", "Solid-solid interface resistance", "Dendrite formation challenges"]
    )

    na_ion = BatteryChemistry(
        name="Sodium-ion (Na-ion)",
        family="Sodium-ion",
        cathode="Na(Ni,Fe,Mn)O2",
        anode="Hard Carbon",
        electrolyte="NaPF6 in PC",
        separator="Glass fiber or Polyolefin",
        nominal_voltage=3.1,
        specific_capacity=140.0,
        energy_density=140.0,
        power_density=1200.0,
        cycle_life=3000,
        efficiency=92.0,
        thermal_stability="High",
        safety_rating=8.0,
        advantages=["Sodium is universally abundant", "Significantly lower material cost", "Good cold-temperature performance", "Can be discharged to 0V for safe transport"],
        disadvantages=["Lower energy density than Li-ion", "Heavier atoms (lower specific energy)", "Supply chain still maturing"]
    )
    
    db.add_all([lfp, nmc, nca, solid_state, na_ion])
    db.commit()

    print("Seeding Reactions...")
    reactions = [
        Reaction(
            chemistry_id=lfp.id,
            reaction_type="discharge_cathode",
            equation="FePO4 + Li+ + e- -> LiFePO4",
            electrons_transferred=1,
            description="Lithium ions intercalate into the iron phosphate structure, reducing Fe3+ to Fe2+."
        ),
        Reaction(
            chemistry_id=lfp.id,
            reaction_type="discharge_anode",
            equation="LiC6 -> C6 + Li+ + e-",
            electrons_transferred=1,
            description="Lithium de-intercalates from the graphite layers."
        ),
        Reaction(
            chemistry_id=nmc.id,
            reaction_type="discharge_cathode",
            equation="Li(1-x)Ni0.8Mn0.1Co0.1O2 + xLi+ + xe- -> LiNi0.8Mn0.1Co0.1O2",
            electrons_transferred=1,
            description="Lithium intercalates into the layered oxide, reducing Ni and Co."
        ),
        Reaction(
            chemistry_id=nmc.id,
            reaction_type="discharge_anode",
            equation="LiC6 -> C6 + Li+ + e-",
            electrons_transferred=1,
            description="Standard graphite anode de-intercalation."
        ),
        Reaction(
            chemistry_id=solid_state.id,
            reaction_type="discharge_anode",
            equation="Li -> Li+ + e-",
            electrons_transferred=1,
            description="Stripping of pure lithium metal at the anode."
        ),
        Reaction(
            chemistry_id=na_ion.id,
            reaction_type="discharge_cathode",
            equation="Na(1-x)MO2 + xNa+ + xe- -> NaMO2",
            electrons_transferred=1,
            description="Sodium ions intercalate into the transition metal oxide layer."
        )
    ]
    db.add_all(reactions)
    db.commit()

    print("Database seeding complete!")

if __name__ == "__main__":
    seed_database()
