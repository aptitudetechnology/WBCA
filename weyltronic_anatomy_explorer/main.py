#!/usr/bin/env python3
"""
Weyltronic Biological Computing Anatomy Educational Explorer
Main entry point for the educational exploration tool
"""

from interfaces.explorer_cli import WeyltonicExplorerCLI
from utils.config import Config

def main():
    """Main entry point for the Weyltronic Explorer"""
    print("🧬 Weyltronic Biological Computing Anatomy Explorer")
    print("=" * 50)
    
    config = Config()
    explorer = WeyltonicExplorerCLI(config)
    explorer.run()

if __name__ == "__main__":
    main()
