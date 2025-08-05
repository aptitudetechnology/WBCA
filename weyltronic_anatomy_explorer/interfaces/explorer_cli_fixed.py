"""
Fixed Interactive CLI for Weyltronic Explorer
Working implementation with proper syntax
"""

from .explorer_cli_simple import SimpleExplorerCLI, main


# Re-export for compatibility
ExplorerCLI = SimpleExplorerCLI


if __name__ == "__main__":
    main()
