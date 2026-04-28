import pygame
import math
import random
from src.utils import AssetManager, CONFIG, WIDTH, HEIGHT

assets = AssetManager()

class Drop(pygame.sprite.Sprite):
    def __init__(self, x, y, drop_type):
        super().__init__()
        self.type = drop_type # 'medkit', 'ammo_shotgun', 'ammo_sword'
        
        colors = {'medkit': (255, 50, 50), 'ammo_shotgun': (50, 50, 255), 'ammo_sword': (150, 150, 150)}
        self.image = assets.get_image(f"drop_{drop_type}.png", (20, 20), colors.get(drop_type, (255,255,255)))
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = 10
        self.lifetime = 600 

    def update(self):
        self.lifetime -= 1
        if self.lifetime % 30 < 15 and self.lifetime < 120:
            self.image.set_alpha(100) 
        else:
            self.image.set_alpha(255)
            
        if self.lifetime <= 0:
            self.kill()

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed, damage, color=(255, 255, 0), radius=4):
        super().__init__()
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = radius
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
        self.damage = damage

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos
        if not (0 <= self.pos.x <= WIDTH and 0 <= self.pos.y <= HEIGHT):
            self.kill()

class Weapon:
    def __init__(self, name):
        cfg = CONFIG['weapons'][name]
        self.name = name
        self.damage = cfg['damage']
        self.cooldown_max = cfg['cooldown']
        self.cooldown = 0
        self.bullet_speed = cfg.get('speed', 0)
        
        ammo_cfg = cfg.get('max_ammo', 'inf')
        self.max_ammo = float('inf') if ammo_cfg == 'inf' else ammo_cfg
        self.ammo = self.max_ammo

        self.sprite = assets.get_image(f"weapon_{name}.png", (40, 20), (100, 100, 100))

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def shoot(self, x, y, target_pos, bullet_group):
        if self.cooldown <= 0 and (self.max_ammo == float('inf') or self.ammo > 0):
            angle = math.atan2(target_pos[1] - y, target_pos[0] - x)
            self._fire(x, y, angle, bullet_group)
            self.cooldown = self.cooldown_max
            if self.max_ammo != float('inf'):
                self.ammo -= 1
            
            assets.play_sound(f"{self.name}.wav")
            return True
        return False

class Pistol(Weapon):
    def _fire(self, x, y, angle, group):
        group.add(Projectile(x, y, angle, self.bullet_speed, self.damage))

class Shotgun(Weapon):
    def _fire(self, x, y, angle, group):
        for spread in [-0.2, -0.1, 0, 0.1, 0.2]:
            group.add(Projectile(x, y, angle + spread, self.bullet_speed, self.damage))

class SwordSlash(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, damage, sword_range):
        super().__init__()
        self.damage = damage
        size = sword_range * 2
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.arc(self.image, (255, 255, 255), (0, 0, size, size), -angle - 1.2, -angle + 1.2, 15)
        self.rect = self.image.get_rect(center=(x, y))
        self.lifetime = 7

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

class Sword(Weapon):
    def __init__(self, name):
        super().__init__(name)
        self.range = CONFIG['weapons'][name].get('range', 60)

    def _fire(self, x, y, angle, group):
        slash_dist = self.range * 0.8
        slash_x = x + math.cos(angle) * slash_dist
        slash_y = y + math.sin(angle) * slash_dist
        group.add(SwordSlash(slash_x, slash_y, angle, self.damage, self.range))

class LivingEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, hp, speed, color, radius, name_prefix, walk_frames=4, death_frames=4, frame_w=64, frame_h=64):
        super().__init__()
        self.name_prefix = name_prefix
        self.max_hp = hp
        self.hp = hp
        self.speed = speed
        self.radius = radius
        self.base_color = color
        
        self.state = "walk"
        self.angle = 0
        
        sheet_name = f"{name_prefix}_sheet.png"
        
        self.frames = {
            "walk": assets.get_spritesheet_row(sheet_name, frame_w, frame_h, 0, walk_frames, (radius*6, radius*6), color),
            "death": assets.get_spritesheet_row(sheet_name, frame_w, frame_h, 1, death_frames, (radius*6, radius*6), color)
        }
        
        self.frame_index = 0
        self.anim_timer = pygame.time.get_ticks()
        self.anim_delay = 200
        self.hit_timer = 0
        
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.anim_timer > self.anim_delay:
            self.anim_timer = now
            self.frame_index += 1
            
            if self.state == "death":
                if self.frame_index >= len(self.frames["death"]):
                    self.kill()
                    return
            else:
                self.frame_index %= len(self.frames[self.state])
        
        current_frame = self.frames[self.state][self.frame_index % len(self.frames[self.state])]
        base_image = current_frame
        
        if self.hit_timer > 0:
            self.hit_timer -= 1
            base_image = current_frame.copy()
            base_image.fill((150, 150, 150), special_flags=pygame.BLEND_RGB_ADD)

        self.image = pygame.transform.rotate(base_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)

    def take_damage(self, amount):
        if self.state == "death": return False
        
        self.hp -= amount
        self.hit_timer = 5 
        
        if self.hp <= 0:
            self.state = "death"
            self.frame_index = 0
            return True
        return False

class Player(LivingEntity):
    def __init__(self, x, y):
        cfg = CONFIG['player']
        
        fw = cfg.get('frame_w', 472)
        fh = cfg.get('frame_h', 472)
        wf = cfg.get('walk_frames', 46)
        df = cfg.get('death_frames', 20)
        
        super().__init__(x, y, cfg['hp'], cfg['speed'], (0, 100, 255), 15, "player", walk_frames=wf, death_frames=df, frame_w=fw, frame_h=fh)
        
        self.weapons = [Sword('sword'), Pistol('pistol'), Shotgun('shotgun')]
        self.weapon_idx = 0
        self.score = 0

    def update(self):
        self.current_weapon.update()

        if self.state != "death":
            mx, my = pygame.mouse.get_pos()
            self.angle = math.degrees(math.atan2(self.pos.y - my, mx - self.pos.x))

            self.angle -= 90 
            
        self.animate()

    @property
    def current_weapon(self):
        return self.weapons[self.weapon_idx]

    def move(self, dx, dy):
        if self.state == "death": return
        if dx != 0 or dy != 0:
            move_vec = pygame.math.Vector2(dx, dy).normalize() * self.speed
            self.pos += move_vec
            self.rect.center = self.pos

    def shoot(self, x, y, target_pos, bullet_group):
        if self.state == "death": return False
        return self.current_weapon.shoot(x, y, target_pos, bullet_group)

class Enemy(LivingEntity):
    def __init__(self, x, y, type_name):
        cfg = CONFIG['enemies'][type_name]

        fw = cfg.get('frame_w', 472)
        fh = cfg.get('frame_h', 472)
        wf = cfg.get('walk_frames', 4)
        df = cfg.get('death_frames', 4)
        
        super().__init__(x, y, cfg['hp'], cfg['speed'], cfg['color'], cfg['radius'], type_name, walk_frames=wf, death_frames=df, frame_w=fw, frame_h=fh)
        self.type = type_name
        self.behavior = cfg['behavior']
        self.damage = cfg['damage']
        self.drop_chance = cfg.get('drop_chance', 0.2)

    def update(self, player_pos, enemy_bullets):
        if self.state == "death":
            self.animate()
            return

        dist_vec = player_pos - self.pos
        if dist_vec.length() > 0:
            direction = dist_vec.normalize()
            
            self.angle = math.degrees(math.atan2(-direction.y, direction.x))
            self.angle += 90
            
            if self.behavior == "chase":
                self.pos += direction * self.speed
            elif self.behavior == "zigzag":
                perp = pygame.math.Vector2(-direction.y, direction.x)
                self.pos += direction * self.speed + perp * math.sin(pygame.time.get_ticks() * 0.01) * 3
            elif self.behavior == "ranged":
                if dist_vec.length() > 250:
                    self.pos += direction * self.speed
                elif dist_vec.length() < 200:
                    self.pos -= direction * self.speed
                
                if random.random() < 0.01:
                    bullet_angle = math.atan2(dist_vec.y, dist_vec.x)
                    enemy_bullets.add(Projectile(self.pos.x, self.pos.y, bullet_angle, 5, self.damage, (255, 0, 255)))

        self.animate()