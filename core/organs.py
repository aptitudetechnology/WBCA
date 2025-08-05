"""
Organ Systems - Complex biological computing structures composed of specialized tissues
"""

from typing import Dict, Any, List, Optional
import uuid
import numpy as np
from .tissues import WeyltonicTissue


class OrganSystem:
    """Base class for all biological computing organ systems"""
    
    def __init__(self, name: str, system_id: str = None):
        self.system_id = system_id or str(uuid.uuid4())
        self.name = name
        self.tissues: Dict[str, WeyltonicTissue] = {}
        self.system_health = 100.0
        self.operational_status = "active"
        self.interconnections = {}
        
        print(f"Organ System '{name}' ({self.system_id}) created")
    
    def add_tissue(self, tissue: WeyltonicTissue, role: str = "support"):
        """Add a specialized tissue to the organ system"""
        tissue_key = f"{role}_{tissue.tissue_id}"
        self.tissues[tissue_key] = tissue
        print(f"Organ {self.name}: Added {tissue.tissue_type} tissue in {role} role")
    
    def execute_system_function(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the organ system's primary function - to be overridden"""
        raise NotImplementedError(f"System function not implemented for {self.name}")
    
    def maintain_system(self):
        """Maintain organ system health and coordination"""
        # Update system health based on tissue health
        if self.tissues:
            tissue_healths = []
            for tissue in self.tissues.values():
                status = tissue.get_tissue_status()
                tissue_healths.append(status['average_health'])
            
            self.system_health = np.mean(tissue_healths)
            
            # Update operational status
            if self.system_health > 80:
                self.operational_status = "optimal"
            elif self.system_health > 50:
                self.operational_status = "degraded"
            else:
                self.operational_status = "critical"
        
        # Coordinate tissue activities
        self._coordinate_tissues()
    
    def _coordinate_tissues(self):
        """Coordinate activities between tissues - to be overridden"""
        pass
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive organ system status"""
        tissue_statuses = {}
        for key, tissue in self.tissues.items():
            tissue_statuses[key] = tissue.get_tissue_status()
        
        return {
            'system_id': self.system_id,
            'name': self.name,
            'health': self.system_health,
            'status': self.operational_status,
            'tissue_count': len(self.tissues),
            'tissues': tissue_statuses,
            'interconnections': self.interconnections
        }


class VascularSystem(OrganSystem):
    """Dual-channel information transport system (xylem/phloem-like networks)"""
    
    def __init__(self, system_id: str = None):
        super().__init__("Vascular System", system_id)
        self.xylem_channels = {}  # Resource transport
        self.phloem_channels = {}  # Information transport
        self.transport_capacity = 100.0
        self.current_load = 0.0
        
    def establish_transport_channel(self, source: str, destination: str, 
                                  channel_type: str = "phloem"):
        """Establish a transport channel between nodes"""
        if channel_type == "xylem":
            self.xylem_channels[f"{source}->{destination}"] = {
                'capacity': 10.0,
                'current_flow': 0.0,
                'channel_health': 100.0
            }
        elif channel_type == "phloem":
            self.phloem_channels[f"{source}->{destination}"] = {
                'capacity': 15.0,
                'current_flow': 0.0,
                'channel_health': 100.0
            }
        
        print(f"Vascular: Established {channel_type} channel {source} -> {destination}")
    
    def execute_system_function(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute dual-channel transport function"""
        if inputs is None:
            inputs = {}
        
        results = {
            'system_function': 'dual_channel_transport',
            'xylem_status': self._transport_resources(inputs.get('resources', {})),
            'phloem_status': self._transport_information(inputs.get('information', {})),
            'total_channels': len(self.xylem_channels) + len(self.phloem_channels),
            'system_load': self.current_load / self.transport_capacity
        }
        
        return results
    
    def _transport_resources(self, resources: Dict[str, Any]) -> Dict[str, Any]:
        """Transport resources through xylem channels"""
        transported = {}
        
        for channel_id, channel in self.xylem_channels.items():
            if channel['channel_health'] > 50:
                # Simulate resource transport
                resource_amount = resources.get('energy', 0) * 0.1
                if resource_amount <= channel['capacity']:
                    channel['current_flow'] = resource_amount
                    transported[channel_id] = resource_amount
                    
        return {
            'channels_active': len([c for c in self.xylem_channels.values() 
                                  if c['channel_health'] > 50]),
            'total_transported': sum(transported.values()),
            'channel_details': transported
        }
    
    def _transport_information(self, information: Dict[str, Any]) -> Dict[str, Any]:
        """Transport information through phloem channels"""
        routed = {}
        
        for channel_id, channel in self.phloem_channels.items():
            if channel['channel_health'] > 50:
                # Simulate information routing
                info_packets = information.get('data_packets', [])
                packets_routed = min(len(info_packets), int(channel['capacity']))
                channel['current_flow'] = packets_routed
                routed[channel_id] = packets_routed
        
        return {
            'channels_active': len([c for c in self.phloem_channels.values() 
                                  if c['channel_health'] > 50]),
            'total_packets_routed': sum(routed.values()),
            'routing_details': routed
        }
    
    def _coordinate_tissues(self):
        """Coordinate vascular tissues for optimal transport"""
        # Balance load across transport tissues
        transport_tissues = [t for t in self.tissues.values() 
                           if t.tissue_type == 'transport']
        
        if transport_tissues:
            total_capacity = sum(len(t.cells) * 10 for t in transport_tissues)
            self.transport_capacity = total_capacity
            
            # Distribute load evenly
            target_load = self.current_load / len(transport_tissues)
            for tissue in transport_tissues:
                tissue.coordinate_function({'target_load': target_load})


class SupportSystem(OrganSystem):
    """Quantum scaffolding with dynamic structural adaptation"""
    
    def __init__(self, system_id: str = None):
        super().__init__("Support System", system_id)
        self.structural_integrity = 100.0
        self.scaffold_nodes = {}
        self.adaptation_capability = 0.8
        
    def add_scaffold_node(self, node_id: str, position: tuple, strength: float = 1.0):
        """Add a structural scaffold node"""
        self.scaffold_nodes[node_id] = {
            'position': position,
            'strength': strength,
            'connections': [],
            'load': 0.0
        }
        
    def execute_system_function(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute structural support and adaptation"""
        if inputs is None:
            inputs = {}
        
        # Assess structural loads
        structural_loads = inputs.get('structural_loads', {})
        adaptation_required = inputs.get('adapt_structure', False)
        
        results = {
            'system_function': 'quantum_scaffolding',
            'structural_integrity': self.structural_integrity,
            'load_distribution': self._distribute_loads(structural_loads),
            'adaptation_status': 'idle'
        }
        
        if adaptation_required:
            results['adaptation_status'] = self._adapt_structure(inputs.get('damage_locations', []))
        
        return results
    
    def _distribute_loads(self, loads: Dict[str, float]) -> Dict[str, Any]:
        """Distribute structural loads across scaffold nodes"""
        load_distribution = {}
        total_load = sum(loads.values())
        
        # Distribute loads based on node strength and position
        for node_id, node in self.scaffold_nodes.items():
            node_capacity = node['strength'] * 10
            allocated_load = min(node_capacity, total_load * 0.1)
            node['load'] = allocated_load
            load_distribution[node_id] = allocated_load
            
        return {
            'total_load': total_load,
            'nodes_engaged': len(load_distribution),
            'load_per_node': load_distribution,
            'system_stress': total_load / (len(self.scaffold_nodes) * 10)
        }
    
    def _adapt_structure(self, damage_locations: List[tuple]) -> str:
        """Adapt structure to route around damage"""
        if not damage_locations:
            return 'no_adaptation_needed'
        
        adaptations_made = 0
        for damage_location in damage_locations:
            # Find nearest scaffold nodes
            nearest_nodes = self._find_nearest_nodes(damage_location, radius=2.0)
            
            # Reroute connections around damage
            for node_id in nearest_nodes:
                if node_id in self.scaffold_nodes:
                    # Strengthen alternative pathways
                    self.scaffold_nodes[node_id]['strength'] *= 1.1
                    adaptations_made += 1
        
        self.structural_integrity = max(50.0, self.structural_integrity - len(damage_locations) * 5)
        
        return f'adapted_{adaptations_made}_connections'
    
    def _find_nearest_nodes(self, location: tuple, radius: float) -> List[str]:
        """Find scaffold nodes within radius of a location"""
        x, y = location
        nearby_nodes = []
        
        for node_id, node in self.scaffold_nodes.items():
            nx, ny = node['position']
            distance = np.sqrt((x - nx)**2 + (y - ny)**2)
            if distance <= radius:
                nearby_nodes.append(node_id)
                
        return nearby_nodes


class ProcessingSystem(OrganSystem):
    """Computational photosynthesis - primary processing engine"""
    
    def __init__(self, system_id: str = None):
        super().__init__("Processing System", system_id)
        self.processing_power = 0.0
        self.quantum_efficiency = 0.8
        self.light_absorption = 1.0
        
    def execute_system_function(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute computational photosynthesis"""
        if inputs is None:
            inputs = {}
        
        light_input = inputs.get('light_data', 1.0)
        processing_tasks = inputs.get('processing_tasks', [])
        
        # Calculate total processing power from computational tissues
        self._calculate_processing_power()
        
        results = {
            'system_function': 'computational_photosynthesis',
            'light_processed': light_input * self.light_absorption,
            'energy_generated': self._generate_energy(light_input),
            'tasks_processed': self._process_tasks(processing_tasks),
            'quantum_efficiency': self.quantum_efficiency,
            'total_processing_power': self.processing_power
        }
        
        return results
    
    def _calculate_processing_power(self):
        """Calculate total system processing power"""
        total_power = 0.0
        
        for tissue in self.tissues.values():
            if tissue.tissue_type == 'computational':
                for cell in tissue.cells:
                    chloroplast = cell.organelles.get('chloroplast')
                    if chloroplast and hasattr(chloroplast, 'processing_power'):
                        total_power += chloroplast.processing_power
        
        self.processing_power = total_power
    
    def _generate_energy(self, light_input: float) -> float:
        """Generate energy through photosynthesis-like process"""
        base_energy = light_input * self.light_absorption * self.quantum_efficiency
        
        # Distribute energy to computational tissues
        for tissue in self.tissues.values():
            if tissue.tissue_type == 'computational':
                tissue.coordinate_function({
                    'light_level': light_input,
                    'energy_boost': base_energy / len(self.tissues)
                })
        
        return base_energy
    
    def _process_tasks(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process computational tasks across the system"""
        if not tasks:
            return {'tasks_completed': 0, 'processing_time': 0}
        
        processing_results = []
        total_processing_time = 0.0
        
        # Distribute tasks across computational tissues
        computational_tissues = [t for t in self.tissues.values() 
                               if t.tissue_type == 'computational']
        
        if computational_tissues:
            tasks_per_tissue = len(tasks) // len(computational_tissues)
            
            for i, tissue in enumerate(computational_tissues):
                start_idx = i * tasks_per_tissue
                end_idx = (start_idx + tasks_per_tissue 
                          if i < len(computational_tissues) - 1 
                          else len(tasks))
                
                tissue_tasks = tasks[start_idx:end_idx]
                if tissue_tasks:
                    result = tissue.coordinate_function({
                        'processing_tasks': tissue_tasks
                    })
                    processing_results.append(result)
                    total_processing_time += len(tissue_tasks) / self.processing_power
        
        return {
            'tasks_completed': len(tasks),
            'processing_time': total_processing_time,
            'tissue_results': processing_results
        }
    
    def _coordinate_tissues(self):
        """Coordinate processing tissues for optimal performance"""
        computational_tissues = [t for t in self.tissues.values() 
                               if t.tissue_type == 'computational']
        
        if len(computational_tissues) > 1:
            # Balance workloads
            avg_load = np.mean([len(t.cells) for t in computational_tissues])
            
            for tissue in computational_tissues:
                if len(tissue.cells) < avg_load * 0.8:
                    # Trigger growth in underutilized tissues
                    tissue.grow()


class RespiratorySystem(OrganSystem):
    """Quantum-classical interface management"""
    
    def __init__(self, system_id: str = None):
        super().__init__("Respiratory System", system_id)
        self.quantum_coherence = 0.9
        self.classical_interface_efficiency = 0.85
        
    def execute_system_function(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute quantum-classical interface management"""
        if inputs is None:
            inputs = {}
        
        quantum_data = inputs.get('quantum_states', [])
        classical_data = inputs.get('classical_data', [])
        
        results = {
            'system_function': 'quantum_classical_interface',
            'quantum_to_classical': self._quantum_to_classical(quantum_data),
            'classical_to_quantum': self._classical_to_quantum(classical_data),
            'coherence_level': self.quantum_coherence,
            'interface_efficiency': self.classical_interface_efficiency
        }
        
        return results
    
    def _quantum_to_classical(self, quantum_data: List[Any]) -> Dict[str, Any]:
        """Convert quantum states to classical information"""
        converted_count = 0
        for state in quantum_data:
            # Simulate quantum measurement
            if self.quantum_coherence > 0.5:
                converted_count += 1
                # Decoherence effect
                self.quantum_coherence *= 0.999
        
        return {
            'states_converted': converted_count,
            'conversion_efficiency': converted_count / len(quantum_data) if quantum_data else 0,
            'remaining_coherence': self.quantum_coherence
        }
    
    def _classical_to_quantum(self, classical_data: List[Any]) -> Dict[str, Any]:
        """Convert classical data to quantum states"""
        prepared_states = min(len(classical_data), 
                            int(len(classical_data) * self.classical_interface_efficiency))
        
        return {
            'states_prepared': prepared_states,
            'preparation_efficiency': self.classical_interface_efficiency,
            'coherence_maintained': self.quantum_coherence > 0.7
        }


class ImmuneSystem(OrganSystem):
    """Adaptive defense and error correction mechanisms"""
    
    def __init__(self, system_id: str = None):
        super().__init__("Immune System", system_id)
        self.threat_database = {}
        self.response_strength = 1.0
        self.adaptation_rate = 0.1
        
    def execute_system_function(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute adaptive defense function"""
        if inputs is None:
            inputs = {}
        
        threats = inputs.get('detected_threats', [])
        system_errors = inputs.get('system_errors', [])
        
        results = {
            'system_function': 'adaptive_defense',
            'threats_neutralized': self._neutralize_threats(threats),
            'errors_corrected': self._correct_errors(system_errors),
            'system_immunity': len(self.threat_database),
            'response_strength': self.response_strength
        }
        
        return results
    
    def _neutralize_threats(self, threats: List[Dict[str, Any]]) -> int:
        """Neutralize system threats"""
        neutralized = 0
        
        for threat in threats:
            threat_type = threat.get('type', 'unknown')
            threat_severity = threat.get('severity', 1.0)
            
            if threat_type in self.threat_database:
                # Known threat - use learned response
                success_rate = self.threat_database[threat_type]['success_rate']
                if success_rate > 0.7:
                    neutralized += 1
            else:
                # New threat - learn and respond
                response_success = self.response_strength > threat_severity
                if response_success:
                    neutralized += 1
                
                # Add to database
                self.threat_database[threat_type] = {
                    'encounters': 1,
                    'success_rate': 1.0 if response_success else 0.0,
                    'severity': threat_severity
                }
        
        return neutralized
    
    def _correct_errors(self, errors: List[Dict[str, Any]]) -> int:
        """Correct system errors"""
        corrected = 0
        
        for error in errors:
            error_type = error.get('type', 'unknown')
            
            # Apply error correction based on type
            if error_type in ['data_corruption', 'transmission_error']:
                # High success rate for these errors
                if np.random.random() < 0.9:
                    corrected += 1
            elif error_type in ['logic_error', 'configuration_error']:
                # Medium success rate
                if np.random.random() < 0.7:
                    corrected += 1
            else:
                # Lower success rate for unknown errors
                if np.random.random() < 0.5:
                    corrected += 1
        
        return corrected
