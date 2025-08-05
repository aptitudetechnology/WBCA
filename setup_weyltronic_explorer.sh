#!/bin/bash

# Weyltronic Biological Computing Anatomy Explorer - MVP Setup Script
# Creates the basic project structure and core files

PROJECT_NAME="weyltronic_anatomy_explorer"

echo "Creating Weyltronic Biological Computing Anatomy Explorer MVP..."

# Create main project directory
mkdir -p $PROJECT_NAME
cd $PROJECT_NAME

# Create directory structure
mkdir -p core quantum genomics interfaces visualization simulations utils examples

# Create __init__.py files
touch core/__init__.py
touch quantum/__init__.py
touch genomics/__init__.py
touch interfaces/__init__.py
touch visualization/__init__.py
touch simulations/__init__.py
touch utils/__init__.py

# Create requirements.txt
cat > requirements.txt << 'EOF'
questionary>=1.10.0
rich>=13.0.0
matplotlib>=3.6.0
numpy>=1.24.0
colorama>=0.4.6
EOF

# Create main.py - Entry point
cat > main.py << 'EOF'
#!/usr/bin/env python3
"""
Weyltronic Biological Computing Anatomy Educational Explorer
Main entry point for the educational exploration tool
"""

from interfaces.explorer_cli import WeyltonicExplorerCLI
from utils.config import Config

def main():
    """Main entry point for the Weyltronic Explorer"""
    print("🧬 Weyltronic Biological Computing Anatomy Explorer")
    print("=" * 50)
    
    config = Config()
    explorer = WeyltonicExplorerCLI(config)
    explorer.run()

if __name__ == "__main__":
    main()
EOF

# Create utils/config.py - Basic configuration
cat > utils/config.py << 'EOF'
"""Configuration management for Weyltronic Explorer"""

class Config:
    """Basic configuration for the Weyltronic system"""
    
    def __init__(self):
        # System parameters
        self.max_cells = 100  # Start small for MVP
        self.quantum_coherence_time = 1000  # microseconds
        self.fpga_clock_speed = 100e6  # 100 MHz
        
        # Visualization settings
        self.animation_fps = 30
        self.cell_display_size = 10
        
        # Educational settings
        self.tutorial_mode = True
        self.show_tooltips = True
        
    def get_organelle_types(self):
        """Get list of available organelle types"""
        return [
            'nucleus',
            'ribosomes', 
            'mitochondria',
            'chloroplasts',
            'er_rough',
            'er_smooth',
            'golgi',
            'vacuole',
            'cytoplasm',
            'cell_wall'
        ]
EOF

# Create utils/helpers.py - Utility functions
cat > utils/helpers.py << 'EOF'
"""Helper utilities for Weyltronic Explorer"""

import random
import numpy as np
from typing import List, Dict, Any

def generate_cell_id() -> str:
    """Generate a unique cell identifier"""
    return f"cell_{random.randint(1000, 9999)}"

def calculate_quantum_coherence(temperature: float, noise_level: float) -> float:
    """Calculate quantum coherence based on environmental factors"""
    # Simplified model for MVP
    base_coherence = 0.95
    temp_factor = max(0.1, 1.0 - (temperature - 310) / 100)  # 310K = body temp
    noise_factor = max(0.1, 1.0 - noise_level)
    return base_coherence * temp_factor * noise_factor

def format_cell_status(cell_data: Dict[str, Any]) -> str:
    """Format cell status for display"""
    status = f"Cell {cell_data.get('id', 'unknown')}\n"
    status += f"  Type: {cell_data.get('type', 'generic')}\n"
    status += f"  Organelles: {len(cell_data.get('organelles', []))}\n"
    status += f"  Energy: {cell_data.get('energy', 0):.1f}%\n"
    return status

class BiologicalTimer:
    """Simple timer for biological processes"""
    
    def __init__(self):
        self.start_time = 0
        self.current_time = 0
        
    def tick(self, dt: float = 0.1):
        """Advance biological time"""
        self.current_time += dt
        
    def get_time(self) -> float:
        """Get current biological time"""
        return self.current_time
EOF

# Create core/organelles.py - FPGA-based organelles
cat > core/organelles.py << 'EOF'
"""
FPGA-based Organelle implementations for Weyltronic cells
Each organelle represents a specialized FPGA logic block
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import random

class Organelle(ABC):
    """Base class for all FPGA-based organelles"""
    
    def __init__(self, organelle_id: str, fpga_blocks: int = 1):
        self.id = organelle_id
        self.fpga_blocks = fpga_blocks
        self.energy_consumption = 1.0
        self.active = True
        self.configuration = {}
        
    @abstractmethod
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Process inputs and return outputs"""
        pass
        
    def reconfigure(self, new_config: Dict[str, Any]):
        """Reconfigure the FPGA organelle"""
        self.configuration.update(new_config)
        
    def get_status(self) -> Dict[str, Any]:
        """Get current organelle status"""
        return {
            'id': self.id,
            'type': self.__class__.__name__,
            'active': self.active,
            'energy': self.energy_consumption,
            'fpga_blocks': self.fpga_blocks,
            'configuration': self.configuration
        }

