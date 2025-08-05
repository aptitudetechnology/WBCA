"""
Interactive Command-Line Interface for Weyltronic Explorer
Simplified implementation with core functionality
"""

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
import time
from typing import Dict, Any, List, Optional

from core.cells import WeyltonicCell
from core.tissues import WeyltonicTissue
from core.organs import VascularSystem, ProcessingSystem, SupportSystem
from genomics.genetic_code import GeneticProgram
from genomics.gene_expression import GeneExpressionEngine


class ExplorerCLI:
    """
    Simplified command-line interface for the Weyltronic Explorer.
    Provides interactive menus for exploration and learning.
    """
    
    def __init__(self):
        self.console = Console()
        self.current_cell = None
        self.current_tissue = None
        self.current_organ_system = None
        self.expression_engine = GeneExpressionEngine()
        
    def run(self):
        """Main entry point for the CLI"""
        self.show_welcome()
        
        while True:
            choice = self.main_menu()
            
            if choice == "exit":
                self.console.print("[yellow]Thank you for exploring! Goodbye![/yellow]")
                break
            
            self.handle_menu_choice(choice)
    
    def show_welcome(self):
        """Display welcome message"""
        welcome_text = """
        Welcome to the Weyltronic Biological Computing Anatomy Explorer!
        
        Explore the fascinating world of biological computing through:
        • Living cells with FPGA-based organelles
        • Quantum coherent information transport
        • Self-organizing tissues and organs
        • Genetic programming and evolution
        
        Let's begin your journey!
        """
        
        self.console.print(Panel(
            Text(welcome_text, justify="center", style="cyan"),
            title="🧬 Weyltronic Explorer 🧬",
            border_style="bold green"
        ))
        
        while True:
            choice = questionary.select(
                "What would you like to explore?",
                choices=[
                    "🔬 Cell Anatomy Basics",
                    "🧪 Create & Configure Cell",
                    "🔗 Tissue Formation",
                    "🏗️  Organ Systems",
                    "⚛️  Quantum Transport",
                    "🧬 Genetic Programming",
                    "📊 System Comparisons",
                    "📚 Educational Tutorials",
                    "📈 View Current Status",
                    "❌ Exit"
                ],
                style=questionary.Style([
                    ('question', 'bold'),
                    ('pointer', 'fg:#00aa00'),
                    ('choice', 'fg:#0088ff'),
                ])
            ).ask()
            
            if choice is None or "Exit" in choice:
                self.console.print("Thank you for exploring! 🌟", style="bold green")
                break
            elif "Cell Anatomy" in choice:
                self.explore_cell_anatomy()
            elif "Create & Configure" in choice:
                self.create_configure_cell_wizard()
            elif "Tissue Formation" in choice:
                self.explore_tissue_formation()
            elif "Organ Systems" in choice:
                self.explore_organ_systems()
            elif "Quantum Transport" in choice:
                self.explore_quantum_transport()
            elif "Genetic Programming" in choice:
                self.explore_genetic_programming()
            elif "System Comparisons" in choice:
                self.compare_architectures()
            elif "Educational Tutorials" in choice:
                self.educational_tutorials()
            elif "View Current Status" in choice:
                self.view_system_status()
    
    def explore_cell_anatomy(self):
        """Educational exploration of cell anatomy basics"""
        self.console.print(Panel(
            "🔬 Cell Anatomy Basics\n\n"
            "Welcome to the foundational unit of biological computing!\n"
            "Each WeyltonicCell contains FPGA-based organelles that can be\n"
            "dynamically reconfigured based on genetic programs.",
            title="Cell Anatomy Explorer",
            border_style="blue"
        ))
        
        if not self.current_cell:
            create_demo = questionary.confirm(
                "No cell is currently loaded. Create a demo cell?"
            ).ask()
            
            if create_demo:
                self.current_cell = WeyltonicCell("demo_cell")
                self.current_cell.specialize("compute")
                self.console.print("✅ Created demo computational cell!", style="green")
        
        while True:
            choice = questionary.select(
                "What aspect of cell anatomy would you like to explore?",
                choices=[
                    "📋 View Organelle Overview",
                    "⚙️  Inspect Individual Organelles",
                    "🔄 Watch Cell Cycle",
                    "🧬 Load Genetic Program",
                    "⬅️  Back to Main Menu"
                ]
            ).ask()
            
            if choice is None or "Back" in choice:
                break
            elif "Organelle Overview" in choice:
                self.show_organelle_overview()
            elif "Inspect Individual" in choice:
                self.inspect_organelles()
            elif "Watch Cell Cycle" in choice:
                self.demonstrate_cell_cycle()
            elif "Load Genetic" in choice:
                self.load_genetic_program_interactive()
    
    def show_organelle_overview(self):
        """Show overview of all organelles in current cell"""
        if not self.current_cell:
            self.console.print("❌ No cell loaded!", style="red")
            return
            
        table = Table(title=f"Organelles in {self.current_cell.cell_id}")
        table.add_column("Organelle", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Active", style="yellow")
        table.add_column("Energy", style="magenta")
        table.add_column("Configuration", style="blue")
        
        for name, organelle in self.current_cell.organelles.items():
            status = organelle.get_status()
            table.add_row(
                name.title(),
                status['type'],
                "✅" if status['active'] else "❌",
                f"{status['energy']:.1f}",
                str(len(status['configuration'])) + " params"
            )
        
        self.console.print(table)
        
        # Show cell-level stats
        cell_status = self.current_cell.get_status()
        self.console.print(f"\n📊 Cell Health: {cell_status['health']:.1f}%")
        self.console.print(f"⚡ Energy Level: {cell_status['energy_level']:.1f}%")
        self.console.print(f"🎯 Specialization: {cell_status['specialization']}")
        self.console.print(f"👥 Neighbors: {cell_status['neighbor_count']}")
        
        questionary.press_any_key("Press any key to continue...").ask()
    
    def inspect_organelles(self):
        """Allow detailed inspection of individual organelles"""
        if not self.current_cell:
            self.console.print("❌ No cell loaded!", style="red")
            return
        
        organelle_choices = list(self.current_cell.organelles.keys()) + ["⬅️ Back"]
        
        choice = questionary.select(
            "Which organelle would you like to inspect?",
            choices=organelle_choices
        ).ask()
        
        if choice and choice != "⬅️ Back":
            organelle = self.current_cell.organelles[choice]
            status = organelle.get_status()
            
            # Create detailed organelle panel
            detail_text = f"""
🔬 {choice.title()} Details

Type: {status['type']}
Status: {'🟢 Active' if status['active'] else '🔴 Inactive'}
Energy Consumption: {status['energy']:.2f} units
FPGA Blocks: {status['fpga_blocks']}

Configuration Parameters:
"""
            
            for key, value in status['configuration'].items():
                detail_text += f"  • {key}: {value}\n"
            
            # Add organelle-specific information
            if hasattr(organelle, 'processing_power'):
                detail_text += f"\n⚡ Processing Power: {organelle.processing_power}"
            if hasattr(organelle, 'capacity'):
                detail_text += f"\n💾 Capacity: {organelle.capacity}"
            if hasattr(organelle, 'efficiency'):
                detail_text += f"\n📈 Efficiency: {organelle.efficiency}"
            
            self.console.print(Panel(detail_text, title=f"{choice.title()} Inspector", border_style="cyan"))
            
            # Offer to reconfigure
            if questionary.confirm("Would you like to modify this organelle?").ask():
                self.reconfigure_organelle_interactive(choice, organelle)
    
    def reconfigure_organelle_interactive(self, organelle_name: str, organelle):
        """Interactive organelle reconfiguration"""
        self.console.print(f"🔧 Reconfiguring {organelle_name}...")
        
        new_config = {}
        
        # Allow modification of specific parameters based on organelle type
        if organelle_name == 'chloroplast':
            if questionary.confirm("Modify processing power?").ask():
                power = questionary.text(
                    f"Enter new processing power (current: {getattr(organelle, 'processing_power', 5.0)}):",
                    validate=lambda x: x.replace('.', '').isdigit()
                ).ask()
                new_config['processing_power'] = float(power)
                
        elif organelle_name == 'vacuole':
            if questionary.confirm("Modify storage capacity?").ask():
                capacity = questionary.text(
                    f"Enter new capacity (current: {getattr(organelle, 'capacity', 100.0)}):",
                    validate=lambda x: x.replace('.', '').isdigit()
                ).ask()
                new_config['capacity'] = float(capacity)
        
        if new_config:
            organelle.reconfigure(new_config)
            self.console.print(f"✅ Reconfigured {organelle_name}!", style="green")
        else:
            self.console.print("No changes made.", style="yellow")
    
    def demonstrate_cell_cycle(self):
        """Demonstrate a cell cycle with live updates"""
        if not self.current_cell:
            self.console.print("❌ No cell loaded!", style="red")
            return
        
        self.console.print("🔄 Starting cell cycle demonstration...")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Processing cell cycle...", total=10)
            
            for i in range(10):
                # Execute cell cycle
                result = self.current_cell.execute_cycle({
                    'light_data': 1.0 + i * 0.1,
                    'nutrients': 0.8
                })
                
                progress.update(task, advance=1, 
                              description=f"Cycle {i+1}: Energy {self.current_cell.energy_level:.1f}%")
                time.sleep(0.5)
        
        # Show results
        status = self.current_cell.get_status()
        self.console.print(f"\n📊 Final Cell Status:")
        self.console.print(f"Health: {status['health']:.1f}%")
        self.console.print(f"Energy: {status['energy_level']:.1f}%")
        self.console.print(f"Age: {status['age']} cycles")
        
        if status['can_divide']:
            self.console.print("🎉 Cell is ready for division!", style="bold green")
        
        questionary.press_any_key("Press any key to continue...").ask()
    
    def create_configure_cell_wizard(self):
        """Guided wizard to create and configure a cell"""
        self.console.print(Panel(
            "🧪 Cell Creation Wizard\n\n"
            "Let's create a new WeyltonicCell and configure it for specific tasks!",
            title="Cell Creator",
            border_style="green"
        ))
        
        # Get cell ID
        cell_id = questionary.text(
            "Enter a unique ID for your new cell:",
            default=f"cell_{int(time.time()) % 10000}"
        ).ask()
        
        if not cell_id:
            self.console.print("❌ Cell creation cancelled.", style="red")
            return
        
        # Create the cell
        self.current_cell = WeyltonicCell(cell_id)
        self.console.print(f"✅ Created cell '{cell_id}'!", style="green")
        
        # Choose specialization
        specialization = questionary.select(
            "What type of cell would you like to create?",
            choices=[
                "compute - High-performance processing",
                "memory - Data storage and retention", 
                "transport - Information routing",
                "sensory - Environmental detection",
                "generic - No specialization"
            ]
        ).ask()
        
        if specialization and specialization != "generic":
            spec_type = specialization.split(' -')[0]
            self.current_cell.specialize(spec_type)
            self.console.print(f"🎯 Specialized as {spec_type} cell!", style="blue")
        
        # Load genetic program
        program_choice = questionary.select(
            "Select a genetic program to load:",
            choices=list(self.sample_programs.keys()) + ["Skip genetic program"]
        ).ask()
        
        if program_choice and program_choice != "Skip genetic program":
            program = self.sample_programs[program_choice]
            self.current_cell.load_genetic_program(program_choice, program.__dict__)
            self.console.print(f"🧬 Loaded genetic program '{program_choice}'!", style="magenta")
        
        # Show final cell status
        self.show_organelle_overview()
        
        # Ask about further actions
        next_action = questionary.select(
            "What would you like to do next?",
            choices=[
                "🔄 Run cell cycles",
                "🧬 Modify genetic program",
                "🔬 Inspect organelles",
                "✨ Create tissue from this cell",
                "⬅️  Return to main menu"
            ]
        ).ask()
        
        if "Run cell cycles" in next_action:
            self.demonstrate_cell_cycle()
        elif "Modify genetic" in next_action:
            self.load_genetic_program_interactive()
        elif "Inspect organelles" in next_action:
            self.inspect_organelles()
        elif "Create tissue" in next_action:
            self.create_tissue_from_cell()
    
    def create_tissue_from_cell(self):
        """Create a tissue using the current cell as a template"""
        if not self.current_cell:
            self.console.print("❌ No cell to use as template!", style="red")
            return
        
        tissue_type = questionary.select(
            "What type of tissue would you like to create?",
            choices=["computational", "storage", "transport", "sensory", "generic"]
        ).ask()
        
        size = questionary.text(
            "How many cells should the tissue contain? (1-20)",
            default="5",
            validate=lambda x: x.isdigit() and 1 <= int(x) <= 20
        ).ask()
        
        if tissue_type and size:
            self.current_tissue = WeyltonicTissue(tissue_type=tissue_type)
            
            # Add the current cell
            self.current_tissue.add_cell(self.current_cell)
            
            # Create additional cells
            for i in range(int(size) - 1):
                new_cell = WeyltonicCell(f"{self.current_cell.cell_id}_clone_{i}")
                new_cell.specialize(self.current_cell.specialization)
                if self.current_cell.current_program:
                    new_cell.load_genetic_program(
                        self.current_cell.current_program,
                        self.current_cell.organelles['nucleus'].genetic_programs.get(
                            self.current_cell.current_program, {}
                        )
                    )
                self.current_tissue.add_cell(new_cell)
            
            self.console.print(f"✅ Created {tissue_type} tissue with {size} cells!", style="green")
            
            # Show tissue status
            status = self.current_tissue.get_tissue_status()
            self.console.print(f"📊 Tissue Status:")
            self.console.print(f"  Cells: {status['cell_count']}")
            self.console.print(f"  Health: {status['average_health']:.1f}%")
            self.console.print(f"  Energy: {status['average_energy']:.1f}%")
    
    def explore_tissue_formation(self):
        """Explore tissue formation and multi-cellular coordination"""
        self.console.print(Panel(
            "🔗 Tissue Formation Explorer\n\n"
            "Explore how individual cells organize into specialized tissues\n"
            "and coordinate their activities for emergent functions.",
            title="Tissue Explorer",
            border_style="blue"
        ))
        
        if not self.current_tissue:
            if questionary.confirm("No tissue loaded. Create a demo tissue?").ask():
                self.create_demo_tissue()
        
        while True:
            choice = questionary.select(
                "What aspect of tissue biology would you like to explore?",
                choices=[
                    "📊 View Tissue Status",
                    "🧪 Tissue Function Test",
                    "📈 Growth Simulation",
                    "🔗 Cell Communication",
                    "⬅️  Back to Main Menu"
                ]
            ).ask()
            
            if choice is None or "Back" in choice:
                break
            elif "View Tissue Status" in choice:
                self.show_tissue_status()
            elif "Function Test" in choice:
                self.test_tissue_function()
            elif "Growth Simulation" in choice:
                self.simulate_tissue_growth()
            elif "Cell Communication" in choice:
                self.demonstrate_cell_communication()
    
    def create_demo_tissue(self):
        """Create a demonstration tissue"""
        tissue_type = questionary.select(
            "What type of demo tissue?",
            choices=["computational", "storage", "transport"]
        ).ask()
        
        self.current_tissue = WeyltonicTissue(tissue_type=tissue_type)
        
        # Create demo cells
        for i in range(3):
            cell = WeyltonicCell(f"demo_{tissue_type}_{i}")
            cell.specialize({"computational": "compute", "storage": "memory", "transport": "transport"}[tissue_type])
            self.current_tissue.add_cell(cell)
        
        self.console.print(f"✅ Created demo {tissue_type} tissue!", style="green")
    
    def show_tissue_status(self):
        """Display comprehensive tissue status"""
        if not self.current_tissue:
            self.console.print("❌ No tissue loaded!", style="red")
            return
        
        status = self.current_tissue.get_tissue_status()
        
        table = Table(title=f"Tissue Status: {status['tissue_id']}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Type", status['tissue_type'])
        table.add_row("Cell Count", str(status['cell_count']))
        table.add_row("Average Health", f"{status['average_health']:.1f}%")
        table.add_row("Average Energy", f"{status['average_energy']:.1f}%")
        table.add_row("Storage Capacity", f"{status['total_storage_capacity']:.0f}")
        table.add_row("Network Connections", str(status['network_connections']))
        
        self.console.print(table)
        
        # Show individual cells
        if questionary.confirm("Show individual cell details?").ask():
            cell_table = Table(title="Individual Cells")
            cell_table.add_column("Cell ID", style="cyan")
            cell_table.add_column("Health", style="green")
            cell_table.add_column("Energy", style="yellow")
            cell_table.add_column("Specialization", style="magenta")
            cell_table.add_column("Position", style="blue")
            
            for cell_info in status['cells']:
                cell_table.add_row(
                    cell_info['id'],
                    f"{cell_info['health']:.1f}%",
                    f"{cell_info['energy']:.1f}%",
                    cell_info['specialization'],
                    str(cell_info['position'])
                )
            
            self.console.print(cell_table)
    
    def test_tissue_function(self):
        """Test the tissue's specialized function"""
        if not self.current_tissue:
            self.console.print("❌ No tissue loaded!", style="red")
            return
        
        self.console.print(f"🧪 Testing {self.current_tissue.tissue_type} tissue function...")
        
        # Prepare test inputs based on tissue type
        if self.current_tissue.tissue_type == "computational":
            test_input = {
                'data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                'task_type': 'parallel_processing'
            }
        elif self.current_tissue.tissue_type == "storage":
            test_input = {
                'store_data': "test_data_package",
                'retrieve_data': False
            }
        else:
            test_input = {'test_message': 'Hello tissue!'}
        
        # Execute function
        result = self.current_tissue.coordinate_function(test_input)
        
        # Display results
        self.console.print("📊 Test Results:")
        for key, value in result.items():
            if isinstance(value, (list, dict)):
                self.console.print(f"  {key}: {len(value) if isinstance(value, list) else len(value)} items")
            else:
                self.console.print(f"  {key}: {value}")
        
        questionary.press_any_key("Press any key to continue...").ask()
    
    def simulate_tissue_growth(self):
        """Simulate tissue growth over time"""
        if not self.current_tissue:
            self.console.print("❌ No tissue loaded!", style="red")
            return
        
        self.console.print("📈 Simulating tissue growth...")
        
        initial_cells = len(self.current_tissue.cells)
        growth_cycles = 5
        
        with Progress(console=self.console) as progress:
            task = progress.add_task("Growing tissue...", total=growth_cycles)
            
            for cycle in range(growth_cycles):
                # Attempt growth
                growth_occurred = self.current_tissue.grow()
                
                if growth_occurred:
                    self.console.print(f"Cycle {cycle + 1}: Growth occurred!")
                else:
                    self.console.print(f"Cycle {cycle + 1}: No growth this cycle")
                
                # Maintain tissue health
                self.current_tissue.maintain_health()
                self.current_tissue.synchronize_cells()
                
                progress.update(task, advance=1)
                time.sleep(1)
        
        final_cells = len(self.current_tissue.cells)
        self.console.print(f"\n📊 Growth Results:")
        self.console.print(f"Initial cells: {initial_cells}")
        self.console.print(f"Final cells: {final_cells}")
        self.console.print(f"Growth: {final_cells - initial_cells} new cells")
        
        questionary.press_any_key("Press any key to continue...").ask()
    
    def demonstrate_cell_communication(self):
        """Demonstrate cell-to-cell communication"""
        if not self.current_tissue:
            self.console.print("❌ No tissue loaded!", style="red")
            return
        
        if len(self.current_tissue.cells) < 2:
            self.console.print("❌ Need at least 2 cells for communication demo!", style="red")
            return
        
        self.console.print("🔗 Demonstrating cell communication...")
        
        sender = self.current_tissue.cells[0]
        receiver = self.current_tissue.cells[1]
        
        message = {
            'type': 'coordination',
            'data': 'synchronization_signal',
            'timestamp': time.time()
        }
        
        self.console.print(f"📤 Sending message from {sender.cell_id} to {receiver.cell_id}")
        sender.communicate_with_neighbor(receiver, message)
        
        self.console.print("✅ Message sent successfully!")
        self.console.print(f"📥 Receiver now has {len(receiver.communication_channels)} communication channels")
        
        questionary.press_any_key("Press any key to continue...").ask()
    
    def explore_organ_systems(self):
        """Explore organ system functionality"""
        self.console.print(Panel(
            "🏗️ Organ Systems Explorer\n\n"
            "Explore complex organ systems built from specialized tissues\n"
            "and see how they coordinate for system-wide functions.",
            title="Organ Systems",
            border_style="purple"
        ))
        
        system_choice = questionary.select(
            "Which organ system would you like to explore?",
            choices=[
                "🚰 Vascular System (Transport)",
                "🏗️ Support System (Structure)", 
                "⚡ Processing System (Computation)",
                "🫁 Respiratory System (Interface)",
                "🛡️ Immune System (Defense)",
                "⬅️ Back to Main Menu"
            ]
        ).ask()
        
        if system_choice and "Back" not in system_choice:
            if "Vascular" in system_choice:
                self.explore_vascular_system()
            elif "Support" in system_choice:
                self.explore_support_system()
            elif "Processing" in system_choice:
                self.explore_processing_system()
            else:
                self.console.print("🚧 This organ system explorer is coming soon!")
                questionary.press_any_key("Press any key to continue...").ask()
    
    def explore_vascular_system(self):
        """Demonstrate vascular system functionality"""
        vascular = VascularSystem()
        
        # Add some demo tissues
        if self.current_tissue:
            vascular.add_tissue(self.current_tissue, "transport")
        
        # Establish channels
        vascular.establish_transport_channel("source_node", "destination_node", "xylem")
        vascular.establish_transport_channel("destination_node", "source_node", "phloem")
        
        # Test system function
        test_input = {
            'resources': {'energy': 100},
            'information': {'data_packets': ['packet1', 'packet2', 'packet3']}
        }
        
        result = vascular.execute_system_function(test_input)
        
        self.console.print("🚰 Vascular System Test Results:")
        for key, value in result.items():
            self.console.print(f"  {key}: {value}")
        
        questionary.press_any_key("Press any key to continue...").ask()
    
    def explore_support_system(self):
        """Demonstrate support system functionality"""
        support = SupportSystem()
        
        # Add scaffold nodes
        support.add_scaffold_node("node1", (0, 0), 1.0)
        support.add_scaffold_node("node2", (1, 1), 0.8)
        support.add_scaffold_node("node3", (2, 0), 1.2)
        
        # Test with structural loads
        test_input = {
            'structural_loads': {'load1': 50, 'load2': 30},
            'adapt_structure': True,
            'damage_locations': [(0.5, 0.5)]
        }
        
        result = support.execute_system_function(test_input)
        
        self.console.print("🏗️ Support System Test Results:")
        for key, value in result.items():
            self.console.print(f"  {key}: {value}")
        
        questionary.press_any_key("Press any key to continue...").ask()
    
    def explore_processing_system(self):
        """Demonstrate processing system functionality"""
        processing = ProcessingSystem()
        
        # Add computational tissue if available
        if self.current_tissue and self.current_tissue.tissue_type == "computational":
            processing.add_tissue(self.current_tissue, "compute")
        
        # Test computational photosynthesis
        test_input = {
            'light_data': 2.0,
            'processing_tasks': [
                {'task': 'matrix_multiply', 'data': [1, 2, 3]},
                {'task': 'signal_process', 'data': [4, 5, 6]}
            ]
        }
        
        result = processing.execute_system_function(test_input)
        
        self.console.print("⚡ Processing System Test Results:")
        for key, value in result.items():
            if isinstance(value, dict):
                self.console.print(f"  {key}:")
                for subkey, subvalue in value.items():
                    self.console.print(f"    {subkey}: {subvalue}")
            else:
                self.console.print(f"  {key}: {value}")
        
        questionary.press_any_key("Press any key to continue...").ask()

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
