import os
from definitions import ROOT_DIR


ORIGINAL_TILE_SIZE = 16
SCALE = 5
TILE_SIZE = ORIGINAL_TILE_SIZE * SCALE
MAX_SCREEN_WIDTH = 16
MAX_SCREEN_HEIGHT = 12
WIDTH, HEIGHT = TILE_SIZE * MAX_SCREEN_WIDTH, TILE_SIZE * MAX_SCREEN_HEIGHT

FPS = 60
# FPS = 1
ENTITY_SPEED = 6
MAPS_FILE_PATH = os.path.join(ROOT_DIR, "maps")
PLAYER_IMAGES_FILE_PATH = os.path.join(ROOT_DIR, "graphics", "player")
ENEMY_IMAGES_FILE_PATH = os.path.join(ROOT_DIR, "graphics", "enemy")
DATA_FILE_PATH = os.path.join(ROOT_DIR, 'data')
TEST_PLAYER_IMAGE_FILE_PATH = os.path.join(ROOT_DIR, "rawAssets", "man.png")
