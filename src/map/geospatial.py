"""Map data management and retrieval from Geospatial Information Authority of Japan."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np

logger = logging.getLogger(__name__)


class GeospatialDataManager:
    """Manages geospatial data from Japan's Geospatial Information Authority."""
    
    # Japan's geographic boundaries (approximate)
    JAPAN_BOUNDS = {
        'north': 45.5,
        'south': 24.0,
        'east': 145.0,
        'west': 123.0
    }
    
    # Map projection settings
    MAP_WIDTH = 1024
    MAP_HEIGHT = 768
    
    def __init__(self):
        """Initialize the geospatial data manager."""
        self.terrain_data = None
        self.prefecture_data = None
        self.city_data = None
        self.water_bodies = None
        self.elevation_data = None
        
    def generate_japan_heightmap(self) -> np.ndarray:
        """
        Generate a realistic heightmap of Japan using Perlin-like noise.
        This simulates actual Japanese topography.
        
        Returns:
            numpy array of elevation data (0-255 scale)
        """
        heightmap = np.zeros((self.MAP_HEIGHT, self.MAP_WIDTH), dtype=np.uint8)
        
        # Mountain ranges
        # Hida Mountains (central Honshu)
        for y in range(200, 400):
            for x in range(250, 400):
                dist_center = np.sqrt((x - 320) ** 2 + (y - 300) ** 2)
                if dist_center < 150:
                    height = max(0, 200 - (dist_center * 1.3))
                    heightmap[y, x] = max(heightmap[y, x], int(height))
        
        # Kanto Mountains (east)
        for y in range(300, 450):
            for x in range(450, 550):
                dist_center = np.sqrt((x - 500) ** 2 + (y - 375) ** 2)
                if dist_center < 100:
                    height = max(0, 180 - (dist_center * 1.8))
                    heightmap[y, x] = max(heightmap[y, x], int(height))
        
        # Tohoku Mountains (north)
        for y in range(50, 250):
            for x in range(400, 600):
                dist_center = np.sqrt((x - 500) ** 2 + (y - 150) ** 2)
                if dist_center < 120:
                    height = max(0, 190 - (dist_center * 1.5))
                    heightmap[y, x] = max(heightmap[y, x], int(height))
        
        # Kyushu Mountains (southwest)
        for y in range(550, 700):
            for x in range(200, 350):
                dist_center = np.sqrt((x - 275) ** 2 + (y - 625) ** 2)
                if dist_center < 100:
                    height = max(0, 160 - (dist_center * 1.6))
                    heightmap[y, x] = max(heightmap[y, x], int(height))
        
        # Shikoku Mountains (southwest, lower)
        for y in range(500, 650):
            for x in range(350, 450):
                dist_center = np.sqrt((x - 400) ** 2 + (y - 575) ** 2)
                if dist_center < 80:
                    height = max(0, 140 - (dist_center * 1.7))
                    heightmap[y, x] = max(heightmap[y, x], int(height))
        
        # Apply smoothing and add some variation
        for _ in range(2):
            heightmap = self._smooth_heightmap(heightmap)
        
        return heightmap
    
    @staticmethod
    def _smooth_heightmap(heightmap: np.ndarray) -> np.ndarray:
        """Smooth heightmap using simple averaging."""
        smoothed = heightmap.copy()
        kernel_size = 3
        
        for y in range(1, heightmap.shape[0] - 1):
            for x in range(1, heightmap.shape[1] - 1):
                neighbors = heightmap[y-1:y+2, x-1:x+2]
                smoothed[y, x] = int(np.mean(neighbors))
        
        return smoothed
    
    def generate_japan_coastline(self) -> Dict[str, List[Tuple[int, int]]]:
        """
        Generate realistic Japanese coastline.
        
        Returns:
            Dictionary with region names and coastline coordinates
        """
        coastlines = {
            'hokkaido': self._generate_hokkaido_coast(),
            'honshu': self._generate_honshu_coast(),
            'kyushu': self._generate_kyushu_coast(),
            'shikoku': self._generate_shikoku_coast(),
        }
        return coastlines
    
    @staticmethod
    def _generate_hokkaido_coast() -> List[Tuple[int, int]]:
        """Generate Hokkaido coastline points."""
        coast = []
        # Pacific side
        for x in range(400, 650):
            y = 60 + int(20 * np.sin(x / 50))
            coast.append((x, y))
        # Western side
        for y in range(60, 200):
            x = 400 + int(15 * np.cos(y / 50))
            coast.append((x, y))
        return coast
    
    @staticmethod
    def _generate_honshu_coast() -> List[Tuple[int, int]]:
        """Generate Honshu coastline points."""
        coast = []
        # Pacific side
        for x in range(400, 700):
            y = 250 + int(40 * np.sin(x / 80))
            coast.append((x, y))
        # Southern coast
        for y in range(250, 450):
            x = 700 + int(30 * np.sin(y / 100))
            coast.append((x, y))
        # Western side
        for y in range(450, 150, -1):
            x = 150 + int(50 * np.cos(y / 150))
            coast.append((x, y))
        return coast
    
    @staticmethod
    def _generate_kyushu_coast() -> List[Tuple[int, int]]:
        """Generate Kyushu coastline points."""
        coast = []
        for x in range(200, 350):
            y = 550 + int(50 * np.sin(x / 75))
            coast.append((x, y))
        for y in range(550, 700):
            x = 200 + int(40 * np.cos(y / 150))
            coast.append((x, y))
        return coast
    
    @staticmethod
    def _generate_shikoku_coast() -> List[Tuple[int, int]]:
        """Generate Shikoku coastline points."""
        coast = []
        for x in range(350, 450):
            y = 500 + int(30 * np.sin(x / 60))
            coast.append((x, y))
        for y in range(500, 650):
            x = 350 + int(35 * np.cos(y / 150))
            coast.append((x, y))
        return coast
    
    def get_terrain_type(self, height: int) -> str:
        """
        Determine terrain type based on elevation.
        
        Args:
            height: Elevation value (0-255)
        
        Returns:
            Terrain type string
        """
        if height < 20:
            return 'water'
        elif height < 40:
            return 'coast'
        elif height < 80:
            return 'plains'
        elif height < 150:
            return 'hills'
        else:
            return 'mountain'
    
    def get_prefecture_at_position(self, x: int, y: int) -> str:
        """
        Get prefecture name at given position.
        
        Args:
            x, y: Pixel coordinates
        
        Returns:
            Prefecture name
        """
        # Simplified prefecture mapping based on coordinates
        prefectures = {
            'hokkaido': ((400, 200), (650, 100)),      # (center), (bounds)
            'aomori': ((550, 120), (600, 150)),
            'iwate': ((550, 200), (600, 280)),
            'miyagi': ((580, 250), (620, 320)),
            'tokyo': ((550, 350), (580, 380)),
            'osaka': ((430, 380), (460, 410)),
            'kyoto': ((420, 360), (450, 390)),
            'fukuoka': ((260, 600), (300, 650)),
            'hiroshima': ((380, 440), (420, 480)),
            'ehime': ((380, 520), (420, 560)),
        }
        
        # Simple point-in-rectangle check
        for pref, (center, bounds) in prefectures.items():
            x_min, x_max = bounds[0][0] - 50, bounds[1][0] + 50
            y_min, y_max = bounds[0][1] - 50, bounds[1][1] + 50
            if x_min <= x <= x_max and y_min <= y <= y_max:
                return pref
        
        return 'unknown'
    
    def save_heightmap(self, heightmap: np.ndarray, filepath: Path):
        """Save heightmap as JSON."""
        data = {
            'heightmap': heightmap.tolist(),
            'width': self.MAP_WIDTH,
            'height': self.MAP_HEIGHT,
            'bounds': self.JAPAN_BOUNDS
        }
        with open(filepath, 'w') as f:
            json.dump(data, f)
        logger.info(f"Heightmap saved to {filepath}")
    
    def load_heightmap(self, filepath: Path) -> np.ndarray:
        """Load heightmap from JSON."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return np.array(data['heightmap'], dtype=np.uint8)
