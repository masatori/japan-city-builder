"""Tilemap class representing the entire game map."""

import logging
from typing import List, Dict, Optional, Tuple
import numpy as np
from .tile import Tile
from .geospatial import GeospatialDataManager

logger = logging.getLogger(__name__)


class Tilemap:
    """Represents the entire game map composed of tiles."""
    
    def __init__(self, width: int = 1024, height: int = 768):
        """Initialize tilemap.
        
        Args:
            width: Map width in tiles
            height: Map height in tiles
        """
        self.width = width
        self.height = height
        self.tiles: List[List[Tile]] = []
        self.geospatial = GeospatialDataManager()
        self.heightmap = None
        self.coastlines = None
        
    def generate_japan_map(self):
        """Generate map with Japanese geography."""
        logger.info("Generating Japan map...")
        
        # Generate heightmap
        self.heightmap = self.geospatial.generate_japan_heightmap()
        self.coastlines = self.geospatial.generate_japan_coastline()
        
        # Create tiles based on heightmap
        self.tiles = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Get elevation from heightmap
                elevation = int(self.heightmap[y, x])
                
                # Determine terrain type
                terrain = self.geospatial.get_terrain_type(elevation)
                
                # Create tile
                tile = Tile(x, y, terrain, elevation)
                row.append(tile)
            
            self.tiles.append(row)
        
        logger.info(f"Japan map generated: {self.width}x{self.height} tiles")
    
    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """Get tile at coordinates.
        
        Args:
            x, y: Tile coordinates
        
        Returns:
            Tile object or None if out of bounds
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None
    
    def set_tile(self, x: int, y: int, tile: Tile) -> bool:
        """Set tile at coordinates.
        
        Args:
            x, y: Tile coordinates
            tile: Tile object to set
        
        Returns:
            True if successful
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = tile
            return True
        return False
    
    def get_neighbors(self, x: int, y: int, radius: int = 1) -> List[Tile]:
        """Get neighboring tiles.
        
        Args:
            x, y: Center tile coordinates
            radius: Search radius
        
        Returns:
            List of neighboring tiles
        """
        neighbors = []
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue
                tile = self.get_tile(x + dx, y + dy)
                if tile:
                    neighbors.append(tile)
        return neighbors
    
    def get_tiles_by_terrain(self, terrain_type: str) -> List[Tile]:
        """Get all tiles of a specific terrain type.
        
        Args:
            terrain_type: Terrain type to search for
        
        Returns:
            List of matching tiles
        """
        tiles = []
        for row in self.tiles:
            for tile in row:
                if tile.terrain_type == terrain_type:
                    tiles.append(tile)
        return tiles
    
    def get_tiles_by_building(self, building_id: str) -> List[Tile]:
        """Get all tiles with a specific building.
        
        Args:
            building_id: Building ID to search for
        
        Returns:
            List of tiles with the building
        """
        tiles = []
        for row in self.tiles:
            for tile in row:
                if tile.building_id == building_id:
                    tiles.append(tile)
        return tiles
    
    def can_place_building(self, x: int, y: int, size: int = 1) -> bool:
        """Check if building can be placed at location.
        
        Args:
            x, y: Center coordinates
            size: Size of building (size x size)
        
        Returns:
            True if placement is possible
        """
        half_size = size // 2
        for dy in range(-half_size, half_size + 1):
            for dx in range(-half_size, half_size + 1):
                tile = self.get_tile(x + dx, y + dy)
                if not tile or not tile.can_build():
                    return False
        return True
    
    def place_building(self, x: int, y: int, building_id: str, size: int = 1) -> bool:
        """Place building on map.
        
        Args:
            x, y: Center coordinates
            building_id: Building ID
            size: Size of building
        
        Returns:
            True if placement successful
        """
        if not self.can_place_building(x, y, size):
            return False
        
        half_size = size // 2
        for dy in range(-half_size, half_size + 1):
            for dx in range(-half_size, half_size + 1):
                tile = self.get_tile(x + dx, y + dy)
                if tile:
                    tile.place_building(building_id)
        
        return True
    
    def remove_building(self, x: int, y: int, size: int = 1):
        """Remove building from map.
        
        Args:
            x, y: Center coordinates
            size: Size of building
        """
        half_size = size // 2
        for dy in range(-half_size, half_size + 1):
            for dx in range(-half_size, half_size + 1):
                tile = self.get_tile(x + dx, y + dy)
                if tile:
                    tile.remove_building()
    
    def get_total_population(self) -> int:
        """Get total population on map.
        
        Returns:
            Total population
        """
        total = 0
        for row in self.tiles:
            for tile in row:
                total += tile.population
        return total
    
    def get_average_happiness(self) -> float:
        """Get average happiness across map.
        
        Returns:
            Average happiness (0-100)
        """
        total = 0
        count = 0
        for row in self.tiles:
            for tile in row:
                if tile.is_developed:
                    total += tile.happiness
                    count += 1
        return total / count if count > 0 else 100
    
    def update(self, delta_time: float):
        """Update all tiles.
        
        Args:
            delta_time: Time since last update in seconds
        """
        for row in self.tiles:
            for tile in row:
                tile.update(delta_time)
    
    def to_dict(self) -> Dict:
        """Convert tilemap to dictionary for serialization.
        
        Returns:
            Dictionary representation
        """
        return {
            'width': self.width,
            'height': self.height,
            'tiles': [[tile.to_dict() for tile in row] for row in self.tiles]
        }
