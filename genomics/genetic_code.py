"""
Genetic Programming Language for Weyltronic Biological Computing
Simple instruction set for cellular configuration and dynamic reconfiguration
"""

from typing import Dict, Any, List, Optional, Tuple
import re
import json
from enum import Enum
from dataclasses import dataclass


class InstructionType(Enum):
    """Types of genetic instructions"""
    CONFIGURE = "CONFIGURE"      # Configure organelle parameters
    CONNECT = "CONNECT"          # Establish connections between organelles
    SPECIALIZE = "SPECIALIZE"    # Specialize cell function
    REGULATE = "REGULATE"        # Regulate gene expression levels
    DIVIDE = "DIVIDE"           # Control cell division
    COMMUNICATE = "COMMUNICATE" # Inter-cellular communication
    ADAPT = "ADAPT"             # Adaptive responses
    REPAIR = "REPAIR"           # Self-repair mechanisms


@dataclass
class GeneticInstruction:
    """Individual genetic instruction"""
    instruction_type: InstructionType
    target: str
    parameters: Dict[str, Any]
    conditions: List[str] = None
    priority: int = 1


class GeneticProgram:
    def validate(self) -> bool:
        """Validate this genetic program using GeneticCodeValidator."""
        from .genetic_code import GeneticCodeValidator
        validator = GeneticCodeValidator()
        is_valid, errors = validator.validate_program(self)
        self.validation_errors = errors
        return is_valid
    """Complete genetic program containing multiple instructions"""
    
    def __init__(self, program_name: str):
        self.program_name = program_name
        self.instructions: List[GeneticInstruction] = []
        self.metadata = {
            'version': '1.0',
            'description': '',
            'author': 'system',
            'created': '',
            'cell_types': []
        }
        self.validation_errors = []
    
    def add_instruction(self, instruction: GeneticInstruction):
        """Add an instruction to the program"""
        self.instructions.append(instruction)
    
    def get_instructions_by_type(self, instruction_type: InstructionType) -> List[GeneticInstruction]:
        """Get all instructions of a specific type"""
        return [inst for inst in self.instructions if inst.instruction_type == instruction_type]
    
    def get_instructions_for_target(self, target: str) -> List[GeneticInstruction]:
        """Get all instructions targeting a specific organelle"""
        return [inst for inst in self.instructions if inst.target == target]


