#!/usr/bin/env python3
"""Main entry point for Japan City Builder."""

import sys
import logging
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.config import Config
from utils.logger import setup_logger


def main():
    """Main application entry point."""
    # Setup logging
    setup_logger()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Japan City Builder...")
    
    # Load configuration
    config = Config.from_file()
    logger.info(f"Configuration loaded: {config}")
    
    # TODO: Initialize game
    # from game.game import Game
    # game = Game(config)
    # game.run()
    
    logger.info("Game initialization complete.")
    print("Hello! Japan City Builder is starting...")
    print("This is a placeholder. Full implementation coming soon!")


if __name__ == "__main__":
    main()
