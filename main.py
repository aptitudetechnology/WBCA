#!/usr/bin/env python3
"""
Weyltronic Biological Computing Anatomy Educational Explorer
Main entry point for the educational exploration tool
"""

from interfaces.explorer_cli_simple import SimpleExplorerCLI


def main():
    """Main entry point for the Weyltronic Explorer"""
    print("🧬 Weyltronic Biological Computing Anatomy Explorer")
    print("=" * 50)
    
    # Create and run the explorer CLI
    explorer = SimpleExplorerCLI()
    explorer.run()


if __name__ == "__main__":
    main()
