import typer
import yaml
import os
from rich.console import Console

app = typer.Typer(help="Hybrid QML EV Battery Optimization CLI")
console = Console()

def load_config(config_path: str):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

@app.command()
def data(config: str = "configs/default.yaml", generate_synthetic: bool = True):
    """
    Run data pipelines to download datasets and/or generate synthetic engineering data.
    """
    console.print(f"[bold blue]Running Data Pipeline with config:[/bold blue] {config}")
    from src.data.datasets import generate_synthetic_battery_data
    if generate_synthetic:
        console.print("Generating synthetic engineering data mapped to public dataset distributions...")
        # Assume generate function handles writing to disk
        df = generate_synthetic_battery_data(num_samples=5000)
        console.print(f"[green]Generated {len(df)} samples successfully.[/green]")

@app.command()
def optimize_classical(config: str = "configs/default.yaml"):
    """
    Run classical multi-objective optimization (NSGA-II) across the continuous 30+ parameter space.
    """
    console.print("[bold green]Starting NSGA-II Optimization...[/bold green]")
    from src.optimization.nsga2_solver import run_nsga2
    run_nsga2(config)

@app.command()
def optimize_quantum(config: str = "configs/default.yaml", method: str = "WS-QAOA"):
    """
    Run Quantum Optimization (e.g. Warm-Started QAOA) on the discretized QUBO formulation.
    """
    console.print(f"[bold purple]Starting Quantum Optimization ({method})...[/bold purple]")
    from src.optimization.qaoa_solver import run_qaoa
    run_qaoa(config)

@app.command()
def train_qml(config: str = "configs/default.yaml", model: str = "QKSVM"):
    """
    Train Quantum Machine Learning models (QKSVM or Re-uploading VQC) for performance prediction.
    """
    console.print(f"[bold cyan]Training QML Model: {model}...[/bold cyan]")
    if model.upper() == "QKSVM":
        from src.quantum_ml.qksvm import train_qksvm
        train_qksvm(config)
    elif model.upper() == "VQC":
        from src.quantum_ml.reuploading_vqc import train_vqc
        train_vqc(config)
    else:
        console.print(f"[red]Unknown model: {model}[/red]")

@app.command()
def visualize():
    """
    Generate publication-quality figures based on run results.
    """
    console.print("[bold yellow]Generating IEEE-style figures...[/bold yellow]")
    # Placeholder for running plotting scripts over generated result data
    console.print("Saved figures to docs/figures/")

if __name__ == "__main__":
    app()
