"""
Quantum Coherence Management - Maintaining quantum states in biological environments
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import uuid
from dataclasses import dataclass
from enum import Enum


class DecoherenceSource(Enum):
    """Types of decoherence sources in biological environments"""
    THERMAL_NOISE = "thermal_noise"
    ELECTROMAGNETIC = "electromagnetic"
    MECHANICAL_VIBRATION = "mechanical_vibration"
    CHEMICAL_INTERACTION = "chemical_interaction"
    MEASUREMENT = "measurement"


@dataclass
class CoherenceDomain:
    """Localized region maintaining quantum coherence"""
    domain_id: str
    center_position: Tuple[float, float, float]
    radius: float
    coherence_time: float  # T2 time
    current_coherence: float
    protection_level: float


class EnvironmentalNoiseModel:
    """Models environmental noise in biological quantum systems"""
    
    def __init__(self, temperature: float = 310.0):  # Body temperature in Kelvin
        self.temperature = temperature
        self.noise_sources = {}
        self.coupling_strengths = {}
        
        # Initialize typical biological noise sources
        self._initialize_biological_noise()
    
    def _initialize_biological_noise(self):
        """Initialize noise sources typical in biological environments"""
        self.noise_sources = {
            DecoherenceSource.THERMAL_NOISE: {
                'strength': self._calculate_thermal_noise(),
                'correlation_time': 1e-12,  # picoseconds
                'spectral_density': 'ohmic'
            },
            DecoherenceSource.ELECTROMAGNETIC: {
                'strength': 0.1,
                'correlation_time': 1e-9,  # nanoseconds
                'spectral_density': '1/f'
            },
            DecoherenceSource.MECHANICAL_VIBRATION: {
                'strength': 0.05,
                'correlation_time': 1e-6,  # microseconds
                'spectral_density': 'lorentzian'
            },
            DecoherenceSource.CHEMICAL_INTERACTION: {
                'strength': 0.2,
                'correlation_time': 1e-8,  # tens of nanoseconds
                'spectral_density': 'super_ohmic'
            }
        }
    
    def _calculate_thermal_noise(self) -> float:
        """Calculate thermal noise strength based on temperature"""
        k_B = 1.381e-23  # Boltzmann constant
        h_bar = 1.055e-34  # Reduced Planck constant
        
        # Typical energy scale for biological quantum processes
        energy_scale = k_B * self.temperature
        return energy_scale / h_bar  # Convert to frequency units
    
    def get_decoherence_rate(self, frequency: float, 
                           coupling_strength: float = 1.0) -> float:
        """Calculate total decoherence rate at given frequency"""
        total_rate = 0.0
        
        for source, params in self.noise_sources.items():
            spectral_density = self._calculate_spectral_density(
                frequency, params['spectral_density'], params['strength']
            )
            
            # Decoherence rate from Fermi's Golden Rule
            rate = coupling_strength**2 * spectral_density * params['correlation_time']
            total_rate += rate
        
        return total_rate
    
    def _calculate_spectral_density(self, frequency: float, 
                                  density_type: str, strength: float) -> float:
        """Calculate spectral density for different noise types"""
        if density_type == 'ohmic':
            return strength * frequency
        elif density_type == '1/f':
            return strength / max(frequency, 1e-6)  # Avoid division by zero
        elif density_type == 'lorentzian':
            gamma = 1e6  # Cutoff frequency
            return strength * gamma / (frequency**2 + gamma**2)
        elif density_type == 'super_ohmic':
            return strength * frequency**3
        else:
            return strength  # Flat spectrum


class CoherenceTracker:
    """
    Tracks quantum coherence in biological computing regions.
    Models decoherence and implements maintenance strategies.
    """
    
    def __init__(self, system_id: str = None, initial_coherence: float = 1.0):
        self.system_id = system_id or str(uuid.uuid4())
        self.current_coherence = initial_coherence
        self.initial_coherence = initial_coherence
        self.coherence_history = [initial_coherence]
        
        # Environment and protection
        self.noise_model = EnvironmentalNoiseModel()
        self.protection_strategies = []
        self.coherence_domains = {}
        
        # Timekeeping
        self.time_step = 1e-9  # nanosecond resolution
        self.current_time = 0.0
        
        # Decoherence parameters
        self.base_decoherence_rate = 1e-6  # 1/μs
        self.topological_protection_factor = 0.1  # Strong protection
        
    def add_coherence_domain(self, center: Tuple[float, float, float], 
                           radius: float, coherence_time: float) -> str:
        """Add a localized coherence domain"""
        domain_id = f"domain_{len(self.coherence_domains)}"
        domain = CoherenceDomain(
            domain_id=domain_id,
            center_position=center,
            radius=radius,
            coherence_time=coherence_time,
            current_coherence=1.0,
            protection_level=0.8
        )
        
        self.coherence_domains[domain_id] = domain
        print(f"CoherenceTracker: Added domain {domain_id} at {center}")
        return domain_id
    
    def update_coherence(self, time_step: float = None):
        """Update coherence considering environmental decoherence"""
        if time_step is None:
            time_step = self.time_step
            
        self.current_time += time_step
        
        # Calculate decoherence rate
        effective_rate = self._calculate_effective_decoherence_rate()
        
        # Apply decoherence (exponential decay)
        decay_factor = np.exp(-effective_rate * time_step)
        self.current_coherence *= decay_factor
        
        # Update coherence domains
        self._update_coherence_domains(time_step)
        
        # Record in history
        self.coherence_history.append(self.current_coherence)
        
        # Limit history length
        if len(self.coherence_history) > 1000:
            self.coherence_history = self.coherence_history[-1000:]
    
    def _calculate_effective_decoherence_rate(self) -> float:
        """Calculate effective decoherence rate with protection"""
        base_rate = self.base_decoherence_rate
        
        # Apply topological protection
        protected_rate = base_rate * self.topological_protection_factor
        
        # Environmental noise contribution
        noise_rate = self.noise_model.get_decoherence_rate(1e9)  # 1 GHz reference
        
        # Protection strategies reduce effective rate
        strategy_factor = 1.0
        for strategy in self.protection_strategies:
            strategy_factor *= strategy.get('effectiveness', 1.0)
        
        total_rate = (protected_rate + noise_rate) * strategy_factor
        return max(1e-12, total_rate)  # Minimum rate due to fundamental limits
    
    def _update_coherence_domains(self, time_step: float):
        """Update individual coherence domains"""
        for domain in self.coherence_domains.values():
            # Domain-specific decoherence
            domain_rate = 1.0 / domain.coherence_time
            domain_rate *= (1.0 - domain.protection_level)  # Protection effect
            
            decay = np.exp(-domain_rate * time_step)
            domain.current_coherence *= decay
            
            # Domains can exchange coherence
            if domain.current_coherence < 0.5:
                self._attempt_coherence_transfer(domain)
    
    def _attempt_coherence_transfer(self, target_domain: CoherenceDomain):
        """Attempt to transfer coherence between domains"""
        for donor_domain in self.coherence_domains.values():
            if (donor_domain.domain_id != target_domain.domain_id and 
                donor_domain.current_coherence > 0.8):
                
                # Calculate transfer efficiency based on distance
                distance = np.linalg.norm(
                    np.array(donor_domain.center_position) - 
                    np.array(target_domain.center_position)
                )
                
                transfer_efficiency = np.exp(-distance / 10.0)  # Exponential decay
                
                if transfer_efficiency > 0.1:
                    transfer_amount = 0.1 * transfer_efficiency
                    donor_domain.current_coherence -= transfer_amount
                    target_domain.current_coherence += transfer_amount
                    
                    print(f"Coherence transfer: {donor_domain.domain_id} -> {target_domain.domain_id}")
                    break
    
    def apply_coherence_maintenance(self, strategy: str = "topological", 
                                  strength: float = 1.0):
        """Apply coherence maintenance strategy"""
        if strategy == "topological":
            self._apply_topological_protection(strength)
        elif strategy == "active_correction":
            self._apply_active_error_correction(strength)
        elif strategy == "environmental_decoupling":
            self._apply_environmental_decoupling(strength)
        elif strategy == "dynamical_decoupling":
            self._apply_dynamical_decoupling(strength)
        else:
            print(f"Unknown coherence maintenance strategy: {strategy}")
    
    def _apply_topological_protection(self, strength: float):
        """Apply topological protection to maintain coherence"""
        # Topological protection inherently reduces decoherence
        protection_boost = 0.05 * strength
        
        self.current_coherence = min(1.0, self.current_coherence + protection_boost)
        self.topological_protection_factor *= (1.0 - 0.1 * strength)
        
        # Add to active strategies
        strategy = {
            'type': 'topological',
            'effectiveness': 0.9 * strength,
            'duration': 100  # Time steps
        }
        self.protection_strategies.append(strategy)
        
        print(f"Applied topological protection (strength={strength:.2f}). "
              f"Coherence: {self.current_coherence:.3f}")
    
    def _apply_active_error_correction(self, strength: float):
        """Apply active quantum error correction"""
        # Error correction can restore coherence but is resource-intensive
        correction_boost = 0.15 * strength
        
        # Only effective if coherence hasn't dropped too low
        if self.current_coherence > 0.3:
            self.current_coherence = min(1.0, self.current_coherence + correction_boost)
            
            strategy = {
                'type': 'active_correction',
                'effectiveness': 0.8 * strength,
                'duration': 50
            }
            self.protection_strategies.append(strategy)
            
            print(f"Applied active error correction (strength={strength:.2f}). "
                  f"Coherence: {self.current_coherence:.3f}")
        else:
            print("Active correction failed: coherence too low")
    
    def _apply_environmental_decoupling(self, strength: float):
        """Apply environmental decoupling techniques"""
        # Reduce coupling to environmental noise
        for noise_source in self.noise_model.noise_sources.values():
            noise_source['strength'] *= (1.0 - 0.2 * strength)
        
        strategy = {
            'type': 'environmental_decoupling',
            'effectiveness': 0.7 * strength,
            'duration': 200
        }
        self.protection_strategies.append(strategy)
        
        print(f"Applied environmental decoupling (strength={strength:.2f})")
    
    def _apply_dynamical_decoupling(self, strength: float):
        """Apply dynamical decoupling pulse sequences"""
        # Simulate effect of decoupling pulses
        pulse_effectiveness = 0.6 * strength
        
        # Temporarily boost coherence
        if np.random.random() < pulse_effectiveness:
            coherence_boost = 0.1 * strength
            self.current_coherence = min(1.0, self.current_coherence + coherence_boost)
        
        strategy = {
            'type': 'dynamical_decoupling',
            'effectiveness': pulse_effectiveness,
            'duration': 20
        }
        self.protection_strategies.append(strategy)
        
        print(f"Applied dynamical decoupling (strength={strength:.2f})")
    
    def cleanup_expired_strategies(self):
        """Remove expired protection strategies"""
        active_strategies = []
        
        for strategy in self.protection_strategies:
            strategy['duration'] -= 1
            if strategy['duration'] > 0:
                active_strategies.append(strategy)
        
        self.protection_strategies = active_strategies
    
    def calculate_coherence_time(self) -> float:
        """Calculate T2 coherence time"""
        if self.current_coherence <= 0:
            return 0.0
            
        # T2 time based on current decoherence rate
        effective_rate = self._calculate_effective_decoherence_rate()
        return 1.0 / effective_rate if effective_rate > 0 else float('inf')
    
    def get_coherence_metrics(self) -> Dict[str, Any]:
        """Get comprehensive coherence metrics"""
        t2_time = self.calculate_coherence_time()
        
        # Calculate average coherence over recent history
        recent_history = self.coherence_history[-100:] if len(self.coherence_history) >= 100 else self.coherence_history
        avg_coherence = np.mean(recent_history) if recent_history else 0
        
        # Domain statistics
        domain_stats = {}
        for domain_id, domain in self.coherence_domains.items():
            domain_stats[domain_id] = {
                'coherence': domain.current_coherence,
                'coherence_time': domain.coherence_time,
                'protection_level': domain.protection_level,
                'position': domain.center_position
            }
        
        return {
            'system_id': self.system_id,
            'current_coherence': self.current_coherence,
            'coherence_time_t2': t2_time,
            'average_coherence': avg_coherence,
            'coherence_degradation': 1.0 - (self.current_coherence / self.initial_coherence),
            'active_strategies': len(self.protection_strategies),
            'coherence_domains': len(self.coherence_domains),
            'domain_details': domain_stats,
            'environmental_temperature': self.noise_model.temperature,
            'topological_protection_factor': self.topological_protection_factor,
            'simulation_time': self.current_time
        }
    
    def simulate_coherence_evolution(self, duration: float, 
                                   maintenance_interval: float = 1e-6) -> List[float]:
        """Simulate coherence evolution over time with periodic maintenance"""
        evolution = []
        steps = int(duration / self.time_step)
        maintenance_steps = int(maintenance_interval / self.time_step)
        
        for step in range(steps):
            self.update_coherence()
            
            # Apply maintenance periodically
            if step % maintenance_steps == 0 and step > 0:
                # Random choice of maintenance strategy
                strategies = ["topological", "active_correction", 
                            "environmental_decoupling", "dynamical_decoupling"]
                strategy = np.random.choice(strategies)
                strength = np.random.uniform(0.5, 1.0)
                self.apply_coherence_maintenance(strategy, strength)
            
            # Cleanup expired strategies
            if step % 10 == 0:
                self.cleanup_expired_strategies()
            
            evolution.append(self.current_coherence)
        
        return evolution
    
    def get_coherence_level(self) -> float:
        """Get current coherence level (compatibility method)"""
        return self.current_coherence
    
    def __str__(self):
        return f"CoherenceTracker(coherence={self.current_coherence:.3f}, T2={self.calculate_coherence_time():.2e}s)"
    
    def __repr__(self):
        return self.__str__()
