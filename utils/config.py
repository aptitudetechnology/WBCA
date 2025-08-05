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
