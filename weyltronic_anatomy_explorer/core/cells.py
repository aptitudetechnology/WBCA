"""
WeyltonicCell - The fundamental reconfigurable biological computing unit
"""

from typing import Dict, Any, List, Optional
import uuid
import copy
from .organelles import (
    Nucleus, Ribosome, Mitochondria, Chloroplast, 
    Vacuole, Cytoplasm, ER, GolgiApparatus, CellWall
)


class WeyltonicCell:
    """
    A reconfigurable FPGA-based biological computing cell.
    Contains multiple organelles that can be dynamically reconfigured
    based on genetic programs.
    """
    
    def __init__(self, cell_id: str = None):
        self.cell_id = cell_id or str(uuid.uuid4())
        self.generation = 1
        self.age = 0
        self.health = 100.0
        self.energy_level = 100.0
        self.division_threshold = 200.0
        
        # Initialize organelles
        self.organelles = {
            'nucleus': Nucleus(f"{self.cell_id}_nucleus"),
            'ribosome': Ribosome(f"{self.cell_id}_ribosome"),
            'mitochondria': Mitochondria(f"{self.cell_id}_mitochondria"),
            'chloroplast': Chloroplast(f"{self.cell_id}_chloroplast"),
            'vacuole': Vacuole(f"{self.cell_id}_vacuole"),
            'cytoplasm': Cytoplasm(f"{self.cell_id}_cytoplasm"),
            'er': ER(f"{self.cell_id}_er"),
            'golgi': GolgiApparatus(f"{self.cell_id}_golgi"),
            'cell_wall': CellWall(f"{self.cell_id}_cell_wall")
        }
        
        # Cell state
        self.current_program = None
        self.specialization = "undifferentiated"
        self.communication_channels = {}
        self.neighboring_cells = []
        
        print(f"WeyltonicCell {self.cell_id} created with {len(self.organelles)} organelles")
    
    def load_genetic_program(self, program_name: str, program_code: Dict[str, Any]):
        """Load a genetic program into the nucleus"""
        self.organelles['nucleus'].load_program(program_name, program_code)
        self.current_program = program_name
        print(f"Cell {self.cell_id}: Loaded genetic program '{program_name}'")
    
    def express_genes(self, gene_segments: List[str]):
        """Express specific gene segments through ribosome"""
        if not self.current_program:
            print(f"Cell {self.cell_id}: No genetic program loaded")
            return False
            
        for segment in gene_segments:
            # Get configuration from nucleus
            config = self.organelles['nucleus'].get_gene_config(segment)
            if config:
                # Ribosome compiles and applies configuration
                success = self.organelles['ribosome'].compile_and_configure(
                    segment, config, self.organelles
                )
                if success:
                    print(f"Cell {self.cell_id}: Successfully expressed gene '{segment}'")
                else:
                    print(f"Cell {self.cell_id}: Failed to express gene '{segment}'")
        
        return True
    
    def specialize(self, cell_type: str):
        """Specialize the cell for a specific function"""
        specialization_programs = {
            'compute': ['high_performance_chloroplast', 'enhanced_processing'],
            'memory': ['expanded_vacuole', 'data_retention_mode'],
            'transport': ['enhanced_cytoplasm', 'channel_optimization'],
            'sensory': ['membrane_sensitivity', 'signal_processing']
        }
        
        if cell_type in specialization_programs:
            self.specialization = cell_type
            self.express_genes(specialization_programs[cell_type])
            print(f"Cell {self.cell_id}: Specialized as '{cell_type}' cell")
        else:
            print(f"Cell {self.cell_id}: Unknown specialization '{cell_type}'")
    
    def execute_cycle(self, inputs: Dict[str, Any] = None):
        """Execute one computational cycle"""
        if inputs is None:
            inputs = {}
            
        # Power management - distribute energy from mitochondria
        total_energy_needed = sum(org.energy_consumption for org in self.organelles.values())
        
        if self.energy_level < total_energy_needed:
            print(f"Cell {self.cell_id}: Insufficient energy ({self.energy_level:.1f} < {total_energy_needed:.1f})")
            return None
            
        # Consume energy
        self.energy_level -= total_energy_needed * 0.1  # 10% consumption per cycle
        
        # Process through organelles based on cytoplasm connections
        cytoplasm = self.organelles['cytoplasm']
        results = {}
        
        # Start with inputs and process through connected organelles
        current_data = inputs
        processing_chain = cytoplasm.get_processing_chain()
        
        for organelle_name in processing_chain:
            if organelle_name in self.organelles:
                organelle = self.organelles[organelle_name]
                if organelle.active:
                    output = organelle.process(current_data)
                    results[organelle_name] = output
                    current_data.update(output)
        
        # Age the cell and check health
        self.age += 1
        self._update_health()
        
        return results
    
    def communicate_with_neighbor(self, neighbor_cell: 'WeyltonicCell', message: Dict[str, Any]):
        """Send a message to a neighboring cell"""
        if neighbor_cell.cell_id not in [cell.cell_id for cell in self.neighboring_cells]:
            self.neighboring_cells.append(neighbor_cell)
            neighbor_cell.neighboring_cells.append(self)
        
        # Process through cell wall
        transmitted_message = self.organelles['cell_wall'].transmit(message)
        neighbor_cell.receive_message(self.cell_id, transmitted_message)
    
    def receive_message(self, sender_id: str, message: Dict[str, Any]):
        """Receive a message from another cell"""
        received_message = self.organelles['cell_wall'].receive(message)
        
        # Store in communication channels
        if sender_id not in self.communication_channels:
            self.communication_channels[sender_id] = []
        self.communication_channels[sender_id].append(received_message)
        
        print(f"Cell {self.cell_id}: Received message from {sender_id}")
    
    def can_divide(self) -> bool:
        """Check if cell can divide"""
        return (self.energy_level > self.division_threshold and 
                self.health > 75.0 and 
                self.age > 10)
    
    def divide(self) -> Optional['WeyltonicCell']:
        """Create a daughter cell through division"""
        if not self.can_divide():
            return None
            
        # Create daughter cell
        daughter_id = f"{self.cell_id}_daughter_{self.generation}"
        daughter_cell = WeyltonicCell(daughter_id)
        daughter_cell.generation = self.generation + 1
        
        # Copy genetic program
        if self.current_program:
            nucleus = self.organelles['nucleus']
            program_code = nucleus.genetic_programs.get(self.current_program, {})
            daughter_cell.load_genetic_program(self.current_program, program_code)
        
        # Copy specialization
        if self.specialization != "undifferentiated":
            daughter_cell.specialize(self.specialization)
        
        # Divide resources
        self.energy_level *= 0.6  # Parent keeps 60%
        daughter_cell.energy_level = self.energy_level * 0.4  # Daughter gets 40%
        
        # Add some mutation potential
        self._introduce_mutations(daughter_cell)
        
        print(f"Cell {self.cell_id}: Divided to create {daughter_id}")
        return daughter_cell
    
    def _update_health(self):
        """Update cell health based on various factors"""
        # Health decreases with age
        age_factor = max(0, 100 - (self.age * 0.1))
        
        # Health affected by energy levels
        energy_factor = self.energy_level
        
        # Health affected by organelle status
        organelle_health = sum(
            100 if org.active else 50 
            for org in self.organelles.values()
        ) / len(self.organelles)
        
        self.health = (age_factor + energy_factor + organelle_health) / 3
        
        # Deactivate organelles if health is low
        if self.health < 30:
            for org in self.organelles.values():
                if org.id != f"{self.cell_id}_nucleus":  # Keep nucleus active
                    org.active = False
    
    def _introduce_mutations(self, daughter_cell: 'WeyltonicCell'):
        """Introduce small random mutations in daughter cell"""
        import random
        
        # Small chance of organelle parameter changes
        for org_name, organelle in daughter_cell.organelles.items():
            if random.random() < 0.05:  # 5% mutation chance
                if hasattr(organelle, 'efficiency'):
                    organelle.efficiency *= random.uniform(0.9, 1.1)
                if hasattr(organelle, 'capacity'):
                    organelle.capacity *= random.uniform(0.95, 1.05)
                print(f"Mutation in {daughter_cell.cell_id}: {org_name} parameters changed")
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive cell status"""
        return {
            'cell_id': self.cell_id,
            'generation': self.generation,
            'age': self.age,
            'health': self.health,
            'energy_level': self.energy_level,
            'specialization': self.specialization,
            'current_program': self.current_program,
            'can_divide': self.can_divide(),
            'neighbor_count': len(self.neighboring_cells),
            'organelles': {
                name: org.get_status() 
                for name, org in self.organelles.items()
            }
        }
    
    def regenerate_energy(self, amount: float = 10.0):
        """Regenerate energy (e.g., through photosynthesis-like process)"""
        if self.organelles['chloroplast'].active:
            energy_gain = self.organelles['chloroplast'].photosynthesize(amount)
            self.energy_level = min(100.0, self.energy_level + energy_gain)
            print(f"Cell {self.cell_id}: Regenerated {energy_gain:.1f} energy")
    
    def repair_damage(self):
        """Attempt to repair cellular damage"""
        if self.health < 100:
            repair_amount = min(10.0, 100 - self.health)
            self.health += repair_amount
            
            # Reactivate organelles if health improves
            if self.health > 50:
                for org in self.organelles.values():
                    if not org.active and org.id != f"{self.cell_id}_nucleus":
                        org.active = True
                        
            print(f"Cell {self.cell_id}: Repaired {repair_amount:.1f} health")
    
    def __str__(self):
        return f"WeyltonicCell({self.cell_id}, {self.specialization}, health={self.health:.1f})"
    
    def __repr__(self):
        return self.__str__()