class GeneticCodeParser:
    """Parser for genetic programming language"""
    
    def __init__(self):
        self.valid_organelles = {
            'nucleus', 'ribosome', 'mitochondria', 'chloroplast', 
            'vacuole', 'cytoplasm', 'er', 'golgi', 'cell_wall'
        }
        self.valid_parameters = {
            'efficiency', 'capacity', 'processing_power', 'light_sensitivity',
            'permeability', 'strength', 'energy_production', 'routing_efficiency'
        }
        
    def parse_program(self, program_text: str) -> GeneticProgram:
        """Parse genetic program from text format"""
        lines = [line.strip() for line in program_text.split('\n') if line.strip()]
        
        program = GeneticProgram("parsed_program")
        current_instruction = None
        
        for line_num, line in enumerate(lines, 1):
            try:
                if line.startswith('#') or line.startswith('//'):
                    # Comment line
                    continue
                elif line.startswith('PROGRAM'):
                    # Program metadata
                    self._parse_program_header(line, program)
                elif line.startswith(tuple(t.value for t in InstructionType)):
                    # New instruction
                    if current_instruction:
                        program.add_instruction(current_instruction)
                    current_instruction = self._parse_instruction_line(line)
                elif current_instruction and ('=' in line or line.startswith('  ')):
                    # Parameter line for current instruction
                    self._parse_parameter_line(line, current_instruction)
                elif line.startswith('END'):
                    # End of program
                    if current_instruction:
                        program.add_instruction(current_instruction)
                    break
                    
            except Exception as e:
                program.validation_errors.append(f"Line {line_num}: {str(e)}")
        
        # Add final instruction if exists
        if current_instruction:
            program.add_instruction(current_instruction)
            
        return program
    
    def _parse_program_header(self, line: str, program: GeneticProgram):
        """Parse program header line"""
        # PROGRAM name "description"
        parts = line.split('"')
        if len(parts) >= 2:
            program.metadata['description'] = parts[1]
        
        name_part = parts[0].replace('PROGRAM', '').strip()
        if name_part:
            program.program_name = name_part
    
    def _parse_instruction_line(self, line: str) -> GeneticInstruction:
        """Parse a single instruction line"""
        # Format: INSTRUCTION_TYPE target [conditions]
        parts = line.split()
        if len(parts) < 2:
            raise ValueError(f"Invalid instruction format: {line}")
        
        instruction_type = InstructionType(parts[0])
        target = parts[1]
        
        # Parse conditions if present
        conditions = []
        if len(parts) > 2:
            condition_text = ' '.join(parts[2:])
            if condition_text.startswith('[') and condition_text.endswith(']'):
                conditions = [c.strip() for c in condition_text[1:-1].split(',')]
        
        return GeneticInstruction(
            instruction_type=instruction_type,
            target=target,
            parameters={},
            conditions=conditions
        )
    
    def _parse_parameter_line(self, line: str, instruction: GeneticInstruction):
        """Parse parameter line and add to instruction"""
        line = line.strip()
        
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            # Parse value type
            parsed_value = self._parse_value(value)
            instruction.parameters[key] = parsed_value
    
    def _parse_value(self, value_str: str) -> Any:
        """Parse value string to appropriate type"""
        value_str = value_str.strip()
        
        # Try to parse as number
        try:
            if '.' in value_str:
                return float(value_str)
            else:
                return int(value_str)
        except ValueError:
            pass
        
        # Try to parse as boolean
        if value_str.lower() in ('true', 'false'):
            return value_str.lower() == 'true'
        
        # Try to parse as list
        if value_str.startswith('[') and value_str.endswith(']'):
            items = [self._parse_value(item.strip()) for item in value_str[1:-1].split(',')]
            return items
        
        # Return as string (remove quotes if present)
        if value_str.startswith('"') and value_str.endswith('"'):
            return value_str[1:-1]
        
        return value_str
    
    def parse_json_program(self, json_text: str) -> GeneticProgram:
        """Parse genetic program from JSON format"""
        try:
            data = json.loads(json_text)
            program = GeneticProgram(data.get('name', 'json_program'))
            program.metadata.update(data.get('metadata', {}))
            
            for inst_data in data.get('instructions', []):
                instruction = GeneticInstruction(
                    instruction_type=InstructionType(inst_data['type']),
                    target=inst_data['target'],
                    parameters=inst_data.get('parameters', {}),
                    conditions=inst_data.get('conditions', []),
                    priority=inst_data.get('priority', 1)
                )
                program.add_instruction(instruction)
                
            return program
            
        except Exception as e:
            program = GeneticProgram("error_program")
            program.validation_errors.append(f"JSON parsing error: {str(e)}")
            return program


