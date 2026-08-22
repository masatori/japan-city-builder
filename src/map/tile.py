"""Tile class representing individual map cells."""

import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class Tile:
    """Represents a single tile on the game map."""
    
    TERRAIN_TYPES = {
        'water': 0,
        'coast': 1,
        'plains': 2,
        'hills': 3,
        'mountain': 4,
    }
    
    def __init__(self, x: int, y: int, terrain_type: str, elevation: int = 0):
        """Initialize a tile.
        
        Args:
            x: X coordinate
            y: Y coordinate
            terrain_type: Type of terrain
            elevation: Elevation value (0-255)
        """
        self.x = x
        self.y = y
        self.terrain_type = terrain_type
        self.elevation = elevation
        
        # Building state
        self.building = None
        self.building_id = None
        
        # Economic data
        self.population = 0
        self.employment = 0
        self.happiness = 100
        self.pollution = 0
        self.crime_rate = 0
        
        # Infrastructure
        self.power = 0  # Power level (0-100)
        self.water = 0  # Water level (0-100)
        self.sewage = 0  # Sewage treatment (0-100)
        
        # Development
        self.development_level = 0  # 0-3
        self.is_developed = False
        self.zoning = None  # 'residential', 'commercial', 'industrial', None
        
        # Properties for night/day cycle
        self.is_illuminated = False
        self.light_level = 0  # 0-255 for night rendering
        
    def can_build(self) -> bool:
        """Check if building is possible on this tile.
        
        Returns:
            True if building is allowed
        """
        if self.terrain_type in ['water']:
            return False
        if self.building is not None:
            return False
        return True
    
    def place_building(self, building_id: str) -> bool:
        """Place a building on this tile.
        
        Args:
            building_id: ID of the building to place
        
        Returns:
            True if placement successful
        """
        if not self.can_build():
            return False
        
        self.building_id = building_id
        self.is_developed = True
        return True
    
    def remove_building(self):
        """Remove building from this tile."""
        self.building = None
        self.building_id = None
        self.is_developed = False
    
    def update(self, delta_time: float):
        """Update tile state each frame.
        
        Args:
            delta_time: Time since last update in seconds
        """
        # Decay happiness slightly
        if self.happiness > 0:
            self.happiness = max(0, self.happiness - 0.1)
        
        # Accumulate pollution
        if self.building_id:
            self.pollution = min(100, self.pollution + 0.05)
        else:
            self.pollution = max(0, self.pollution - 0.1)
    
    def get_color_for_terrain(self, is_night: bool = False) -> tuple:
        """Get RGB color for this tile based on terrain and time of day.
        
        Args:
            is_night: Whether it's nighttime
        
        Returns:
            RGB color tuple
        """
        colors = {
            'water': (41, 128, 185) if not is_night else (20, 40, 80),
            'coast': (149, 165, 166) if not is_night else (60, 70, 90),
            'plains': (46, 204, 113) if not is_night else (30, 80, 50),
            'hills': (155, 89, 182) if not is_night else (80, 40, 100),
            'mountain': (127, 140, 141) if not is_night else (70, 70, 80),
        }
        return colors.get(self.terrain_type, (200, 200, 200))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert tile to dictionary for serialization.
        
        Returns:
            Dictionary representation of tile
        """
        return {
            'x': self.x,
            'y': self.y,
            'terrain_type': self.terrain_type,
            'elevation': self.elevation,
            'building_id': self.building_id,
            'population': self.population,
            'happiness': self.happiness,
            'pollution': self.pollution,
            'zoning': self.zoning,
        }
    
    def __repr__(self) -> str:
        return f"Tile({self.x}, {self.y}, {self.terrain_type}, elev={self.elevation})"
