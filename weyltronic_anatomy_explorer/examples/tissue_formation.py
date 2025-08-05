#!/usr/bin/env python3
"""
Tissue Formation Example - Demonstrates tissue growth and development
Shows how cells aggregate, specialize, and form functional tissues
"""

import sys
sys.path.append('..')

from core.cells import WeyltonicCell
from core.tissues import WeyltonicTissue
from genomics.genetic_code import GeneticProgram
from genomics.gene_expression import GeneExpressionEngine
from visualization.tissue_development import TissueDevelopmentVisualizer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
import time
import random


console = Console()


def create_stem_cells(count: int = 5):
    """Create initial stem cells for tissue formation"""
    console.print(f"\n[bold cyan]Creating {count} stem cells...[/bold cyan]")
    
    stem_cells = []
    
    # Basic stem cell genetic program
    stem_program = """
    # Stem cell program - can differentiate into any type
    GENE_START stem_cell_base
    CONFIG fpga_mode: flexible
    CONFIG differentiation_potential: high
    
    EXPR maintain: all_organelles
    EXPR regulate: differentiation_factors
    
    TRAIT pluripotent: true
    TRAIT high_division_rate: true
    GENE_END
    """
    
    program = GeneticProgram(stem_program)
    
    for i in range(count):
        cell = WeyltonicCell(cell_id=f"STEM-{i:03d}", cell_type="stem")
        if program.validate():
            cell.load_genetic_program(program)
        stem_cells.append(cell)
    
    console.print(f"[green]✓ Created {len(stem_cells)} stem cells[/green]")
    return stem_cells


def demonstrate_tissue_formation():
    """Demonstrate tissue formation from stem cells"""
    console.print("\n[bold green]Tissue Formation Demonstration[/bold green]")
    
    # Create initial stem cells
    stem_cells = create_stem_cells(10)
    
    # Create tissue with stem cells
    tissue = WeyltonicTissue(tissue_id="TISSUE-001")
    
    console.print("\n[bold cyan]Phase 1: Cell Aggregation[/bold cyan]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Aggregating cells...", total=len(stem_cells))
        
        for cell in stem_cells:
            tissue.add_cell(cell)
            progress.update(task, advance=1)
            time.sleep(0.1)
    
    console.print(f"[green]✓ Tissue contains {tissue.cell_count} cells[/green]")
    
    # Phase 2: Differentiation
    console.print("\n[bold cyan]Phase 2: Cell Differentiation[/bold cyan]")
    
    # Create gene expression engine
    expression_engine = GeneExpressionEngine()
    
    # Define differentiation pattern
    cell_types = ['compute', 'memory', 'transport', 'structural']
    type_ratios = [0.3, 0.3, 0.2, 0.2]  # Desired ratios
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Differentiating cells...", total=tissue.cell_count)
        
        for i, cell in enumerate(tissue.cells.values()):
            # Determine cell fate based on ratios
            fate = random.choices(cell_types, weights=type_ratios)[0]
            
            # Apply differentiation
            diff_program = f"""
            # Differentiation program for {fate} cell
            GENE_START differentiate_{fate}
            CONFIG target_type: {fate}
            EXPR activate: {fate}_specific_genes
            EXPR suppress: stem_cell_genes
            GENE_END
            """
            
            program = GeneticProgram(diff_program)
            if program.validate():
                cell.load_genetic_program(program)
                cell.specialize(fate)
            
            progress.update(task, advance=1)
            time.sleep(0.05)
    
    # Show differentiation results
    show_tissue_composition(tissue)
    
    # Phase 3: Tissue Specialization
    console.print("\n[bold cyan]Phase 3: Tissue Specialization[/bold cyan]")
    
    tissue.specialize("processing")
    console.print("[green]✓ Tissue specialized for processing[/green]")
    
    # Phase 4: Growth Simulation
    console.print("\n[bold cyan]Phase 4: Growth Simulation[/bold cyan]")
    
    growth_cycles = 5
    for cycle in range(growth_cycles):
        console.print(f"\n[yellow]Growth Cycle {cycle + 1}:[/yellow]")
        
        # Simulate growth
        growth_result = tissue.grow(
            growth_factor=1.2,
            resource_availability=0.8,
            stress_level=0.1
        )
        
        console.print(f"  New cells: {growth_result['new_cells']}")
        console.print(f"  Dead cells: {growth_result['dead_cells']}")
        console.print(f"  Total cells: {tissue.cell_count}")
        console.print(f"  Tissue health: {tissue.health:.1%}")
        
        time.sleep(0.5)
    
    return tissue