class Nucleus(Organelle):
    """Configuration management and genetic code storage"""
    
    def __init__(self, organelle_id: str):
        super().__init__(organelle_id, fpga_blocks=4)
        self.genetic_code = []
        self.configuration_memory = {}
        
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Manage cell configuration and genetic programs"""
        outputs = {
            'configuration_updates': {},
            'genetic_instructions': self.genetic_code
        }
        
        if 'new_genetic_code' in inputs:
            self.genetic_code = inputs['new_genetic_code']
            outputs['reconfiguration_signal'] = True
            
        return outputs
        
    def load_genetic_program(self, program: List[str]):
        """Load a genetic program into the nucleus"""
        self.genetic_code = program

class Ribosomes(Organelle):
    """Code compilation units that reconfigure other organelles"""
    
    def __init__(self, organelle_id: str):
        super().__init__(organelle_id, fpga_blocks=2)
        self.compilation_queue = []
        
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Compile genetic code into organelle configurations"""
        outputs = {'compiled_configs': []}
        
        if 'genetic_instructions' in inputs:
            for instruction in inputs['genetic_instructions']:
                compiled_config = self._compile_instruction(instruction)
                outputs['compiled_configs'].append(compiled_config)
                
        return outputs
        
    def _compile_instruction(self, instruction: str) -> Dict[str, Any]:
        """Compile a single genetic instruction"""
        # Simplified compilation for MVP
        return {
            'target_organelle': 'mitochondria',  # Default target
            'config_update': {'efficiency': random.uniform(0.8, 1.2)}
        }

class Mitochondria(Organelle):
    """Power management and energy distribution circuits"""
    
    def __init__(self, organelle_id: str):
        super().__init__(organelle_id, fpga_blocks=3)
        self.energy_production = 10.0
        self.efficiency = 1.0
        
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate and distribute energy"""
        current_production = self.energy_production * self.efficiency
        
        outputs = {
            'energy_output': current_production,
            'power_status': 'optimal' if self.efficiency > 0.8 else 'degraded'
        }
        
        # Handle efficiency updates from ribosomes
        if 'config_update' in inputs and 'efficiency' in inputs['config_update']:
            self.efficiency = inputs['config_update']['efficiency']
            
        return outputs

# Additional organelle classes would go here...
# For MVP, we'll create the basic framework and add more organelles later
EOF

# Create prompt files for larger components
cat > PROMPTS.md << 'EOF'
# Prompts for Creating Remaining Components

## 1. Core Components

### core/cells.py
Create a WeyltonicCell class that:
- Contains multiple organelles (FPGA logic blocks)
- Manages intercellular communication through cytoplasm interconnect
- Handles dynamic reconfiguration based on genetic programs
- Tracks energy consumption and cellular health
- Supports cellular division and specialization

### core/tissues.py
Create WeyltonicTissue class that:
- Groups multiple cells with similar functions
- Manages tissue-level coordination and communication
- Handles tissue growth and adaptation
- Supports different tissue types (computational, storage, transport)

### core/organs.py
Create organ system models:
- Vascular system (dual-channel transport)
- Support system (quantum scaffolding)
- Processing system (computational photosynthesis)
- Each organ composed of specialized tissues

## 2. Quantum Components

### quantum/weyl_transport.py
Implement Weyl semimetal transport:
- Topologically protected quantum channels
- Chiral anomaly effects
- Self-healing transport networks
- Quantum coherence in biological environments

### quantum/coherence.py
Quantum coherence management:
- Decoherence time calculations
- Environmental noise modeling
- Coherence preservation strategies
- Quantum error correction

## 3. Genomics System

### genomics/genetic_code.py
Genetic programming language:
- Simple instruction set for cellular configuration
- Parser for genetic programs
- Validation and error checking
- Program optimization

### genomics/gene_expression.py
Dynamic reconfiguration engine:
- Real-time FPGA reconfiguration
- Gene expression levels
- Regulatory networks
- Cellular differentiation

## 4. Interactive Interfaces

### interfaces/explorer_cli.py
Command-line interface with:
- Questionary menus for exploration
- Rich console displays
- Interactive tutorials
- System status monitoring

### interfaces/educational_ui.py
Educational interface featuring:
- Step-by-step learning modules
- Interactive experiments
- Progress tracking
- Concept explanations

## 5. Visualization Components

### visualization/cellular_anatomy.py
Cell structure visualizations:
- Organelle arrangement diagrams
- Real-time activity displays
- 3D cellular models
- Interactive organelle inspection

### visualization/tissue_development.py
Growth and development plots:
- Time-lapse tissue formation
- Cell division animations
- Differentiation pathways
- Resource flow visualization

## 6. Example Programs

### examples/single_cell_explorer.py
Basic cell exploration:
- Create and configure individual cells
- Experiment with different organelle combinations
- Observe cellular responses to genetic programs

### examples/tissue_formation.py
Multi-cellular organization:
- Demonstrate cell-to-cell communication
- Show tissue emergence from individual cells
- Explore different tissue architectures

Each component should be created with proper error handling, documentation, and integration with the existing framework.
EOF

# Create interfaces/explorer_cli.py - Basic CLI
cat > interfaces/explorer_cli.py << 'EOF'
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
EOF

# Create a simple example
cat > examples/single_cell_explorer.py << 'EOF'
#!/usr/bin/env python3
"""
Single Cell Explorer Example
Demonstrates basic cell creation and organelle exploration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.organelles import Nucleus, Ribosomes, Mitochondria
from utils.helpers import generate_cell_id, format_cell_status
from utils.config import Config

