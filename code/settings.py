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

# Enemy parameters
ENEMY_SPEED = 3  # Enemy speed must be > 1 to avoid NPC movement bug
ENEMY_AGGRESSION_RADIUS = 1 * TILE_SIZE  # amount of tiles you want radius to cover

# Image file paths
MAPS_FILE_PATH = os.path.join(ROOT_DIR, "maps")
PLAYER_IMAGES_FILE_PATH = os.path.join(ROOT_DIR, "graphics", "player")
ENEMY_IMAGES_FILE_PATH = os.path.join(ROOT_DIR, "graphics", "enemy")
DATA_FILE_PATH = os.path.join(ROOT_DIR, 'data')
TEST_PLAYER_IMAGE_FILE_PATH = os.path.join(ROOT_DIR, "rawAssets", "man.png")
