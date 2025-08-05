"""
Weyl Semimetal Transport - Topologically protected quantum channels
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import uuid
from dataclasses import dataclass


@dataclass
class QuantumState:
    """Represents a quantum state for transport"""
    amplitude: complex
    phase: float
    coherence: float
    chirality: int  # +1 or -1 for Weyl node chirality


class WeylNode:
    """Individual Weyl node with specific chirality"""
    
    def __init__(self, node_id: str, position: Tuple[float, float, float], chirality: int):
        self.node_id = node_id
        self.position = position  # 3D position in momentum space
        self.chirality = chirality  # +1 or -1
        self.energy = 0.0
        self.occupancy = 0.0
        self.defects = []
        
    def add_defect(self, defect_type: str, severity: float):
        """Add a defect to the node"""
        self.defects.append({
            'type': defect_type,
            'severity': severity,
            'timestamp': np.random.randint(0, 1000)
        })
        
    def calculate_transport_coefficient(self) -> float:
        """Calculate transport coefficient considering defects"""
        base_coefficient = 1.0
        
        for defect in self.defects:
            # Topological protection reduces defect impact
            base_coefficient *= (1.0 - defect['severity'] * 0.1)
            
        return max(0.1, base_coefficient)  # Minimum due to topological protection


class WeylChannel:
    """
    Topologically protected quantum transport channel using Weyl semimetal edge states.
    These channels are inherently robust against local defects and can self-heal.
    """
    
    def __init__(self, channel_id: str, start_node: WeylNode, end_node: WeylNode):
        self.channel_id = channel_id
        self.start_node = start_node
        self.end_node = end_node
        self.length = self._calculate_length()
        self.defects = []
        self.transmission_probability = 1.0
        self.topological_protection = True
        self.chiral_anomaly_strength = 0.1
        
    def _calculate_length(self) -> float:
        """Calculate channel length in momentum space"""
        dx = self.end_node.position[0] - self.start_node.position[0]
        dy = self.end_node.position[1] - self.start_node.position[1]
        dz = self.end_node.position[2] - self.start_node.position[2]
        return np.sqrt(dx**2 + dy**2 + dz**2)
    
    def add_defect(self, location: float, defect_type: str = "scattering", severity: float = 0.1):
        """Add a defect to the channel"""
        if 0 <= location <= self.length:
            self.defects.append({
                'location': location,
                'type': defect_type,
                'severity': severity,
                'active': True
            })
            self._update_transmission_probability()
            print(f"WeylChannel {self.channel_id}: Added {defect_type} defect at {location:.2f}")
        
    def _update_transmission_probability(self):
        """Update transmission probability considering defects and topological protection"""
        if not self.topological_protection:
            # Without protection, defects severely impact transmission
            self.transmission_probability = 1.0
            for defect in self.defects:
                if defect['active']:
                    self.transmission_probability *= (1.0 - defect['severity'])
        else:
            # With topological protection, defects have minimal impact
            total_defect_impact = sum(d['severity'] for d in self.defects if d['active'])
            # Topological protection limits defect impact to square root
            self.transmission_probability = 1.0 - np.sqrt(total_defect_impact * 0.01)
            self.transmission_probability = max(0.8, self.transmission_probability)  # Strong protection
    
    def transmit_quantum_state(self, quantum_state: QuantumState) -> QuantumState:
        """
        Transmit quantum state through the channel with topological protection
        """
        if not quantum_state:
            return None
            
        # Apply chiral anomaly effects if nodes have opposite chirality
        if self.start_node.chirality != self.end_node.chirality:
            quantum_state = self._apply_chiral_anomaly(quantum_state)
        
        # Apply transmission probability
        transmission_success = np.random.random() < self.transmission_probability
        
        if transmission_success:
            # Successful transmission with minimal decoherence due to topological protection
            output_state = QuantumState(
                amplitude=quantum_state.amplitude * np.sqrt(self.transmission_probability),
                phase=quantum_state.phase + self._calculate_phase_shift(),
                coherence=quantum_state.coherence * 0.99,  # Minimal decoherence
                chirality=self.end_node.chirality
            )
            
            # Self-healing: attempt to bypass defects
            if self.defects:
                output_state = self._self_heal_transmission(output_state)
                
            return output_state
        else:
            # Transmission failed, but topological protection ensures partial recovery
            return QuantumState(
                amplitude=quantum_state.amplitude * 0.5,
                phase=quantum_state.phase,
                coherence=quantum_state.coherence * 0.8,
                chirality=quantum_state.chirality
            )
    
    def _apply_chiral_anomaly(self, quantum_state: QuantumState) -> QuantumState:
        """Apply chiral anomaly effects for novel computational primitives"""
        # Chiral anomaly creates charge pumping between opposite chirality nodes
        anomaly_factor = self.chiral_anomaly_strength * (
            self.start_node.chirality - self.end_node.chirality
        )
        
        # This can be used for unique quantum computations
        enhanced_amplitude = quantum_state.amplitude * (1.0 + anomaly_factor * 0.1j)
        phase_shift = anomaly_factor * np.pi / 4
        
        return QuantumState(
            amplitude=enhanced_amplitude,
            phase=quantum_state.phase + phase_shift,
            coherence=quantum_state.coherence,
            chirality=quantum_state.chirality
        )
    
    def _calculate_phase_shift(self) -> float:
        """Calculate geometric phase shift during transport"""
        # Berry phase from Weyl node geometry
        base_phase = self.length * 0.1
        
        # Topological contribution
        topological_phase = np.pi * (self.start_node.chirality - self.end_node.chirality) / 2
        
        return base_phase + topological_phase
    
    def _self_heal_transmission(self, quantum_state: QuantumState) -> QuantumState:
        """
        Self-healing capability where information reroutes around damage.
        This is an inherent property of topologically protected channels.
        """
        healing_efficiency = 0.9  # High efficiency due to topological protection
        
        # Count active defects
        active_defects = sum(1 for d in self.defects if d['active'])
        
        if active_defects > 0:
            print(f"WeylChannel {self.channel_id}: Self-healing around {active_defects} defects")
            
            # Topological protection enables rerouting with minimal loss
            healed_coherence = quantum_state.coherence * healing_efficiency
            healed_amplitude = quantum_state.amplitude * np.sqrt(healing_efficiency)
            
            # Attempt to deactivate some defects through healing
            for defect in self.defects:
                if defect['active'] and np.random.random() < 0.3:  # 30% healing chance
                    defect['active'] = False
                    print(f"WeylChannel {self.channel_id}: Healed {defect['type']} defect")
            
            self._update_transmission_probability()
            
            return QuantumState(
                amplitude=healed_amplitude,
                phase=quantum_state.phase,
                coherence=healed_coherence,
                chirality=quantum_state.chirality
            )
        
        return quantum_state
    
    def get_channel_status(self) -> Dict[str, Any]:
        """Get comprehensive channel status"""
        active_defects = [d for d in self.defects if d['active']]
        
        return {
            'channel_id': self.channel_id,
            'length': self.length,
            'transmission_probability': self.transmission_probability,
            'topological_protection': self.topological_protection,
            'defect_count': len(self.defects),
            'active_defects': len(active_defects),
            'self_healing_active': len(active_defects) > 0,
            'chiral_anomaly_strength': self.chiral_anomaly_strength,
            'start_node': {
                'id': self.start_node.node_id,
                'chirality': self.start_node.chirality,
                'position': self.start_node.position
            },
            'end_node': {
                'id': self.end_node.node_id,
                'chirality': self.end_node.chirality,
                'position': self.end_node.position
            }
        }


class WeylTransportNetwork:
    """Network of interconnected Weyl channels forming a transport substrate"""
    
    def __init__(self, network_id: str = None):
        self.network_id = network_id or str(uuid.uuid4())
        self.nodes: Dict[str, WeylNode] = {}
        self.channels: Dict[str, WeylChannel] = {}
        self.network_coherence = 1.0
        self.fault_tolerance = 0.9
        
    def add_weyl_node(self, position: Tuple[float, float, float], chirality: int) -> str:
        """Add a Weyl node to the network"""
        node_id = f"node_{len(self.nodes)}"
        node = WeylNode(node_id, position, chirality)
        self.nodes[node_id] = node
        
        print(f"WeylNetwork: Added {chirality:+d} chirality node at {position}")
        return node_id
    
    def create_channel(self, start_node_id: str, end_node_id: str) -> Optional[str]:
        """Create a transport channel between two nodes"""
        if start_node_id not in self.nodes or end_node_id not in self.nodes:
            return None
            
        channel_id = f"{start_node_id}_to_{end_node_id}"
        start_node = self.nodes[start_node_id]
        end_node = self.nodes[end_node_id]
        
        channel = WeylChannel(channel_id, start_node, end_node)
        self.channels[channel_id] = channel
        
        print(f"WeylNetwork: Created channel {channel_id}")
        return channel_id
    
    def route_quantum_state(self, quantum_state: QuantumState, 
                          start_node_id: str, end_node_id: str) -> Optional[QuantumState]:
        """Route quantum state through the network"""
        # Find path from start to end
        path = self._find_path(start_node_id, end_node_id)
        
        if not path:
            print(f"WeylNetwork: No path found from {start_node_id} to {end_node_id}")
            return None
        
        current_state = quantum_state
        
        # Transmit through each channel in the path
        for i in range(len(path) - 1):
            channel_id = f"{path[i]}_to_{path[i+1]}"
            if channel_id in self.channels:
                channel = self.channels[channel_id]
                current_state = channel.transmit_quantum_state(current_state)
                
                if current_state is None or current_state.coherence < 0.1:
                    print(f"WeylNetwork: Transmission failed at channel {channel_id}")
                    return None
            else:
                print(f"WeylNetwork: Channel {channel_id} not found")
                return None
        
        return current_state
    
    def _find_path(self, start_id: str, end_id: str) -> List[str]:
        """Find path between nodes using simple pathfinding"""
        # For now, direct connection or single hop
        direct_channel = f"{start_id}_to_{end_id}"
        if direct_channel in self.channels:
            return [start_id, end_id]
        
        # Try single hop through other nodes
        for intermediate_id in self.nodes:
            if intermediate_id != start_id and intermediate_id != end_id:
                channel1 = f"{start_id}_to_{intermediate_id}"
                channel2 = f"{intermediate_id}_to_{end_id}"
                if channel1 in self.channels and channel2 in self.channels:
                    return [start_id, intermediate_id, end_id]
        
        return []  # No path found
    
    def introduce_network_damage(self, damage_fraction: float = 0.1):
        """Introduce random damage to test fault tolerance"""
        num_channels_to_damage = int(len(self.channels) * damage_fraction)
        channels_to_damage = np.random.choice(
            list(self.channels.keys()), 
            size=min(num_channels_to_damage, len(self.channels)),
            replace=False
        )
        
        for channel_id in channels_to_damage:
            channel = self.channels[channel_id]
            defect_location = np.random.uniform(0, channel.length)
            defect_severity = np.random.uniform(0.1, 0.5)
            channel.add_defect(defect_location, "random_damage", defect_severity)
        
        print(f"WeylNetwork: Introduced damage to {len(channels_to_damage)} channels")
    
    def measure_network_performance(self) -> Dict[str, Any]:
        """Measure overall network performance"""
        total_channels = len(self.channels)
        functional_channels = sum(
            1 for channel in self.channels.values() 
            if channel.transmission_probability > 0.5
        )
        
        avg_transmission = np.mean([
            channel.transmission_probability 
            for channel in self.channels.values()
        ]) if self.channels else 0
        
        total_defects = sum(
            len(channel.defects) 
            for channel in self.channels.values()
        )
        
        return {
            'network_id': self.network_id,
            'total_nodes': len(self.nodes),
            'total_channels': total_channels,
            'functional_channels': functional_channels,
            'network_efficiency': functional_channels / total_channels if total_channels > 0 else 0,
            'average_transmission': avg_transmission,
            'total_defects': total_defects,
            'network_coherence': self.network_coherence,
            'fault_tolerance': self.fault_tolerance
        }
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get comprehensive network status"""
        node_statuses = {}
        for node_id, node in self.nodes.items():
            node_statuses[node_id] = {
                'position': node.position,
                'chirality': node.chirality,
                'defect_count': len(node.defects),
                'transport_coefficient': node.calculate_transport_coefficient()
            }
        
        channel_statuses = {}
        for channel_id, channel in self.channels.items():
            channel_statuses[channel_id] = channel.get_channel_status()
        
        return {
            'network_id': self.network_id,
            'performance': self.measure_network_performance(),
            'nodes': node_statuses,
            'channels': channel_statuses
        }


def create_test_weyl_network() -> WeylTransportNetwork:
    """Create a test Weyl transport network for demonstration"""
    network = WeylTransportNetwork("test_network")
    
    # Add nodes with alternating chirality
    positions = [
        (0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0),
        (0.5, 0.5, 1), (0.5, 0.5, -1)
    ]
    chiralities = [1, -1, 1, -1, 1, -1]
    
    node_ids = []
    for pos, chirality in zip(positions, chiralities):
        node_id = network.add_weyl_node(pos, chirality)
        node_ids.append(node_id)
    
    # Create channels between nodes
    connections = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Square ring
        (0, 4), (1, 4), (2, 5), (3, 5)   # Vertical connections
    ]
    
    for start_idx, end_idx in connections:
        network.create_channel(node_ids[start_idx], node_ids[end_idx])
    
    return network