class GeneticCodeValidator:
    """Validates genetic programs for correctness and safety"""
    
    def __init__(self):
        self.max_instructions = 1000
        self.max_parameter_value = 10.0
        self.min_parameter_value = 0.0
        
    def validate_program(self, program: GeneticProgram) -> Tuple[bool, List[str]]:
        """Validate entire genetic program"""
        errors = []
        
        # Check program size
        if len(program.instructions) > self.max_instructions:
            errors.append(f"Program too large: {len(program.instructions)} > {self.max_instructions}")
        
        # Validate each instruction
        for i, instruction in enumerate(program.instructions):
            inst_errors = self._validate_instruction(instruction)
            for error in inst_errors:
                errors.append(f"Instruction {i+1}: {error}")
        
        # Check for conflicts
        conflict_errors = self._check_conflicts(program)
        errors.extend(conflict_errors)
        
        return len(errors) == 0, errors
    
    def _validate_instruction(self, instruction: GeneticInstruction) -> List[str]:
        """Validate a single instruction"""
        errors = []
        
        # Validate target
        valid_targets = {
            'nucleus', 'ribosome', 'mitochondria', 'chloroplast',
            'vacuole', 'cytoplasm', 'er', 'golgi', 'cell_wall', 'cell'
        }
        
        if instruction.target not in valid_targets:
            errors.append(f"Invalid target: {instruction.target}")
        
        # Validate parameters based on instruction type
        if instruction.instruction_type == InstructionType.CONFIGURE:
            errors.extend(self._validate_configure_parameters(instruction))
        elif instruction.instruction_type == InstructionType.CONNECT:
            errors.extend(self._validate_connect_parameters(instruction))
        elif instruction.instruction_type == InstructionType.SPECIALIZE:
            errors.extend(self._validate_specialize_parameters(instruction))
        
        # Validate parameter values
        for key, value in instruction.parameters.items():
            if isinstance(value, (int, float)):
                if value < self.min_parameter_value or value > self.max_parameter_value:
                    errors.append(f"Parameter {key} out of range: {value}")
        
        return errors
    
    def _validate_configure_parameters(self, instruction: GeneticInstruction) -> List[str]:
        """Validate CONFIGURE instruction parameters"""
        errors = []
        
        organelle_params = {
            'mitochondria': ['efficiency', 'energy_production'],
            'chloroplast': ['processing_power', 'light_sensitivity'],
            'vacuole': ['capacity'],
            'cytoplasm': ['routing_efficiency'],
            'cell_wall': ['permeability']
        }
        
        expected_params = organelle_params.get(instruction.target, [])
        
        for param in instruction.parameters:
            if expected_params and param not in expected_params:
                errors.append(f"Invalid parameter {param} for {instruction.target}")
        
        return errors
    
    def _validate_connect_parameters(self, instruction: GeneticInstruction) -> List[str]:
        """Validate CONNECT instruction parameters"""
        errors = []
        
        required_params = ['source', 'destination']
        for param in required_params:
            if param not in instruction.parameters:
                errors.append(f"Missing required parameter: {param}")
        
        return errors
    
    def _validate_specialize_parameters(self, instruction: GeneticInstruction) -> List[str]:
        """Validate SPECIALIZE instruction parameters"""
        errors = []
        
        valid_specializations = ['compute', 'memory', 'transport', 'sensory']
        specialization = instruction.parameters.get('type')
        
        if specialization and specialization not in valid_specializations:
            errors.append(f"Invalid specialization type: {specialization}")
        
        return errors
    
    def _check_conflicts(self, program: GeneticProgram) -> List[str]:
        """Check for conflicting instructions"""
        errors = []
        
        # Check for multiple SPECIALIZE instructions (should be only one)
        specialize_instructions = program.get_instructions_by_type(InstructionType.SPECIALIZE)
        if len(specialize_instructions) > 1:
            errors.append("Multiple SPECIALIZE instructions found")
        
        # Check for conflicting parameter values
        config_instructions = program.get_instructions_by_type(InstructionType.CONFIGURE)
        target_params = {}
        
        for instruction in config_instructions:
            target = instruction.target
            if target not in target_params:
                target_params[target] = {}
            
            for param, value in instruction.parameters.items():
                if param in target_params[target]:
                    if target_params[target][param] != value:
                        errors.append(f"Conflicting values for {target}.{param}")
                else:
                    target_params[target][param] = value
        
        return errors


