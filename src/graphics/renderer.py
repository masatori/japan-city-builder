"""Game renderer using Pygame."""

import logging
from typing import Optional, Tuple
import pygame
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)


class GameRenderer:
    """Handles all game rendering."""
    
    # Color palette
    COLORS = {
        'background': (20, 25, 35),
        'ui_bg': (30, 35, 45),
        'ui_border': (66, 153, 225),
        'text': (236, 240, 241),
        'text_dark': (44, 62, 80),
        'accent': (66, 153, 225),
    }
    
    def __init__(self, width: int = 1280, height: int = 720, tile_size: int = 32):
        """Initialize renderer.
        
        Args:
            width: Window width
            height: Window height
            tile_size: Size of each tile in pixels
        """
        self.width = width
        self.height = height
        self.tile_size = tile_size
        
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Japan City Builder")
        
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_large = pygame.font.Font(None, 48)
        
        # Camera/viewport
        self.camera_x = 0
        self.camera_y = 0
        self.zoom = 1.0
        
        # Time of day (0.0 = midnight, 1.0 = next midnight)
        self.time_of_day = 0.5  # Start at noon
        self.is_night = False
        
        # Tile cache for performance
        self.tile_cache = {}
        
        logger.info(f"Renderer initialized: {width}x{height}")
    
    def clear(self):
        """Clear screen with background color."""
        self.screen.fill(self.COLORS['background'])
    
    def draw_tilemap(self, tilemap):
        """Draw the tilemap.
        
        Args:
            tilemap: Tilemap object to render
        """
        # Calculate visible tile range
        start_x = max(0, int(self.camera_x // self.tile_size))
        start_y = max(0, int(self.camera_y // self.tile_size))
        end_x = min(tilemap.width, start_x + (self.width // self.tile_size) + 2)
        end_y = min(tilemap.height, start_y + (self.height // self.tile_size) + 2)
        
        # Draw tiles
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = tilemap.get_tile(x, y)
                if tile:
                    self.draw_tile(tile, x, y)
    
    def draw_tile(self, tile, grid_x: int, grid_y: int):
        """Draw a single tile.
        
        Args:
            tile: Tile object to draw
            grid_x, grid_y: Grid coordinates
        """
        # Calculate screen position
        screen_x = int(grid_x * self.tile_size - self.camera_x)
        screen_y = int(grid_y * self.tile_size - self.camera_y)
        
        # Skip if off-screen
        if screen_x > self.width or screen_y > self.height:
            return
        if screen_x + self.tile_size < 0 or screen_y + self.tile_size < 0:
            return
        
        # Get terrain color
        color = tile.get_color_for_terrain(self.is_night)
        
        # Adjust color for pollution
        if tile.pollution > 50:
            # Polluted areas get a gray tint
            pollution_factor = (tile.pollution - 50) / 50
            color = (
                int(color[0] * (1 - pollution_factor * 0.3) + 100 * pollution_factor * 0.3),
                int(color[1] * (1 - pollution_factor * 0.3) + 100 * pollution_factor * 0.3),
                int(color[2] * (1 - pollution_factor * 0.3) + 100 * pollution_factor * 0.3),
            )
        
        # Draw tile rectangle
        rect = pygame.Rect(screen_x, screen_y, self.tile_size, self.tile_size)
        pygame.draw.rect(self.screen, color, rect)
        
        # Draw border
        border_color = (100, 100, 100) if not self.is_night else (40, 40, 40)
        pygame.draw.rect(self.screen, border_color, rect, 1)
        
        # Highlight developed tiles at night with light
        if self.is_night and tile.is_developed:
            light_color = (255, 240, 100)
            pygame.draw.circle(
                self.screen,
                light_color,
                (screen_x + self.tile_size // 2, screen_y + self.tile_size // 2),
                self.tile_size // 3,
                width=2
            )
    
    def draw_ui_panel(self, width: int, height: int, x: int, y: int):
        """Draw UI panel with modern design.
        
        Args:
            width, height: Panel dimensions
            x, y: Panel position
        """
        # Panel background
        panel_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, self.COLORS['ui_bg'], panel_rect)
        
        # Panel border
        pygame.draw.rect(self.screen, self.COLORS['ui_border'], panel_rect, 2)
    
    def draw_text(self, text: str, x: int, y: int, size: str = 'medium',
                  color: Tuple[int, int, int] = None, bold: bool = False):
        """Draw text on screen.
        
        Args:
            text: Text to draw
            x, y: Position
            size: Font size ('small', 'medium', 'large')
            color: Text color (RGB)
            bold: Whether text is bold
        """
        if color is None:
            color = self.COLORS['text']
        
        font_map = {'small': self.font_small, 'medium': self.font_medium, 'large': self.font_large}
        font = font_map.get(size, self.font_medium)
        
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))
    
    def draw_hud(self, game_state):
        """Draw heads-up display.
        
        Args:
            game_state: GameState object
        """
        # Left panel - stats
        self.draw_ui_panel(300, self.height, 0, 0)
        
        # Draw stats
        y_offset = 20
        line_height = 30
        
        self.draw_text("City Stats", 20, y_offset, size='large')
        y_offset += line_height * 1.5
        
        self.draw_text(f"Year: {game_state.current_year}", 20, y_offset)
        y_offset += line_height
        
        self.draw_text(f"Population: {game_state.total_population:,}", 20, y_offset)
        y_offset += line_height
        
        self.draw_text(f"Budget: ${game_state.current_balance:,}", 20, y_offset,
                      color=(39, 174, 96) if game_state.current_balance >= 0 else (231, 76, 60))
        y_offset += line_height
        
        # Right panel - time and weather
        self.draw_ui_panel(300, 150, self.width - 300, 0)
        
        # Time display
        hours = int(self.time_of_day * 24)
        minutes = int((self.time_of_day * 24 - hours) * 60)
        time_str = f"{hours:02d}:{minutes:02d}"
        self.draw_text(time_str, self.width - 280, 20, size='large')
        
        # Day/Night indicator
        if self.is_night:
            self.draw_text("Night", self.width - 280, 60, color=(100, 150, 255))
        else:
            self.draw_text("Day", self.width - 280, 60, color=(255, 200, 100))
    
    def update_time_of_day(self, delta_time: float, time_scale: float = 1.0):
        """Update time of day.
        
        Args:
            delta_time: Time elapsed in seconds
            time_scale: Speed of time progression (1.0 = real time)
        """
        # Advance time (1 second = 1 minute in game, scaled by time_scale)
        self.time_of_day += (delta_time / 1440.0) * time_scale  # 1440 seconds = 24 hours
        
        if self.time_of_day >= 1.0:
            self.time_of_day -= 1.0
        
        # Determine if it's night
        self.is_night = self.time_of_day < 0.25 or self.time_of_day > 0.75
    
    def pan_camera(self, dx: int, dy: int):
        """Pan camera.
        
        Args:
            dx, dy: Movement in pixels
        """
        self.camera_x += dx
        self.camera_y += dy
        
        # Clamp camera
        self.camera_x = max(0, self.camera_x)
        self.camera_y = max(0, self.camera_y)
    
    def present(self):
        """Update display."""
        pygame.display.flip()
    
    def get_fps(self) -> float:
        """Get current FPS.
        
        Returns:
            Frames per second
        """
        return self.clock.get_fps()
    
    def tick(self, fps: int = 60) -> float:
        """Tick clock and return delta time.
        
        Args:
            fps: Target frames per second
        
        Returns:
            Delta time in seconds
        """
        return self.clock.tick(fps) / 1000.0
    
    def quit(self):
        """Shutdown renderer."""
        pygame.quit()
        logger.info("Renderer shutdown")
