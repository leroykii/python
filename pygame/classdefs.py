import pygame
from pygame.locals import *
import random

INITIAL_PLAYER_VELOCITY = 2
BULLET_VELOCITY = 1
MAX_VELOCITY = 2
MIN_VELOCITY = 1


# Define our player object and call super to give it all the properties
# and methods of pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.points = 0
        self.velocity = INITIAL_PLAYER_VELOCITY

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.velocity)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.velocity)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.velocity, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.velocity, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((30, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(820, random.randint(0, 600)))
        self.speed = random.randint(MIN_VELOCITY, MAX_VELOCITY)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Food(Enemy):
    pass


class VenomousFood(Enemy):
    pass


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super(Boss, self).__init__()
        self.surf = pygame.Surface((100, 100))
        self.surf.fill((198, 96, 194))
        self.rect = self.surf.get_rect(center=(650, random.randint(0, 600)))
        self.hits = 0


class Shoot(pygame.sprite.Sprite):
    def __init__(self, player_position):
        super(Shoot, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((0, 100, 255))
        self.rect = self.surf.get_rect()
        self.rect[0] = player_position[0] + player_position[2]
        self.rect[1] = player_position[1] + player_position[3] / 2
        self.speed = BULLET_VELOCITY

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > 800:
            self.kill()
