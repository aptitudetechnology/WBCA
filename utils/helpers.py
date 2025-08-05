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
