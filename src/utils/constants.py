"""Game constants and global settings."""

# Window size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_FPS = 60

# Map settings
MAP_WIDTH = 100
MAP_HEIGHT = 100
TILE_SIZE = 32  # pixels

# Game economy
INITIAL_BUDGET = 10000
MONTH_DURATION = 30  # real-time seconds per game month

# Tile terrain types
TERRAIN_GRASS = 0
TERRAIN_MOUNTAIN = 1
TERRAIN_WATER = 2
TERRAIN_COAST = 3
TERRAIN_URBAN = 4

# Building categories
CAT_RESIDENTIAL = "residential"
CAT_COMMERCIAL = "commercial"
CAT_INDUSTRIAL = "industrial"
CAT_INFRASTRUCTURE = "infrastructure"
CAT_PUBLIC = "public"
CAT_TOURISM = "tourism"

# Game speeds
GAME_SPEED_PAUSED = 0
GAME_SPEED_NORMAL = 1
GAME_SPEED_FAST = 2
GAME_SPEED_VERY_FAST = 4

# Colors (RGB)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GRAY = (128, 128, 128)

# Difficulty levels
DIFFICULTY_EASY = "easy"
DIFFICULTY_NORMAL = "normal"
DIFFICULTY_HARD = "hard"
DIFFICULTY_SURVIVAL = "survival"
