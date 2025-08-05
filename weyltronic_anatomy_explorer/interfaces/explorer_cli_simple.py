"""
Simplified Interactive CLI for Weyltronic Explorer
Core functionality without complex features that were causing issues
"""

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint
import time
from typing import Dict, Any, List, Optional

from core.cells import WeyltonicCell
from core.tissues import WeyltonicTissue
from core.organs import VascularSystem, ProcessingSystem, SupportSystem
from genomics.genetic_code import GeneticProgram
from genomics.gene_expression import GeneExpressionEngine


class SimpleExplorerCLI:
    """Simplified command-line interface for the Weyltronic Explorer"""
    
    def __init__(self):
        self.console = Console()
        self.current_cell = None
        self.current_tissue = None
        self.current_organ_system = None
        self.expression_engine = GeneExpressionEngine()
        
    def run(self):
        """Main entry point"""
        self.show_welcome()
        
        while True:
            choice = self.main_menu()
            
            if choice == "Exit":
                self.console.print("\n[yellow]Thank you for exploring! Goodbye![/yellow]")
                break
            
            self.handle_choice(choice)
    
    def show_welcome(self):
        """Display welcome message"""
        self.console.print(Panel(
            "[bold cyan]Welcome to the Weyltronic Biological Computing Explorer![/bold cyan]\n\n"
            "Explore:\n"
            "• Living cells with FPGA organelles\n"
            "• Quantum information transport\n"
            "• Self-organizing tissues and organs\n"
            "• Genetic programming systems",
            title="🧬 Weyltronic Explorer 🧬",
            border_style="bold green"
        ))
    
    def main_menu(self) -> str:
        """Display main menu"""
        choices = [
            "Cell Explorer",
            "Tissue Builder", 
            "Organ Systems",
            "Genetic Programming",
            "Educational Mode",
            "Exit"
        ]
        
        return questionary.select(
            "What would you like to explore?",
            choices=choices
        ).ask()
    
    def handle_choice(self, choice: str):
        """Handle main menu choice"""
        if choice == "Cell Explorer":
            self.cell_explorer()
        elif choice == "Tissue Builder":
            self.tissue_builder()
        elif choice == "Organ Systems":
            self.organ_systems()
        elif choice == "Genetic Programming":
            self.genetic_programming()
        elif choice == "Educational Mode":
            self.educational_mode()
    
    def cell_explorer(self):
        """Explore cellular components"""
        self.console.print("\n[bold cyan]Cell Explorer[/bold cyan]")
        
        action = questionary.select(
            "Cell actions:",
            choices=["Create New Cell", "View Current Cell", "Cell Division", "Back"]
        ).ask()
        
        if action == "Create New Cell":
            cell_type = questionary.select(
                "Select cell type:",
                choices=["compute", "memory", "transport", "stem"]
            ).ask()
            
            self.current_cell = WeyltonicCell(
                cell_id=f"CELL-{int(time.time()) % 1000}",
                cell_type=cell_type
            )
            
            self.console.print(f"[green]Created {cell_type} cell: {self.current_cell.cell_id}[/green]")
            
        elif action == "View Current Cell" and self.current_cell:
            self.display_cell_info()
            
        elif action == "Cell Division" and self.current_cell:
            if self.current_cell.can_divide():
                daughter_cells = self.current_cell.divide()
                self.console.print(f"[green]Cell divided into {len(daughter_cells)} daughter cells![/green]")
            else:
                self.console.print("[red]Cell cannot divide (insufficient energy/health)[/red]")
    
    def display_cell_info(self):
        """Display current cell information"""
        if not self.current_cell:
            self.console.print("[red]No cell selected![/red]")
            return
        
        cell = self.current_cell
        
        # Create info table
        table = Table(title=f"Cell {cell.cell_id}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="yellow")
        
        table.add_row("Type", cell.cell_type)
        table.add_row("Specialization", cell.specialization or "None")
        table.add_row("Energy", f"{cell.energy_level:.1%}")
        table.add_row("Health", f"{cell.health:.1%}")
        table.add_row("Age", f"{cell.age} cycles")
        table.add_row("Organelles", str(len(cell.organelles)))
        
        self.console.print(table)
    
    def tissue_builder(self):
        """Build and explore tissues"""
        self.console.print("\n[bold cyan]Tissue Builder[/bold cyan]")
        
        action = questionary.select(
            "Tissue actions:",
            choices=["Create New Tissue", "Add Cells", "View Tissue", "Back"]
        ).ask()
        
        if action == "Create New Tissue":
            self.current_tissue = WeyltonicTissue(
                tissue_id=f"TISSUE-{int(time.time()) % 1000}"
            )
            self.console.print(f"[green]Created tissue: {self.current_tissue.tissue_id}[/green]")
            
        elif action == "Add Cells" and self.current_tissue:
            num_cells = questionary.text(
                "How many cells to add?",
                default="10"
            ).ask()
            
            try:
                count = int(num_cells)
                for i in range(count):
                    cell = WeyltonicCell(
                        cell_id=f"CELL-T{i}",
                        cell_type="stem"
                    )
                    self.current_tissue.add_cell(cell)
                
                self.console.print(f"[green]Added {count} cells to tissue[/green]")
            except ValueError:
                self.console.print("[red]Invalid number![/red]")
                
        elif action == "View Tissue" and self.current_tissue:
            self.display_tissue_info()
    
    def display_tissue_info(self):
        """Display tissue information"""
        if not self.current_tissue:
            self.console.print("[red]No tissue selected![/red]")
            return
        
        tissue = self.current_tissue
        
        panel = Panel(
            f"[bold]Tissue ID:[/bold] {tissue.tissue_id}\n"
            f"[bold]Cell Count:[/bold] {tissue.cell_count}\n"
            f"[bold]Specialization:[/bold] {tissue.specialization or 'None'}\n"
            f"[bold]Health:[/bold] {tissue.health:.1%}",
            title="Tissue Information",
            border_style="green"
        )
        
        self.console.print(panel)
    
    def organ_systems(self):
        """Explore organ systems"""
        self.console.print("\n[bold cyan]Organ Systems[/bold cyan]")
        
        organ_type = questionary.select(
            "Select organ system:",
            choices=["Vascular", "Processing", "Support", "Back"]
        ).ask()
        
        if organ_type == "Vascular":
            self.current_organ_system = VascularSystem("VASC-001")
        elif organ_type == "Processing":
            self.current_organ_system = ProcessingSystem("PROC-001")
        elif organ_type == "Support":
            self.current_organ_system = SupportSystem("SUPP-001")
        else:
            return
        
        if self.current_organ_system:
            self.console.print(f"[green]Created {organ_type} system[/green]")
            self.display_organ_info()
    
    def display_organ_info(self):
        """Display organ system information"""
        if not self.current_organ_system:
            return
        
        organ = self.current_organ_system
        
        self.console.print(Panel(
            f"[bold]System:[/bold] {organ.system_type}\n"
            f"[bold]ID:[/bold] {organ.system_id}\n"
            f"[bold]Tissues:[/bold] {len(organ.tissues)}\n"
            f"[bold]Capacity:[/bold] {organ.capacity:.1%}\n"
            f"[bold]Health:[/bold] {organ.health:.1%}",
            title="Organ System",
            border_style="blue"
        ))
    
    def genetic_programming(self):
        """Explore genetic programming"""
        self.console.print("\n[bold cyan]Genetic Programming[/bold cyan]")
        
        sample_program = '''
# Sample genetic program
GENE_START sample_cell
CONFIG fpga_mode: parallel_compute
CONFIG power_mode: balanced

EXPR activate: nucleus, mitochondria
EXPR enhance: processing_speed

TRAIT adaptive: true
GENE_END
        '''
        
        self.console.print(Panel(
            sample_program,
            title="Sample Genetic Program",
            border_style="magenta"
        ))
        
        action = questionary.select(
            "What would you like to do?",
            choices=["Load into cell", "Create new program", "Back"]
        ).ask()
        
        if action == "Load into cell" and self.current_cell:
            program = GeneticProgram(sample_program)
            if program.validate():
                self.current_cell.load_genetic_program(program)
                self.console.print("[green]Program loaded successfully![/green]")
            else:
                self.console.print("[red]Program validation failed![/red]")
    
    def educational_mode(self):
        """Educational information"""
        self.console.print("\n[bold cyan]Educational Mode[/bold cyan]")
        
        topics = [
            "What are Weyltronic Cells?",
            "How do Quantum Channels work?",
            "Understanding Organelles",
            "Tissue Formation",
            "Back"
        ]
        
        topic = questionary.select("Choose a topic:", choices=topics).ask()
        
        if topic == "What are Weyltronic Cells?":
            self.console.print(Panel(
                "Weyltronic cells are the fundamental units of biological computing.\n\n"
                "Each cell contains:\n"
                "• FPGA-based organelles for computation\n"
                "• Quantum channels for information transport\n"
                "• Genetic programs for configuration\n"
                "• Self-organizing capabilities",
                title="Weyltronic Cells",
                border_style="yellow"
            ))
        elif topic == "How do Quantum Channels work?":
            self.console.print(Panel(
                "Quantum channels use Weyl semimetal properties for:\n\n"
                "• Topologically protected information transport\n"
                "• Coherent quantum state transmission\n"
                "• Fault-tolerant communication\n"
                "• Self-healing pathways",
                title="Quantum Channels",
                border_style="yellow"
            ))
        elif topic == "Understanding Organelles":
            self.console.print(Panel(
                "Organelles are specialized FPGA units:\n\n"
                "• Nucleus: Central control and coordination\n"
                "• Mitochondria: Energy generation\n"
                "• Ribosomes: Protein synthesis (computation)\n"
                "• Golgi: Data packaging and transport\n"
                "• ER: Memory and storage",
                title="Organelles",
                border_style="yellow"
            ))
        elif topic == "Tissue Formation":
            self.console.print(Panel(
                "Tissues form through:\n\n"
                "• Cell aggregation and adhesion\n"
                "• Differentiation into specialized types\n"
                "• Emergent collective behaviors\n"
                "• Self-organization into functional units",
                title="Tissue Formation",
                border_style="yellow"
            ))


def main():
    """Main entry point"""
    cli = SimpleExplorerCLI()
    
    try:
        cli.run()
    except KeyboardInterrupt:
        cli.console.print("\n[yellow]Interrupted by user[/yellow]")
    except Exception as e:
        cli.console.print(f"\n[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
