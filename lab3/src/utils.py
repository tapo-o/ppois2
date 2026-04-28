import json
import os
import pygame

WIDTH, HEIGHT = 1024, 768
FPS = 60
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

def load_config():
    path = os.path.join(DATA_DIR, 'config.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

CONFIG = load_config()

def load_scores():
    path = os.path.join(DATA_DIR, 'scores.json')
    if not os.path.exists(path): return []
    with open(path, 'r', encoding='utf-8') as f:
        return sorted(json.load(f), key=lambda x: x['score'], reverse=True)[:10]

def save_score(name, score):
    path = os.path.join(DATA_DIR, 'scores.json')
    scores = load_scores()
    scores.append({"name": name, "score": score})
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(scores, f, indent=4, ensure_ascii=False)

class AssetManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.images = {}
            cls._instance.sounds = {}
            cls._instance.sprite_rows = {} 

        return cls._instance

    def get_image(self, name, size=None, default_color=(255, 255, 255)):
        key = f"{name}_{size}"
        if key in self.images: return self.images[key]
        path = os.path.join(ASSETS_DIR, 'images', name)
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            if size: img = pygame.transform.scale(img, size)
            self.images[key] = img
        else:
            w, h = size if size else (30, 30)
            img = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.circle(img, default_color, (w//2, h//2), w//2)
            self.images[key] = img
        return self.images[key]

    def get_anim_frames(self, prefix, state, count, size, color):
        frames = []
        for i in range(count):
            fname = f"{prefix}_{state}_{i}.png"
            frames.append(self.get_image(fname, size, color))
        return frames

    def play_music(self, name):
        path = os.path.join(ASSETS_DIR, 'sounds', name)
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1)

    def play_sound(self, name, vol=1.0):
        path = os.path.join(ASSETS_DIR, 'sounds', name)
        if name not in self.sounds and os.path.exists(path):
            self.sounds[name] = pygame.mixer.Sound(path)
        if name in self.sounds:
            self.sounds[name].set_volume(vol)
            self.sounds[name].play()

    def get_spritesheet_row(self, name, frame_width, frame_height, row_idx, count, size=None, default_color=(255, 255, 255)):
        

        cache_key = f"{name}_{row_idx}_{count}_{size}"
        if cache_key in self.sprite_rows:
            return self.sprite_rows[cache_key] 


        path = os.path.join(ASSETS_DIR, 'images', name)
        
        if not os.path.exists(path):
            frames = []
            w, h = size if size else (frame_width, frame_height)
            for _ in range(count):
                img = pygame.Surface((w, h), pygame.SRCALPHA)
                pygame.draw.circle(img, default_color, (w//2, h//2), w//2)
                frames.append(img)
            self.sprite_rows[cache_key] = frames
            return frames
            
        

        if name not in self.images:
            self.images[name] = pygame.image.load(path).convert_alpha()
        sheet = self.images[name]
        
        frames = []
        for i in range(count):
            rect = pygame.Rect(i * frame_width, row_idx * frame_height, frame_width, frame_height)
            frame = pygame.Surface(rect.size, pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), rect)
            
            if size:
                frame = pygame.transform.scale(frame, size)
            frames.append(frame)
            
        self.sprite_rows[cache_key] = frames 

        return frames