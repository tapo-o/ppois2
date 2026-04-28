import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed, damage, sprite):
        super().__init__()
        self.image = pygame.transform.rotate(sprite, -math.degrees(angle))
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * speed
        self.damage = damage

    def update(self):
        self.rect.centerx += self.vel.x
        self.rect.centery += self.vel.y
        # Удалять пулю за границами экрана

class Weapon:
    def __init__(self, name, cooldown):
        self.name = name
        self.last_shot = 0
        self.cooldown = cooldown

    def can_use(self):
        return pygame.time.get_ticks() - self.last_shot > self.cooldown

class MeleeWeapon(Weapon):
    def attack(self, pos, direction):
        self.last_shot = pygame.time.get_ticks()
        # Возвращаем "зону поражения" меча
        return pygame.Rect(pos[0], pos[1], 100, 100) 

class RangedWeapon(Weapon):
    def shoot(self, pos, angle, bullet_sprite):
        self.last_shot = pygame.time.get_ticks()
        return Bullet(pos[0], pos[1], angle, 10, 20, bullet_sprite)