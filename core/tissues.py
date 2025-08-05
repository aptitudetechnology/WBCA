"""
WeyltonicTissue - Collections of specialized cells working cooperatively
"""

from typing import Dict, Any, List, Optional
import uuid
import numpy as np
from .cells import WeyltonicCell


class WeyltonicTissue:
    """
    A collection of WeyltonicCells grouped for specialized functions.
    Manages tissue-level coordination and communication.
    """
    
    def __init__(self, tissue_id: str = None, tissue_type: str = "generic"):
        self.tissue_id = tissue_id or str(uuid.uuid4())
        self.tissue_type = tissue_type
        self.cells: List[WeyltonicCell] = []
        self.cell_positions = {}  # 2D grid positions
        self.communication_network = {}
        self.tissue_age = 0
        self.growth_rate = 1.0
        self.max_size = 100  # Maximum number of cells
        
        # Tissue-specific properties
        self.specialized_function = self._get_specialized_function(tissue_type)
        self.coordination_patterns = {}
        self.resource_sharing = True
        
        print(f"WeyltonicTissue {self.tissue_id} ({tissue_type}) created")
    
    def _get_specialized_function(self, tissue_type: str) -> str:
        """Get the specialized function based on tissue type"""
        functions = {
            'computational': 'parallel_processing',
            'storage': 'data_retention',
            'transport': 'information_routing',
            'sensory': 'environmental_sensing',
            'structural': 'mechanical_support',
            'metabolic': 'energy_production'
        }
        return functions.get(tissue_type, 'general_purpose')
    
    def add_cell(self, cell: WeyltonicCell, position: tuple = None):
        """Add a cell to the tissue"""
        if len(self.cells) >= self.max_size:
            print(f"Tissue {self.tissue_id}: Maximum size reached")
            return False
            
        self.cells.append(cell)
        
        # Assign position in tissue
        if position is None:
            position = self._find_available_position()
        self.cell_positions[cell.cell_id] = position
        
        # Establish connections with neighboring cells
        self._establish_local_connections(cell, position)
        
        # Specialize cell based on tissue type
        if self.tissue_type != "generic":
            cell.specialize(self._get_cell_specialization())
            
        print(f"Tissue {self.tissue_id}: Added cell {cell.cell_id} at position {position}")
        return True
    
    def _find_available_position(self) -> tuple:
        """Find an available position in the tissue grid"""
        occupied_positions = set(self.cell_positions.values())
        
        # Simple spiral placement algorithm
        x, y = 0, 0
        if (x, y) not in occupied_positions:
            return (x, y)
            
        for radius in range(1, 20):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if abs(dx) == radius or abs(dy) == radius:
                        pos = (dx, dy)
                        if pos not in occupied_positions:
                            return pos
        
        # Fallback
        return (len(self.cells), 0)
    
    def _establish_local_connections(self, new_cell: WeyltonicCell, position: tuple):
        """Establish connections with neighboring cells"""
        x, y = position
        neighbors = [
            (x-1, y), (x+1, y), (x, y-1), (x, y+1)  # Adjacent cells
        ]
        
        for neighbor_pos in neighbors:
            for existing_cell in self.cells[:-1]:  # Exclude the new cell
                if self.cell_positions.get(existing_cell.cell_id) == neighbor_pos:
                    # Establish bidirectional communication
                    new_cell.neighboring_cells.append(existing_cell)
                    existing_cell.neighboring_cells.append(new_cell)
                    
                    # Add to communication network
                    if new_cell.cell_id not in self.communication_network:
                        self.communication_network[new_cell.cell_id] = []
                    if existing_cell.cell_id not in self.communication_network:
                        self.communication_network[existing_cell.cell_id] = []
                        
                    self.communication_network[new_cell.cell_id].append(existing_cell.cell_id)
                    self.communication_network[existing_cell.cell_id].append(new_cell.cell_id)
    
    def _get_cell_specialization(self) -> str:
        """Get cell specialization based on tissue type"""
        specializations = {
            'computational': 'compute',
            'storage': 'memory',
            'transport': 'transport',
            'sensory': 'sensory'
        }
        return specializations.get(self.tissue_type, 'compute')
    
    def coordinate_function(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """Coordinate the tissue's specialized function"""
        if inputs is None:
            inputs = {}
            
        results = {}
        
        if self.specialized_function == 'parallel_processing':
            results = self._parallel_processing(inputs)
        elif self.specialized_function == 'data_retention':
            results = self._data_storage(inputs)
        elif self.specialized_function == 'information_routing':
            results = self._information_routing(inputs)
        elif self.specialized_function == 'environmental_sensing':
            results = self._environmental_sensing(inputs)
        elif self.specialized_function == 'energy_production':
            results = self._energy_production(inputs)
        else:
            results = self._general_processing(inputs)
            
        return results
    
    def _parallel_processing(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate parallel processing across cells"""
        if not self.cells:
            return {'error': 'No cells available'}
            
        # Distribute workload across cells
        data_chunks = inputs.get('data', [])
        if not isinstance(data_chunks, list):
            data_chunks = [data_chunks]
            
        chunk_size = max(1, len(data_chunks) // len(self.cells))
        results = []
        
        for i, cell in enumerate(self.cells):
            start_idx = i * chunk_size
            end_idx = start_idx + chunk_size if i < len(self.cells) - 1 else len(data_chunks)
            
            if start_idx < len(data_chunks):
                cell_input = {
                    'processing_data': data_chunks[start_idx:end_idx],
                    'task_id': f"task_{i}"
                }
                cell_result = cell.execute_cycle(cell_input)
                results.append(cell_result)
        
        return {
            'tissue_function': 'parallel_processing',
            'individual_results': results,
            'cells_used': len(self.cells),
            'total_processing_power': sum(
                cell.organelles['chloroplast'].processing_power 
                for cell in self.cells
            )
        }
    
    def _data_storage(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate data storage across cells"""
        storage_data = inputs.get('store_data')
        retrieve_request = inputs.get('retrieve_data', False)
        
        total_capacity = sum(
            cell.organelles['vacuole'].capacity 
            for cell in self.cells
        )
        total_usage = sum(
            cell.organelles['vacuole'].current_usage 
            for cell in self.cells
        )
        
        results = {
            'tissue_function': 'data_storage',
            'total_capacity': total_capacity,
            'total_usage': total_usage,
            'utilization': total_usage / total_capacity if total_capacity > 0 else 0
        }
        
        if storage_data:
            # Find cell with available capacity
            for cell in self.cells:
                if cell.organelles['vacuole'].store(storage_data):
                    results['stored_in'] = cell.cell_id
                    results['storage_success'] = True
                    break
            else:
                results['storage_success'] = False
                results['error'] = 'No available capacity'
        
        if retrieve_request:
            # Try to retrieve from any cell
            for cell in self.cells:
                data = cell.organelles['vacuole'].retrieve()
                if data:
                    results['retrieved_data'] = data
                    results['retrieved_from'] = cell.cell_id
                    break
            else:
                results['retrieved_data'] = None
        
        return results
    
    def _information_routing(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate information routing through tissue"""
        message = inputs.get('route_message')
        destination = inputs.get('destination')
        
        if not message:
            return {'error': 'No message to route'}
            
        # Use cells as routing nodes
        routing_path = self._find_routing_path(destination)
        
        return {
            'tissue_function': 'information_routing',
            'message_routed': bool(message),
            'routing_path': routing_path,
            'network_topology': self.communication_network
        }
    
    def _environmental_sensing(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate environmental sensing"""
        sensor_readings = []
        
        for cell in self.cells:
            # Simulate sensing through cell wall
            cell_wall = cell.organelles['cell_wall']
            if hasattr(cell_wall, 'permeability'):
                reading = {
                    'cell_id': cell.cell_id,
                    'permeability': cell_wall.permeability,
                    'position': self.cell_positions.get(cell.cell_id, (0, 0)),
                    'health': cell.health
                }
                sensor_readings.append(reading)
        
        return {
            'tissue_function': 'environmental_sensing',
            'sensor_readings': sensor_readings,
            'average_health': np.mean([cell.health for cell in self.cells]) if self.cells else 0
        }
    
    def _energy_production(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate energy production across cells"""
        total_energy_produced = 0
        
        for cell in self.cells:
            # Trigger photosynthesis in chloroplasts
            energy = cell.organelles['chloroplast'].photosynthesize(
                inputs.get('light_level', 1.0)
            )
            total_energy_produced += energy
            cell.energy_level = min(100.0, cell.energy_level + energy)
        
        return {
            'tissue_function': 'energy_production',
            'total_energy_produced': total_energy_produced,
            'cells_energized': len(self.cells)
        }
    
    def _general_processing(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """General processing for unspecialized tissues"""
        results = []
        for cell in self.cells:
            result = cell.execute_cycle(inputs)
            results.append(result)
        
        return {
            'tissue_function': 'general_processing',
            'cell_results': results
        }
    
    def _find_routing_path(self, destination: str) -> List[str]:
        """Find routing path through tissue network"""
        if not self.cells:
            return []
            
        # Simple shortest path (could be enhanced with actual pathfinding)
        start_cell = self.cells[0].cell_id
        
        if destination in self.communication_network:
            return [start_cell, destination]
        
        # For now, return path through first few cells
        return [cell.cell_id for cell in self.cells[:3]]
    
    def grow(self) -> bool:
        """Attempt tissue growth by cell division"""
        if len(self.cells) >= self.max_size:
            return False
            
        # Find a cell capable of division
        for cell in self.cells:
            if cell.can_divide():
                daughter_cell = cell.divide()
                if daughter_cell:
                    self.add_cell(daughter_cell)
                    self.tissue_age += 1
                    print(f"Tissue {self.tissue_id}: Grew from {len(self.cells)-1} to {len(self.cells)} cells")
                    return True
        
        return False
    
    def maintain_health(self):
        """Maintain tissue health through cell cooperation"""
        # Share resources between healthy and damaged cells
        if self.resource_sharing:
            healthy_cells = [cell for cell in self.cells if cell.health > 70]
            damaged_cells = [cell for cell in self.cells if cell.health < 50]
            
            for healthy_cell in healthy_cells:
                for damaged_cell in damaged_cells:
                    if healthy_cell.energy_level > 80:
                        # Transfer some energy
                        transfer_amount = min(10.0, healthy_cell.energy_level - 70)
                        healthy_cell.energy_level -= transfer_amount
                        damaged_cell.energy_level += transfer_amount
                        
                        # Attempt repair
                        damaged_cell.repair_damage()
    
    def synchronize_cells(self):
        """Synchronize cellular activities"""
        # Coordinate cell cycles
        avg_age = np.mean([cell.age for cell in self.cells]) if self.cells else 0
        
        for cell in self.cells:
            # Adjust cell timing based on tissue average
            if abs(cell.age - avg_age) > 5:
                # Small adjustment to synchronize
                adjustment = (avg_age - cell.age) * 0.1
                cell.age += adjustment
        
        print(f"Tissue {self.tissue_id}: Synchronized {len(self.cells)} cells")
    
    def get_tissue_status(self) -> Dict[str, Any]:
        """Get comprehensive tissue status"""
        if not self.cells:
            return {
                'tissue_id': self.tissue_id,
                'tissue_type': self.tissue_type,
                'cell_count': 0,
                'health': 0,
                'energy': 0
            }
        
        avg_health = np.mean([cell.health for cell in self.cells])
        avg_energy = np.mean([cell.energy_level for cell in self.cells])
        total_capacity = sum(
            cell.organelles['vacuole'].capacity 
            for cell in self.cells
        )
        
        return {
            'tissue_id': self.tissue_id,
            'tissue_type': self.tissue_type,
            'specialized_function': self.specialized_function,
            'cell_count': len(self.cells),
            'tissue_age': self.tissue_age,
            'average_health': avg_health,
            'average_energy': avg_energy,
            'total_storage_capacity': total_capacity,
            'network_connections': len(self.communication_network),
            'can_grow': len(self.cells) < self.max_size,
            'cells': [
                {
                    'id': cell.cell_id,
                    'health': cell.health,
                    'energy': cell.energy_level,
                    'specialization': cell.specialization,
                    'position': self.cell_positions.get(cell.cell_id)
                }
                for cell in self.cells
            ]
        }
    
    def __str__(self):
        return f"WeyltonicTissue({self.tissue_id}, {self.tissue_type}, {len(self.cells)} cells)"
    
    def __repr__(self):
        return self.__str__()
