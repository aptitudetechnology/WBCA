"""
Command-line interface for Weyltronic Biological Computing Explorer
"""

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from core.organelles import Nucleus, Ribosomes, Mitochondria
from utils.helpers import generate_cell_id

class WeyltonicExplorerCLI:
    """Interactive command-line interface for biological computing exploration"""
    
    def __init__(self, config):
        self.config = config
        self.console = Console()
        self.current_cell = None
        self.tutorial_mode = config.tutorial_mode
        
    def run(self):
        """Main CLI loop"""
        self.show_welcome()
        
        while True:
            choice = self.main_menu()
            
            if choice == "Create Cell":
                self.create_cell_wizard()
            elif choice == "Explore Organelles":
                self.explore_organelles()
            elif choice == "View Cell Status":
                self.view_cell_status()
            elif choice == "Tutorial Mode":
                self.tutorial_mode = not self.tutorial_mode
                self.console.print(f"Tutorial mode: {'ON' if self.tutorial_mode else 'OFF'}")
            elif choice == "Exit":
                break
                
        self.console.print("👋 Thank you for exploring biological computing!")
        
    def show_welcome(self):
        """Display welcome message"""
        welcome_text = """
🧬 Welcome to the Weyltronic Biological Computing Anatomy Explorer!

This educational tool helps you understand how biological computing differs 
from traditional computer architecture through interactive exploration of 
FPGA-based cellular units and quantum transport systems.

Key Concepts:
• Cells as reconfigurable computing units
• Organelles as specialized FPGA logic blocks  
• Quantum transport through Weyl semimetal channels
• Biological growth vs. engineered architecture
        """
        
        self.console.print(Panel(welcome_text, title="Weyltronic Explorer", border_style="green"))
        
    def main_menu(self):
        """Display main menu and get user choice"""
        choices = [
            "Create Cell",
            "Explore Organelles", 
            "View Cell Status",
            f"Tutorial Mode ({'ON' if self.tutorial_mode else 'OFF'})",
            "Exit"
        ]
        
        return questionary.select(
            "What would you like to explore?",
            choices=choices
        ).ask()
        
    def create_cell_wizard(self):
        """Interactive cell creation wizard"""
        self.console.print("\n🔬 Cell Creation Wizard")
        
        if self.tutorial_mode:
            self.console.print("""
[dim]Tutorial: A Weyltronic cell is like a tiny biological computer made of 
specialized organelles (FPGA blocks) that can reconfigure themselves based 
on genetic programs. Let's create your first cell![/dim]
            """)
            
        cell_id = generate_cell_id()
        
        # Select organelles
        available_organelles = self.config.get_organelle_types()
        selected_organelles = questionary.checkbox(
            "Select organelles for your cell:",
            choices=available_organelles
        ).ask()
        
        # Create the cell with selected organelles
        self.current_cell = self._create_cell_with_organelles(cell_id, selected_organelles)
        
        self.console.print(f"\n✅ Created cell: {cell_id}")
        self.console.print(f"Organelles: {', '.join(selected_organelles)}")
        
        if self.tutorial_mode:
            self.console.print("""
[dim]Your cell is now ready! Each organelle is implemented as FPGA logic blocks
that can be reconfigured dynamically. Try exploring the organelles next.[/dim]
            """)
    
    def _create_cell_with_organelles(self, cell_id, organelle_types):
        """Create a cell with specified organelles"""
        organelles = {}
        
        for org_type in organelle_types:
            if org_type == 'nucleus':
                organelles[org_type] = Nucleus(f"{cell_id}_{org_type}")
            elif org_type == 'ribosomes':
                organelles[org_type] = Ribosomes(f"{cell_id}_{org_type}")
            elif org_type == 'mitochondria':
                organelles[org_type] = Mitochondria(f"{cell_id}_{org_type}")
            # Add more organelle types as they're implemented
                
        return {
            'id': cell_id,
            'organelles': organelles,
            'energy': 100.0,
            'type': 'generic'
        }
        
    def explore_organelles(self):
        """Explore individual organelles"""
        if not self.current_cell:
            self.console.print("❌ No cell created yet. Please create a cell first.")
            return
            
        organelle_names = list(self.current_cell['organelles'].keys())
        
        if not organelle_names:
            self.console.print("❌ Current cell has no organelles.")
            return
            
        selected = questionary.select(
            "Which organelle would you like to explore?",
            choices=organelle_names + ["Back to main menu"]
        ).ask()
        
        if selected == "Back to main menu":
            return
            
        organelle = self.current_cell['organelles'][selected]
        self._display_organelle_details(organelle)
        
    def _display_organelle_details(self, organelle):
        """Display detailed information about an organelle"""
        status = organelle.get_status()
        
        table = Table(title=f"Organelle: {status['type']}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("ID", status['id'])
        table.add_row("Type", status['type'])
        table.add_row("FPGA Blocks", str(status['fpga_blocks']))
        table.add_row("Energy Consumption", f"{status['energy']:.1f}")
        table.add_row("Status", "Active" if status['active'] else "Inactive")
        
        self.console.print(table)
        
        if self.tutorial_mode:
            self._show_organelle_tutorial(status['type'])
            
    def _show_organelle_tutorial(self, organelle_type):
        """Show tutorial information for specific organelle types"""
        tutorials = {
            'Nucleus': """
[dim]Tutorial: The Nucleus acts as the configuration management center,
storing genetic programs and coordinating cellular reconfiguration.[/dim]
            """,
            'Ribosomes': """
[dim]Tutorial: Ribosomes compile genetic code into FPGA configurations,
acting like biological compilers that reconfigure other organelles.[/dim]
            """,
            'Mitochondria': """
[dim]Tutorial: Mitochondria manage power distribution and energy efficiency,
crucial for maintaining quantum coherence in biological systems.[/dim]
            """
        }
        
        if organelle_type in tutorials:
            self.console.print(tutorials[organelle_type])
            
    def view_cell_status(self):
        """Display current cell status"""
        if not self.current_cell:
            self.console.print("❌ No cell created yet.")
            return
            
        cell_panel = Panel(
            f"Cell ID: {self.current_cell['id']}\n"
            f"Type: {self.current_cell['type']}\n" 
            f"Energy: {self.current_cell['energy']:.1f}%\n"
            f"Organelles: {len(self.current_cell['organelles'])}",
            title="Current Cell Status",
            border_style="blue"
        )
        
        self.console.print(cell_panel)