def show_tissue_composition(tissue: WeyltonicTissue):
    """Display tissue composition analysis"""
    console.print("\n[bold]Tissue Composition Analysis[/bold]")
    
    # Count cell types
    type_counts = {}
    for cell in tissue.cells.values():
        cell_type = cell.specialization or cell.cell_type
        type_counts[cell_type] = type_counts.get(cell_type, 0) + 1
    
    # Create composition table
    table = Table(title="Cell Type Distribution")
    table.add_column("Cell Type", style="cyan")
    table.add_column("Count", style="magenta")
    table.add_column("Percentage", style="yellow")
    
    total_cells = sum(type_counts.values())
    for cell_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_cells) * 100
        table.add_row(
            cell_type,
            str(count),
            f"{percentage:.1f}%"
        )
    
    console.print(table)


def demonstrate_tissue_function(tissue: WeyltonicTissue):
    """Demonstrate tissue-level functions"""
    console.print("\n[bold cyan]Tissue Function Demonstration[/bold cyan]")
    
    # Execute tissue function based on specialization
    console.print(f"\nExecuting {tissue.specialization} tissue function...")
    
    for i in range(3):
        result = tissue.execute_tissue_function({
            'function': 'process_data',
            'input': f'data_batch_{i}',
            'priority': 'high'
        })
        
        if result['success']:
            console.print(f"  ✓ Function executed successfully")
            console.print(f"    Output: {result.get('output', 'processed')}")
            console.print(f"    Cells involved: {result.get('cells_involved', 'multiple')}")
        else:
            console.print(f"  ✗ Function failed: {result.get('error', 'Unknown')}")
        
        time.sleep(0.5)


def visualize_tissue_development(tissue: WeyltonicTissue):
    """Visualize tissue development (placeholder)"""
    console.print("\n[bold cyan]Tissue Development Visualization[/bold cyan]")
    
    visualizer = TissueDevelopmentVisualizer()
    
    console.print("[yellow]Note: Visualization would appear here in full implementation[/yellow]")
    
    # Show development summary
    dev_panel = Panel(
        f"[bold]Tissue ID:[/bold] {tissue.tissue_id}\n"
        f"[bold]Total Cells:[/bold] {tissue.cell_count}\n"
        f"[bold]Specialization:[/bold] {tissue.specialization}\n"
        f"[bold]Development Stage:[/bold] Mature\n"
        f"[bold]Structural Integrity:[/bold] {tissue.health:.1%}\n"
        f"[bold]Functional Capacity:[/bold] {random.uniform(0.8, 0.95):.1%}",
        title="Tissue Development Summary",
        border_style="green"
    )
    console.print(dev_panel)


def interactive_tissue_explorer():
    """Interactive tissue formation and exploration"""
    console.print("\n[bold green]Interactive Tissue Explorer[/bold green]")
    
    tissue = None
    
    while True:
        console.print("\n[bold]Options:[/bold]")
        console.print("1. Form New Tissue")
        console.print("2. View Tissue Composition")
        console.print("3. Demonstrate Tissue Function")
        console.print("4. Simulate Growth")
        console.print("5. Visualize Development")
        console.print("6. Exit")
        
        if tissue:
            console.print(f"\n[dim]Current tissue: {tissue.tissue_id} ({tissue.cell_count} cells)[/dim]")
        
        choice = console.input("\n[cyan]Select option (1-6): [/cyan]")
        
        if choice == '1':
            tissue = demonstrate_tissue_formation()
        elif choice == '2':
            if tissue:
                show_tissue_composition(tissue)
            else:
                console.print("[red]No tissue formed yet![/red]")
        elif choice == '3':
            if tissue:
                demonstrate_tissue_function(tissue)
            else:
                console.print("[red]No tissue formed yet![/red]")
        elif choice == '4':
            if tissue:
                console.print("\n[cyan]Simulating tissue growth...[/cyan]")
                growth_result = tissue.grow(
                    growth_factor=1.3,
                    resource_availability=0.9,
                    stress_level=0.05
                )
                console.print(f"[green]Growth complete: +{growth_result['new_cells']} cells[/green]")
            else:
                console.print("[red]No tissue formed yet![/red]")
        elif choice == '5':
            if tissue:
                visualize_tissue_development(tissue)
            else:
                console.print("[red]No tissue formed yet![/red]")
        elif choice == '6':
            console.print("[yellow]Exiting Tissue Explorer[/yellow]")
            break
        else:
            console.print("[red]Invalid option[/red]")


def main():
    """Main entry point"""
    console.rule("[bold blue]Weyltronic Tissue Formation Example[/bold blue]")
    
    console.print("""
    Welcome to the Tissue Formation Example!
    
    This example demonstrates:
    • Creating stem cells and forming tissues
    • Cell differentiation and specialization
    • Tissue growth and development
    • Emergent tissue-level functions
    • Basic visualization of tissue structure
    
    Watch as individual cells come together to form
    functional biological computing tissues!
    
    [italic]Note: Visualizations are placeholders in this demo.[/italic]
    """)
    
    try:
        interactive_tissue_explorer()
    except KeyboardInterrupt:
        console.print("\n[yellow]Explorer interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
    
    console.rule("[bold blue]Thank you for exploring tissue formation![/bold blue]")


if __name__ == "__main__":
    main()
