"""Generate custom icons and sprites for the game."""

import logging
from typing import Tuple
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)


class IconGenerator:
    """Generates custom game icons and sprites."""
    
    # Color palette - modern, minimal design
    COLORS = {
        'primary_dark': (30, 35, 45),
        'primary_light': (45, 50, 65),
        'accent_blue': (66, 153, 225),
        'accent_green': (39, 174, 96),
        'accent_orange': (230, 126, 34),
        'accent_red': (231, 76, 60),
        'text_light': (236, 240, 241),
        'text_dark': (44, 62, 80),
        'border': (149, 165, 166),
    }
    
    def __init__(self, icon_size: int = 32):
        """Initialize icon generator.
        
        Args:
            icon_size: Size of generated icons in pixels
        """
        self.icon_size = icon_size
    
    def generate_building_icon(self, building_type: str) -> np.ndarray:
        """Generate icon for building type.
        
        Args:
            building_type: Type of building (residential, commercial, etc.)
        
        Returns:
            RGB numpy array for icon
        """
        icon = np.ones((self.icon_size, self.icon_size, 3), dtype=np.uint8) * 240
        
        if building_type == 'residential':
            return self._draw_residential_icon(icon)
        elif building_type == 'commercial':
            return self._draw_commercial_icon(icon)
        elif building_type == 'industrial':
            return self._draw_industrial_icon(icon)
        elif building_type == 'station':
            return self._draw_station_icon(icon)
        elif building_type == 'airport':
            return self._draw_airport_icon(icon)
        elif building_type == 'hospital':
            return self._draw_hospital_icon(icon)
        elif building_type == 'school':
            return self._draw_school_icon(icon)
        elif building_type == 'park':
            return self._draw_park_icon(icon)
        
        return icon
    
    def _draw_residential_icon(self, icon: np.ndarray) -> np.ndarray:
        """Draw residential building icon."""
        # Draw house shape - simple rectangular building
        color = self.COLORS['accent_green']
        h, w = self.icon_size, self.icon_size
        
        # Main building
        icon[8:24, 8:24] = color
        
        # Windows
        window_color = self.COLORS['accent_blue']
        icon[10:12, 10:12] = window_color
        icon[10:12, 14:16] = window_color
        icon[16:18, 10:12] = window_color
        icon[16:18, 14:16] = window_color
        
        # Door
        door_color = self.COLORS['text_dark']
        icon[18:23, 14:16] = door_color
        
        return icon
    
    def _draw_commercial_icon(self, icon: np.ndarray) -> np.ndarray:
        """Draw commercial building icon."""
        color = self.COLORS['accent_orange']
        h, w = self.icon_size, self.icon_size
        
        # Tall building
        icon[6:24, 10:22] = color
        
        # Windows grid
        window_color = self.COLORS['text_light']
        for row in range(3):
            for col in range(2):
                y = 8 + row * 5
                x = 12 + col * 5
                icon[y:y+2, x:x+2] = window_color
        
        return icon
    
    def _draw_industrial_icon(self, icon: np.ndarray) -> np.ndarray:
        """Draw industrial building icon."""
        color = self.COLORS['text_dark']
        h, w = self.icon_size, self.icon_size
        
        # Factory shape
        icon[10:22, 8:24] = color
        
        # Smokestacks
        stack_color = self.COLORS['text_dark']
        icon[4:10, 10:12] = stack_color
        icon[4:10, 20:22] = stack_color
        
        return icon
    
    def _draw_station_icon(self, icon: np.ndarray) -> np.ndarray:
        """Draw train station icon."""
        color = self.COLORS['accent_red']
        h, w = self.icon_size, self.icon_size
        
        # Station building
        icon[10:20, 8:24] = color
        
        # Platform
        platform_color = self.COLORS['text_dark']
        icon[20:22, 6:26] = platform_color
        
        # Tracks
        icon[23:24, 6:26] = (0, 0, 0)
        icon[25:26, 6:26] = (0, 0, 0)
        
        return icon
    
    def _draw_airport_icon(self, icon: np.ndarray) -> np.ndarray:
        """Draw airport icon."""
        color = self.COLORS['accent_blue']
        h, w = self.icon_size, self.icon_size
        
        # Terminal building
        icon[12:20, 10:22] = color
        
        # Runway
        runway_color = self.COLORS['text_dark']
        icon[8:10, 6:26] = runway_color
        
        return icon
    
    def _draw_hospital_icon(self, icon: np.ndarray) -> np.ndarray:
        """Draw hospital icon."""
        color = self.COLORS['accent_red']
        h, w = self.icon_size, self.icon_size
        
        # Building
        icon[8:24, 12:20] = color
        
        # Red cross symbol
        cross_color = self.COLORS['text_light']
        icon[14:18, 15:17] = cross_color  # Vertical line
        icon[15:17, 14:18] = cross_color  # Horizontal line
        
        return icon
    
    def _draw_school_icon(self, icon: np.ndarray) -> np.ndarray:
        """Draw school icon."""
        color = self.COLORS['accent_green']
        h, w = self.icon_size, self.icon_size
        
        # Building
        icon[10:22, 10:22] = color
        
        # Flag on top (for school)
        flag_color = self.COLORS['accent_red']
        icon[8:10, 15:20] = flag_color
        
        return icon
    
    def _draw_park_icon(self, icon: np.ndarray) -> np.ndarray:
        """Draw park icon."""
        # Green background
        icon[:] = self.COLORS['accent_green']
        
        # Tree shapes (simple)
        tree_color = self.COLORS['text_dark']
        # Tree 1
        icon[8:16, 10:14] = tree_color
        # Tree 2
        icon[12:20, 18:22] = tree_color
        
        return icon
    
    def generate_terrain_texture(self, terrain_type: str, is_night: bool = False) -> np.ndarray:
        """Generate texture for terrain tile.
        
        Args:
            terrain_type: Type of terrain
            is_night: Whether it's night time
        
        Returns:
            RGB numpy array for texture
        """
        size = self.icon_size
        texture = np.zeros((size, size, 3), dtype=np.uint8)
        
        terrain_colors = {
            'water': (41, 128, 185) if not is_night else (20, 40, 80),
            'coast': (149, 165, 166) if not is_night else (60, 70, 90),
            'plains': (46, 204, 113) if not is_night else (30, 80, 50),
            'hills': (155, 89, 182) if not is_night else (80, 40, 100),
            'mountain': (127, 140, 141) if not is_night else (70, 70, 80),
        }
        
        color = terrain_colors.get(terrain_type, (200, 200, 200))
        texture[:] = color
        
        # Add some variation with noise
        noise = np.random.randint(-10, 10, (size, size, 3))
        texture = np.clip(texture + noise, 0, 255).astype(np.uint8)
        
        return texture
