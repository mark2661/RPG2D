import os
from definitions import ROOT_DIR

# Screen/Tile dimensions
ORIGINAL_TILE_SIZE = 16
SCALE = 5
TILE_SIZE = ORIGINAL_TILE_SIZE * SCALE
MAX_SCREEN_WIDTH = 16
MAX_SCREEN_HEIGHT = 12
WIDTH, HEIGHT = TILE_SIZE * MAX_SCREEN_WIDTH, TILE_SIZE * MAX_SCREEN_HEIGHT

# Frame rate
FPS = 60

# Entity parameters
ENTITY_SPEED = 6
DEFAULT_ATTACK_COOLDOWN_TIME = 400  # milliseconds
DEFAULT_HEALTH_POINTS = 100

# Player parameters
PLAYER_ATTACK_COOLDOWN_TIME = 400  # milliseconds
PLAYER_HEALTH_POINTS = 100
PLAYER_ATTACK_DAMAGE = 20

# Enemy parameters
ENEMY_SPEED = 3  # Enemy speed must be > 1 to avoid NPC movement bug
ENEMY_AGGRESSION_RADIUS = 2 * TILE_SIZE  # amount of tiles you want radius to cover
ENEMY_ATTACK_RADIUS_SCALE_FACTOR = 0.75  # Scaling factor to shrink the attack radius to compared to the aggression circle
ENEMY_ATTACK_COOLDOWN_TIME = 1000  # milliseconds
ENEMY_HEALTH_POINTS = 100

# Image file paths
MAPS_FILE_PATH = os.path.join(ROOT_DIR, "maps")
PLAYER_IMAGES_FILE_PATH = os.path.join(ROOT_DIR, "graphics", "player")
ENEMY_IMAGES_FILE_PATH = os.path.join(ROOT_DIR, "graphics", "enemy")
DATA_FILE_PATH = os.path.join(ROOT_DIR, 'data')
TEST_PLAYER_IMAGE_FILE_PATH = os.path.join(ROOT_DIR, "rawAssets", "man.png")
