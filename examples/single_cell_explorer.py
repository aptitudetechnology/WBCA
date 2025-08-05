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
