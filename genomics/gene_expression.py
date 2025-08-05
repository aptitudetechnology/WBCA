"""
Gene Expression Engine - Dynamic reconfiguration and regulation
Real-time FPGA reconfiguration based on genetic programs
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import time
from enum import Enum
from dataclasses import dataclass

from .genetic_code import GeneticProgram, GeneticInstruction, InstructionType


class ExpressionLevel(Enum):
    """Gene expression levels"""
    SILENT = 0.0
    LOW = 0.25
    MODERATE = 0.5
    HIGH = 0.75
    MAXIMUM = 1.0


@dataclass
class GeneExpressionProfile:
    """Expression profile for a specific gene"""
    gene_id: str
    base_expression: float
    current_expression: float
    regulation_factors: Dict[str, float]
    last_updated: float


class RegulatoryNetwork:
    """Models regulatory interactions between genes"""
    
    def __init__(self):
        self.regulations = {}  # gene_id -> {regulator_id: strength}
        self.feedback_loops = []
        self.network_state = {}
        
    def add_regulation(self, regulator: str, target: str, strength: float):
        """Add regulatory relationship"""
        if target not in self.regulations:
            self.regulations[target] = {}
        self.regulations[target][regulator] = strength
        
    def add_feedback_loop(self, genes: List[str], loop_type: str = "positive"):
        """Add feedback loop between genes"""
        self.feedback_loops.append({
            'genes': genes,
            'type': loop_type,
            'strength': 1.0
        })
        
    def calculate_regulation_effect(self, target_gene: str, 
                                  current_expressions: Dict[str, float]) -> float:
        """Calculate regulatory effect on target gene"""
        if target_gene not in self.regulations:
            return 1.0  # No regulation
            
        total_effect = 1.0
        
        for regulator, strength in self.regulations[target_gene].items():
            if regulator in current_expressions:
                regulator_expression = current_expressions[regulator]
                
                if strength > 0:  # Positive regulation (activation)
                    effect = 1.0 + (strength * regulator_expression)
                else:  # Negative regulation (repression)
                    effect = 1.0 + (strength * (1.0 - regulator_expression))
                
                total_effect *= effect
        
        return np.clip(total_effect, 0.1, 2.0)  # Limit regulation effect


class CellularDifferentiation:
    """Manages cellular differentiation processes"""
    
    def __init__(self):
        self.differentiation_pathways = {}
        self.current_lineage = "undifferentiated"
        self.differentiation_progress = 0.0
        self.commitment_threshold = 0.8
        
    def add_pathway(self, from_type: str, to_type: str, 
                   required_expressions: Dict[str, float]):
        """Add differentiation pathway"""
        pathway_id = f"{from_type}_to_{to_type}"
        self.differentiation_pathways[pathway_id] = {
            'from': from_type,
            'to': to_type,
            'requirements': required_expressions,
            'progress_rate': 0.1
        }
        
    def evaluate_differentiation(self, current_expressions: Dict[str, float]) -> Optional[str]:
        """Evaluate possible differentiation based on expression profile"""
        best_match = None
        best_score = 0.0
        
        for pathway_id, pathway in self.differentiation_pathways.items():
            if pathway['from'] == self.current_lineage:
                score = self._calculate_pathway_score(pathway, current_expressions)
                
                if score > best_score and score > self.commitment_threshold:
                    best_score = score
                    best_match = pathway
        
        if best_match:
            self.differentiation_progress += best_match['progress_rate']
            
            if self.differentiation_progress >= 1.0:
                old_lineage = self.current_lineage
                self.current_lineage = best_match['to']
                self.differentiation_progress = 0.0
                return f"differentiated_{old_lineage}_to_{self.current_lineage}"
        
        return None
    
    def _calculate_pathway_score(self, pathway: Dict[str, Any], 
                               expressions: Dict[str, float]) -> float:
        """Calculate how well current expressions match pathway requirements"""
        requirements = pathway['requirements']
        total_score = 0.0
        
        for gene, required_level in requirements.items():
            if gene in expressions:
                current_level = expressions[gene]
                # Score based on how close current level is to required
                score = 1.0 - abs(current_level - required_level)
                total_score += max(0, score)
        
        return total_score / len(requirements) if requirements else 0.0


class FPGAReconfigurationEngine:
    """Real-time FPGA reconfiguration based on gene expression"""
    
    def __init__(self):
        self.reconfiguration_queue = []
        self.active_configurations = {}
        self.reconfiguration_history = []
        self.max_reconfigurations_per_cycle = 5
        
    def queue_reconfiguration(self, target_organelle: str, 
                            new_config: Dict[str, Any], priority: int = 1):
        """Queue an FPGA reconfiguration"""
        reconfig = {
            'target': target_organelle,
            'configuration': new_config,
            'priority': priority,
            'timestamp': time.time(),
            'status': 'queued'
        }
        
        self.reconfiguration_queue.append(reconfig)
        self.reconfiguration_queue.sort(key=lambda x: (-x['priority'], x['timestamp']))
        
    def process_reconfigurations(self, organelles: Dict[str, Any]) -> List[str]:
        """Process queued reconfigurations"""
        processed = []
        reconfigurations_this_cycle = 0
        
        while (self.reconfiguration_queue and 
               reconfigurations_this_cycle < self.max_reconfigurations_per_cycle):
            
            reconfig = self.reconfiguration_queue.pop(0)
            target = reconfig['target']
            
            if target in organelles:
                success = self._apply_reconfiguration(organelles[target], reconfig)
                
                if success:
                    reconfig['status'] = 'completed'
                    processed.append(f"Reconfigured {target}")
                    
                    # Store active configuration
                    self.active_configurations[target] = reconfig['configuration']
                else:
                    reconfig['status'] = 'failed'
                    processed.append(f"Failed to reconfigure {target}")
                
                # Add to history
                self.reconfiguration_history.append(reconfig)
                reconfigurations_this_cycle += 1
        
        # Limit history size
        if len(self.reconfiguration_history) > 1000:
            self.reconfiguration_history = self.reconfiguration_history[-1000:]
        
        return processed
    
    def _apply_reconfiguration(self, organelle: Any, reconfig: Dict[str, Any]) -> bool:
        """Apply reconfiguration to organelle"""
        try:
            if hasattr(organelle, 'reconfigure'):
                organelle.reconfigure(reconfig['configuration'])
                return True
            else:
                # Direct parameter setting
                for param, value in reconfig['configuration'].items():
                    if hasattr(organelle, param):
                        setattr(organelle, param, value)
                return True
        except Exception as e:
            print(f"Reconfiguration error: {e}")
            return False
    
    def get_reconfiguration_status(self) -> Dict[str, Any]:
        """Get current reconfiguration status"""
        return {
            'queued_reconfigurations': len(self.reconfiguration_queue),
            'active_configurations': len(self.active_configurations),
            'total_reconfigurations': len(self.reconfiguration_history),
            'recent_failures': sum(1 for r in self.reconfiguration_history[-10:] 
                                 if r['status'] == 'failed')
        }


class GeneExpressionEngine:
    """
    Main engine for gene expression and dynamic reconfiguration
    Integrates regulatory networks, differentiation, and FPGA reconfiguration
    """
    
    def __init__(self):
        self.gene_profiles: Dict[str, GeneExpressionProfile] = {}
        self.regulatory_network = RegulatoryNetwork()
        self.differentiation_engine = CellularDifferentiation()
        self.fpga_engine = FPGAReconfigurationEngine()
        
        # Expression dynamics
        self.noise_level = 0.02
        self.time_constant = 1.0  # Expression change rate
        self.current_time = 0.0
        
        # Environmental factors
        self.environmental_signals = {}
        self.stress_level = 0.0
        
        self._initialize_default_profiles()
        self._setup_default_regulations()
        
    def _initialize_default_profiles(self):
        """Initialize default gene expression profiles"""
        default_genes = [
            'mitochondria_efficiency', 'chloroplast_processing', 'vacuole_capacity',
            'cytoplasm_routing', 'cell_wall_permeability', 'ribosome_activity',
            'nucleus_control', 'er_manufacturing', 'golgi_packaging'
        ]
        
        for gene in default_genes:
            self.gene_profiles[gene] = GeneExpressionProfile(
                gene_id=gene,
                base_expression=0.5,
                current_expression=0.5 + np.random.normal(0, 0.1),
                regulation_factors={},
                last_updated=0.0
            )
    
    def _setup_default_regulations(self):
        """Setup default regulatory relationships"""
        # Energy metabolism regulation
        self.regulatory_network.add_regulation('mitochondria_efficiency', 'chloroplast_processing', 0.3)
        self.regulatory_network.add_regulation('chloroplast_processing', 'mitochondria_efficiency', 0.2)
        
        # Manufacturing pipeline regulation
        self.regulatory_network.add_regulation('nucleus_control', 'ribosome_activity', 0.5)
        self.regulatory_network.add_regulation('ribosome_activity', 'er_manufacturing', 0.4)
        self.regulatory_network.add_regulation('er_manufacturing', 'golgi_packaging', 0.6)
        
        # Storage and transport regulation
        self.regulatory_network.add_regulation('vacuole_capacity', 'cytoplasm_routing', -0.2)
        self.regulatory_network.add_regulation('cytoplasm_routing', 'cell_wall_permeability', 0.3)
        
        # Feedback loops
        self.regulatory_network.add_feedback_loop(['mitochondria_efficiency', 'chloroplast_processing'])
        self.regulatory_network.add_feedback_loop(['ribosome_activity', 'er_manufacturing', 'golgi_packaging'])
    
    def express_genetic_program(self, program: GeneticProgram, organelles: Dict[str, Any]):
        """Express genetic program by updating gene expression and reconfiguring organelles"""
        expression_changes = []
        
        for instruction in program.instructions:
            if instruction.instruction_type == InstructionType.CONFIGURE:
                changes = self._process_configure_instruction(instruction, organelles)
                expression_changes.extend(changes)
            elif instruction.instruction_type == InstructionType.REGULATE:
                changes = self._process_regulate_instruction(instruction)
                expression_changes.extend(changes)
            elif instruction.instruction_type == InstructionType.SPECIALIZE:
                changes = self._process_specialize_instruction(instruction)
                expression_changes.extend(changes)
        
        # Update expression levels
        self._update_expression_dynamics()
        
        # Process FPGA reconfigurations
        reconfig_results = self.fpga_engine.process_reconfigurations(organelles)
        
        # Check for differentiation
        differentiation_result = self.differentiation_engine.evaluate_differentiation(
            {gene: profile.current_expression for gene, profile in self.gene_profiles.items()}
        )
        
        return {
            'expression_changes': expression_changes,
            'reconfigurations': reconfig_results,
            'differentiation': differentiation_result,
            'current_lineage': self.differentiation_engine.current_lineage
        }
    
    def _process_configure_instruction(self, instruction: GeneticInstruction, 
                                     organelles: Dict[str, Any]) -> List[str]:
        """Process CONFIGURE instruction"""
        changes = []
        target = instruction.target
        
        # Map organelle to relevant genes
        organelle_genes = {
            'mitochondria': 'mitochondria_efficiency',
            'chloroplast': 'chloroplast_processing',
            'vacuole': 'vacuole_capacity',
            'cytoplasm': 'cytoplasm_routing',
            'cell_wall': 'cell_wall_permeability'
        }
        
        if target in organelle_genes:
            gene = organelle_genes[target]
            
            # Increase expression for this gene
            if gene in self.gene_profiles:
                old_expression = self.gene_profiles[gene].current_expression
                self.gene_profiles[gene].current_expression = min(1.0, old_expression + 0.2)
                changes.append(f"Increased {gene} expression")
            
            # Queue FPGA reconfiguration
            self.fpga_engine.queue_reconfiguration(target, instruction.parameters, priority=2)
            changes.append(f"Queued reconfiguration for {target}")
        
        return changes
    
    def _process_regulate_instruction(self, instruction: GeneticInstruction) -> List[str]:
        """Process REGULATE instruction"""
        changes = []
        target_gene = instruction.target
        
        if target_gene in self.gene_profiles:
            # Apply regulation parameters
            for param, value in instruction.parameters.items():
                if param == 'expression_level':
                    self.gene_profiles[target_gene].current_expression = np.clip(value, 0.0, 1.0)
                    changes.append(f"Set {target_gene} expression to {value}")
                elif param == 'regulation_factor':
                    # Add regulation factor
                    factor_name = instruction.parameters.get('factor_name', 'external')
                    self.gene_profiles[target_gene].regulation_factors[factor_name] = value
                    changes.append(f"Added regulation factor {factor_name} to {target_gene}")
        
        return changes
    
    def _process_specialize_instruction(self, instruction: GeneticInstruction) -> List[str]:
        """Process SPECIALIZE instruction"""
        changes = []
        specialization_type = instruction.parameters.get('type', 'generic')
        
        # Define expression profiles for different specializations
        specialization_profiles = {
            'compute': {
                'chloroplast_processing': 0.9,
                'mitochondria_efficiency': 0.8,
                'cytoplasm_routing': 0.7
            },
            'memory': {
                'vacuole_capacity': 0.9,
                'er_manufacturing': 0.7,
                'golgi_packaging': 0.6
            },
            'transport': {
                'cytoplasm_routing': 0.9,
                'cell_wall_permeability': 0.8,
                'mitochondria_efficiency': 0.6
            },
            'sensory': {
                'cell_wall_permeability': 0.9,
                'nucleus_control': 0.8,
                'ribosome_activity': 0.7
            }
        }
        
        if specialization_type in specialization_profiles:
            profile = specialization_profiles[specialization_type]
            
            for gene, target_expression in profile.items():
                if gene in self.gene_profiles:
                    old_expression = self.gene_profiles[gene].current_expression
                    self.gene_profiles[gene].current_expression = target_expression
                    changes.append(f"Specialized {gene}: {old_expression:.2f} -> {target_expression:.2f}")
            
            # Set up differentiation pathway if not already committed
            if self.differentiation_engine.current_lineage == "undifferentiated":
                self.differentiation_engine.add_pathway(
                    "undifferentiated", 
                    specialization_type, 
                    profile
                )
                changes.append(f"Added differentiation pathway to {specialization_type}")
        
        return changes
    
    def _update_expression_dynamics(self):
        """Update gene expression levels based on regulatory network"""
        current_expressions = {
            gene: profile.current_expression 
            for gene, profile in self.gene_profiles.items()
        }
        
        for gene, profile in self.gene_profiles.items():
            # Calculate regulatory effects
            regulation_effect = self.regulatory_network.calculate_regulation_effect(
                gene, current_expressions
            )
            
            # Calculate target expression
            target_expression = profile.base_expression * regulation_effect
            
            # Apply environmental factors
            if self.environmental_signals:
                for signal, strength in self.environmental_signals.items():
                    if signal in profile.regulation_factors:
                        target_expression *= (1.0 + profile.regulation_factors[signal] * strength)
            
            # Add noise
            noise = np.random.normal(0, self.noise_level)
            target_expression += noise
            
            # Update expression with time constant
            expression_change = (target_expression - profile.current_expression) / self.time_constant
            profile.current_expression += expression_change * 0.1  # Time step
            
            # Clip to valid range
            profile.current_expression = np.clip(profile.current_expression, 0.0, 1.0)
            profile.last_updated = self.current_time
        
        self.current_time += 0.1
    
    def set_environmental_signal(self, signal_name: str, strength: float):
        """Set environmental signal that affects gene expression"""
        self.environmental_signals[signal_name] = strength
    
    def set_stress_level(self, stress: float):
        """Set cellular stress level"""
        self.stress_level = np.clip(stress, 0.0, 1.0)
        
        # Stress affects expression of stress response genes
        if stress > 0.5:
            for gene in ['mitochondria_efficiency', 'ribosome_activity']:
                if gene in self.gene_profiles:
                    self.gene_profiles[gene].current_expression *= (1.0 + stress * 0.2)
    
    def get_expression_state(self) -> Dict[str, Any]:
        """Get current gene expression state"""
        expression_levels = {}
        regulation_states = {}
        
        for gene, profile in self.gene_profiles.items():
            expression_levels[gene] = profile.current_expression
            regulation_states[gene] = {
                'base_expression': profile.base_expression,
                'regulation_factors': profile.regulation_factors,
                'last_updated': profile.last_updated
            }
        
        return {
            'expression_levels': expression_levels,
            'regulation_states': regulation_states,
            'current_lineage': self.differentiation_engine.current_lineage,
            'differentiation_progress': self.differentiation_engine.differentiation_progress,
            'environmental_signals': self.environmental_signals,
            'stress_level': self.stress_level,
            'fpga_status': self.fpga_engine.get_reconfiguration_status()
        }
    
    def simulate_expression_evolution(self, steps: int = 100) -> Dict[str, List[float]]:
        """Simulate gene expression evolution over time"""
        evolution = {gene: [] for gene in self.gene_profiles.keys()}
        
        for step in range(steps):
            self._update_expression_dynamics()
            
            for gene, profile in self.gene_profiles.items():
                evolution[gene].append(profile.current_expression)
            
            # Occasionally introduce environmental changes
            if step % 20 == 0 and np.random.random() < 0.3:
                signal_strength = np.random.uniform(-0.5, 0.5)
                self.set_environmental_signal(f"signal_{step}", signal_strength)
        
        return evolution
