import os
import pygame
from settings import *
from collections import defaultdict


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], image_path: str, groups: list[pygame.sprite.Sprite],
                 obstacle_sprites: pygame.sprite.Group, transition_sprites: pygame.sprite.Group,
                 initial_level_code: int):
        super().__init__(groups)
        # player sprite
        self.image = pygame.image.load(image_path).convert_alpha()
        # scale image to match screen size
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)

        # general setup
        self.animations = defaultdict(lambda: [])
        self.import_player_assets()
        # status keeps track of the current action and direction of the player
        self.status = "down"
        self.current_level_code = initial_level_code

        # attacking monitors wheather or not the player is attacking
        # attack mechanics not currently implemented
        self.attacking = False

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 6
        self.frame_index = 0
        self.animation_speed = 0.15

        # collisions
        self.obstacle_sprites = obstacle_sprites
        self.transition_sprites = transition_sprites

    def import_player_assets(self):
        for folder in os.listdir(PLAYER_IMAGES_FILE_PATH):
            folder_path = os.path.join(PLAYER_IMAGES_FILE_PATH, folder)
            for image in os.listdir(folder_path):
                image_path = os.path.join(folder_path, image)
                surf = pygame.image.load(image_path).convert_alpha()
                # scale player image up to fit map size
                surf = pygame.transform.scale(surf, (TILE_SIZE, TILE_SIZE))
                self.animations[folder].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()
        up, down, left, right = keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]

        if up:
            self.direction.y = -1
            self.status = "up"

        elif down:
            self.direction.y = 1
            self.status = "down"

        else:
            self.direction.y = 0

        if right:
            self.direction.x = 1
            self.status = "right"

        elif left:
            self.direction.x = -1
            self.status = "left"

        else:
            self.direction.x = 0

    def get_status(self):
        # idle status
        if all(velocity == 0 for velocity in self.direction) and \
                all(word not in self.status for word in ["idle", "attack"]):
            self.status += "_idle"

    def move(self, speed: float):
        # normalise the direction vector so both diagonal speeds always have a magnitude of 1
        if self.direction.magnitude() != 0: self.direction = self.direction.normalize()

        # check for collision with a TransitionBox object
        self.collision("transition")
        
        # update horizontal velocity
        self.rect.x += self.direction.x * speed

        # check for horizontal collision
        self.collision("horizontal")

        # update vertical velocity
        self.rect.y += self.direction.y * speed

        # check for vertical collision
        self.collision("vertical")

    def collision(self, direction: str):
        if direction == "transition":
            for transition_sprite in self.transition_sprites:
                if transition_sprite.rect.colliderect(self.rect):
                    self.current_level_code = transition_sprite.get_transition_code()
                    # self.rect.center = transition_sprite.get_transition_spawn_point()

        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    # player moving to the right
                    if self.direction.x > 0: self.rect.right = sprite.rect.left

                    # player moving to the left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    # player moving to the down
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top

                    # player moving to the up
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation): self.frame_index = 0

        # change the current player image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.input()
        self.get_status()
        self.animate()
        self.move(self.speed)