def main():
    """Run single cell exploration example"""
    print("🔬 Single Cell Explorer Example")
    print("=" * 40)
    
    config = Config()
    cell_id = generate_cell_id()
    
    # Create a basic cell with essential organelles
    print(f"\n📱 Creating cell: {cell_id}")
    
    nucleus = Nucleus(f"{cell_id}_nucleus")
    ribosomes = Ribosomes(f"{cell_id}_ribosomes") 
    mitochondria = Mitochondria(f"{cell_id}_mitochondria")
    
    cell = {
        'id': cell_id,
        'type': 'basic_cell',
        'organelles': {
            'nucleus': nucleus,
            'ribosomes': ribosomes,
            'mitochondria': mitochondria
        },
        'energy': 100.0
    }
    
    print(format_cell_status(cell))
    
    # Demonstrate organelle processing
    print("\n⚡ Demonstrating organelle processing...")
    
    # Nucleus processes genetic code
    genetic_program = ['INCREASE_EFFICIENCY', 'BOOST_ENERGY']
    nucleus.load_genetic_program(genetic_program)
    
    nucleus_output = nucleus.process({})
    print(f"Nucleus output: {nucleus_output}")
    
    # Ribosomes compile genetic instructions
    ribosomes_output = ribosomes.process({
        'genetic_instructions': genetic_program
    })
    print(f"Ribosomes output: {ribosomes_output}")
    
    # Mitochondria respond to configuration updates
    if ribosomes_output['compiled_configs']:
        config_update = ribosomes_output['compiled_configs'][0]
        mitochondria_output = mitochondria.process(config_update)
        print(f"Mitochondria output: {mitochondria_output}")
    
    print("\n✅ Single cell exploration complete!")
    print("This demonstrates how organelles work together in biological computing.")

if __name__ == "__main__":
    main()
EOF

chmod +x examples/single_cell_explorer.py

# Create README
cat > README.md << 'EOF'
# Weyltronic Biological Computing Anatomy Explorer - MVP

An educational tool for exploring biological computing concepts through interactive cellular anatomy.

## Quick Start

1. **Setup**:
   ```bash
   ./setup_weyltronic_explorer.sh  # If running the setup script
   # OR manually:
   pip install -r requirements.txt
   ```

2. **Run Main Explorer**:
   ```bash
   python main.py
   ```

3. **Try Examples**:
   ```bash
   python examples/single_cell_explorer.py
   ```

## Core Concepts

- **FPGA-Based Cellular Units**: Each cell contains organelles implemented as reconfigurable FPGA logic blocks
- **Weyltronic Quantum Transport**: Topologically protected quantum channels for information transfer
- **Biological Computing Anatomy**: How computational systems can be organized like biological organs
- **Genetic Programming**: Dynamic reconfiguration of cellular components through genetic code

## Current MVP Features

- ✅ Basic cell creation and configuration
- ✅ Core organelles (Nucleus, Ribosomes, Mitochondria)
- ✅ Interactive CLI with questionary and rich
- ✅ Organelle exploration and status display
- ✅ Tutorial mode for educational guidance
- ✅ Single cell example demonstration

## Next Development Steps

See `PROMPTS.md` for detailed prompts to create the remaining components:
- Additional organelle types
- Tissue and organ system modeling
- Quantum transport implementation
- Advanced visualization
- More educational scenarios

## Architecture

```
weyltronic_anatomy_explorer/
├── core/           # Cellular and anatomical components
├── quantum/        # Weyltronic quantum transport
├── genomics/       # Genetic programming system
├── interfaces/     # User interfaces
├── visualization/  # Plotting and display
├── examples/       # Educational examples
└── utils/          # Utilities and configuration
```

## Educational Goals

This tool teaches biological computing through hands-on exploration of:
- How cells can function as computational units
- Why biological organization outperforms traditional architecture
- Quantum effects in biological systems
- Emergent properties from cellular interactions
EOF

echo "✅ Weyltronic Biological Computing Anatomy Explorer MVP structure created!"
echo ""
echo "Next steps:
1. pip install -r requirements.txt
2. python main.py

📝 See PROMPTS.md for creating the remaining components
🔬 Try: python examples/single_cell_explorer.py
"