class GeneticCodeOptimizer:
    """Optimizes genetic programs for efficiency and performance"""
    
    def optimize_program(self, program: GeneticProgram) -> GeneticProgram:
        """Optimize genetic program"""
        optimized = GeneticProgram(f"{program.program_name}_optimized")
        optimized.metadata = program.metadata.copy()
        
        # Sort instructions by priority and type
        sorted_instructions = sorted(
            program.instructions, 
            key=lambda x: (x.priority, x.instruction_type.value)
        )
        
        # Remove duplicate instructions
        seen_instructions = set()
        for instruction in sorted_instructions:
            # Create a hash of the instruction for deduplication
            inst_hash = (
                instruction.instruction_type,
                instruction.target,
                frozenset(instruction.parameters.items()) if instruction.parameters else frozenset(),
                tuple(instruction.conditions) if instruction.conditions else tuple()
            )
            
            if inst_hash not in seen_instructions:
                optimized.add_instruction(instruction)
                seen_instructions.add(inst_hash)
        
        # Merge compatible instructions
        optimized = self._merge_compatible_instructions(optimized)
        
        return optimized
    
    def _merge_compatible_instructions(self, program: GeneticProgram) -> GeneticProgram:
        """Merge compatible CONFIGURE instructions for the same target"""
        merged_program = GeneticProgram(program.program_name)
        merged_program.metadata = program.metadata.copy()
        
        # Group CONFIGURE instructions by target
        config_groups = {}
        other_instructions = []
        
        for instruction in program.instructions:
            if instruction.instruction_type == InstructionType.CONFIGURE:
                target = instruction.target
                if target not in config_groups:
                    config_groups[target] = []
                config_groups[target].append(instruction)
            else:
                other_instructions.append(instruction)
        
        # Merge CONFIGURE instructions for each target
        for target, instructions in config_groups.items():
            merged_params = {}
            merged_conditions = []
            max_priority = 1
            
            for instruction in instructions:
                merged_params.update(instruction.parameters)
                if instruction.conditions:
                    merged_conditions.extend(instruction.conditions)
                max_priority = max(max_priority, instruction.priority)
            
            # Remove duplicate conditions
            merged_conditions = list(set(merged_conditions))
            
            merged_instruction = GeneticInstruction(
                instruction_type=InstructionType.CONFIGURE,
                target=target,
                parameters=merged_params,
                conditions=merged_conditions,
                priority=max_priority
            )
            
            merged_program.add_instruction(merged_instruction)
        
        # Add other instructions
        for instruction in other_instructions:
            merged_program.add_instruction(instruction)
        
        return merged_program


def create_sample_programs() -> Dict[str, GeneticProgram]:
    """Create sample genetic programs for different cell types"""
    programs = {}
    
    # Compute cell program
    compute_program = GeneticProgram("compute_cell")
    compute_program.metadata['description'] = "High-performance computational cell"
    
    compute_program.add_instruction(GeneticInstruction(
        InstructionType.SPECIALIZE,
        "cell",
        {"type": "compute"}
    ))
    
    compute_program.add_instruction(GeneticInstruction(
        InstructionType.CONFIGURE,
        "chloroplast",
        {"processing_power": 8.0, "light_sensitivity": 1.5}
    ))
    
    compute_program.add_instruction(GeneticInstruction(
        InstructionType.CONFIGURE,
        "mitochondria",
        {"efficiency": 1.2, "energy_production": 15.0}
    ))
    
    compute_program.add_instruction(GeneticInstruction(
        InstructionType.CONNECT,
        "cytoplasm",
        {"source": "chloroplast", "destination": "vacuole"}
    ))
    
    programs["compute_cell"] = compute_program
    
    # Memory cell program
    memory_program = GeneticProgram("memory_cell")
    memory_program.metadata['description'] = "High-capacity storage cell"
    
    memory_program.add_instruction(GeneticInstruction(
        InstructionType.SPECIALIZE,
        "cell",
        {"type": "memory"}
    ))
    
    memory_program.add_instruction(GeneticInstruction(
        InstructionType.CONFIGURE,
        "vacuole",
        {"capacity": 500.0}
    ))
    
    memory_program.add_instruction(GeneticInstruction(
        InstructionType.CONFIGURE,
        "er",
        {"pipeline_stages": 6}
    ))
    
    programs["memory_cell"] = memory_program
    
    # Transport cell program
    transport_program = GeneticProgram("transport_cell")
    transport_program.metadata['description'] = "Efficient transport and routing cell"
    
    transport_program.add_instruction(GeneticInstruction(
        InstructionType.SPECIALIZE,
        "cell",
        {"type": "transport"}
    ))
    
    transport_program.add_instruction(GeneticInstruction(
        InstructionType.CONFIGURE,
        "cytoplasm",
        {"routing_efficiency": 2.0}
    ))
    
    transport_program.add_instruction(GeneticInstruction(
        InstructionType.CONFIGURE,
        "cell_wall",
        {"permeability": 0.9}
    ))
    
    programs["transport_cell"] = transport_program
    
    return programs
