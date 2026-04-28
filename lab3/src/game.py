import pygame
import sys
import random
import math
from src.utils import WIDTH, HEIGHT, FPS, CONFIG, AssetManager, load_scores, save_score
from src.entities import Player, Enemy, SwordSlash, Drop

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont('Arial', 28)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=10)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.assets = AssetManager()
        self.font = pygame.font.SysFont('Arial', 32)
        self.small_font = pygame.font.SysFont('Arial', 24)
        self.state = "MENU"
        self.reset_game()

    def reset_game(self):
        self.player = Player(WIDTH // 2, HEIGHT // 2)
        self.all_sprites = pygame.sprite.Group(self.player)
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.drops = pygame.sprite.Group() # Группа для дропа
        self.current_wave_idx = 0
        self.enemies_to_spawn = []
        self.spawn_timer = 0
        self.score = 0

    def spawn_wave(self):
        if self.current_wave_idx < len(CONFIG['waves']):
            wave_data = CONFIG['waves'][self.current_wave_idx]
            for e_type, count in wave_data['enemies'].items():
                for _ in range(count):
                    side = random.choice(['top', 'bottom', 'left', 'right'])
                    if side == 'top': x, y = random.randint(0, WIDTH), -50
                    elif side == 'bottom': x, y = random.randint(0, WIDTH), HEIGHT + 50
                    elif side == 'left': x, y = -50, random.randint(0, HEIGHT)
                    else: x, y = WIDTH + 50, random.randint(0, HEIGHT)
                    self.enemies_to_spawn.append(Enemy(x, y, e_type))
            self.current_wave_idx += 1

    def handle_input(self):
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_w]: dy -= 1
            if keys[pygame.K_s]: dy += 1
            if keys[pygame.K_a]: dx -= 1
            if keys[pygame.K_d]: dx += 1
            self.player.move(dx, dy)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.player.shoot(self.player.pos.x, self.player.pos.y, pygame.mouse.get_pos(), self.bullets)
                if event.type == pygame.KEYDOWN:
                    # 1 - Меч (индекс 0), 2 - Пистолет (индекс 1), 3 - Ружье (индекс 2)
                    if event.key == pygame.K_1: self.player.weapon_idx = 0 
                    elif event.key == pygame.K_2: self.player.weapon_idx = 1 
                    elif event.key == pygame.K_3: self.player.weapon_idx = 2

    def spawn_drop(self, x, y, chance):
        if random.random() < chance:
            drop_type = random.choice(['medkit', 'ammo_shotgun', 'ammo_sword'])
            drop = Drop(x, y, drop_type)
            self.drops.add(drop)
            self.all_sprites.add(drop)

    def update(self):
        self.player.update()
        
        # Если игрок умер и анимация закончилась
        if self.player.state == "death" and not self.player.alive():
            self.check_highscore()

        if len(self.enemies) == 0 and len(self.enemies_to_spawn) == 0:
            if self.current_wave_idx < len(CONFIG['waves']):
                self.spawn_wave()
            elif self.player.state != "death":
                self.check_highscore()

        now = pygame.time.get_ticks()
        if self.enemies_to_spawn and now > self.spawn_timer:
            enemy = self.enemies_to_spawn.pop()
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            self.spawn_timer = now + 400

        self.bullets.update()
        self.enemy_bullets.update()
        self.drops.update()
        
        for e in self.enemies:
            e.update(self.player.pos, self.enemy_bullets)

        # Сбор дропа игроком
        if self.player.state != "death":
            for drop in pygame.sprite.spritecollide(self.player, self.drops, True, pygame.sprite.collide_circle):
                if drop.type == 'medkit':
                    self.player.hp = min(self.player.hp + 20, self.player.max_hp)
                elif drop.type == 'ammo_shotgun':
                    self.player.weapons[1].ammo = min(self.player.weapons[1].ammo + 10, self.player.weapons[1].max_ammo)
                elif drop.type == 'ammo_sword':
                    self.player.weapons[2].ammo = min(self.player.weapons[2].ammo + 15, self.player.weapons[2].max_ammo)

            # Урон игроку
            for enemy in pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_circle):
                if enemy.state != "death" and self.player.take_damage(enemy.damage / 60):
                    pass # Смерть обрабатывается в начале update

            if pygame.sprite.spritecollide(self.player, self.enemy_bullets, True, pygame.sprite.collide_circle):
                self.player.take_damage(10)

        # Урон врагам
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, False, False)
        for enemy, bullets_hit in hits.items():
            if enemy.state == "death": continue
            for b in bullets_hit:
                if not isinstance(b, SwordSlash):
                    b.kill()
                if enemy.take_damage(b.damage):
                    self.score += 10
                    self.spawn_drop(enemy.pos.x, enemy.pos.y, enemy.drop_chance)

    def check_highscore(self):
        if self.score <= 0:
            self.state = "MENU"
            return
        scores = load_scores()
        if not scores or self.score > scores[0]['score']:
            self.state = "NEW_RECORD"
        else:
            save_score("Player", self.score)
            self.state = "MENU"

    # ... [ОСТАВЛЯЕМ МЕТОДЫ input_record, show_menu, show_records БЕЗ ИЗМЕНЕНИЙ] ...
    
    # Для полноты ответа дублирую их, чтобы можно было скопировать:
    def input_record(self):
        name = ""
        while self.state == "NEW_RECORD":
            self.screen.fill((40, 0, 0))
            title = self.font.render("!!! GLOBAL TOP RECORD !!!", True, (255, 255, 0))
            score_txt = self.font.render(f"YOUR SCORE: {self.score}", True, (255, 255, 255))
            prompt = self.font.render(f"ENTER NAME: {name}_", True, (0, 255, 0))
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
            self.screen.blit(score_txt, (WIDTH//2 - score_txt.get_width()//2, HEIGHT//2 - 40))
            self.screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 + 20))
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name.strip():
                        save_score(name, self.score)
                        self.state = "RECORDS"
                    elif event.key == pygame.K_BACKSPACE: name = name[:-1]
                    elif len(name) < 12 and event.unicode.isprintable(): name += event.unicode
            pygame.display.flip()
            self.clock.tick(FPS)

    def show_menu(self):
            # 1. Включаем музыку для меню
            self.assets.play_music("mainmenu.wav")
            
            # 2. Настраиваем параллакс (два слоя фона)
            bg_back = self.assets.get_image("bg_menu_back.png", (WIDTH, HEIGHT), (20, 20, 25))
            bg_front = self.assets.get_image("bg_menu_front.png", (WIDTH, HEIGHT), (20, 20, 30))
            scroll_back = 0
            scroll_front = 0
            
            btn_w, btn_h = 250, 50
            # Сдвигаем кнопки немного выше (начинаем с 230 вместо 250) и уменьшаем шаг между ними
            start_btn = Button(WIDTH//2-btn_w//2, 230, btn_w, btn_h, "START GAME", (50, 150, 50), (70, 200, 70))
            scores_btn = Button(WIDTH//2-btn_w//2, 300, btn_w, btn_h, "RECORDS", (50, 50, 150), (70, 70, 200))
            help_btn = Button(WIDTH//2-btn_w//2, 370, btn_w, btn_h, "HELP", (150, 100, 50), (200, 150, 70)) # Оранжевая кнопка
            exit_btn = Button(WIDTH//2-btn_w//2, 440, btn_w, btn_h, "EXIT", (150, 50, 50), (200, 70, 70))
            
            while self.state == "MENU":
                # --- Логика параллакса ---
                scroll_back -= 0.5   
                scroll_front -= 1.5  
                
                if scroll_back <= -WIDTH: scroll_back = 0
                if scroll_front <= -WIDTH: scroll_front = 0
                
                self.screen.blit(bg_back, (scroll_back, 0))
                self.screen.blit(bg_back, (scroll_back + WIDTH, 0))
                
                self.screen.blit(bg_front, (scroll_front, 0))
                self.screen.blit(bg_front, (scroll_front + WIDTH, 0))
                # -------------------------

                title = self.font.render("CRIMSONLAND", True, (255, 50, 50))
                self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
                
                start_btn.draw(self.screen)
                scores_btn.draw(self.screen)
                help_btn.draw(self.screen) # Отрисовка кнопки справки
                exit_btn.draw(self.screen)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                    if start_btn.is_clicked(event): self.state = "PLAYING"
                    if scores_btn.is_clicked(event): self.state = "RECORDS"
                    if help_btn.is_clicked(event): self.state = "HELP" # Переход в справку
                    if exit_btn.is_clicked(event): pygame.quit(); sys.exit()
                    
                pygame.display.flip()
                self.clock.tick(FPS)

    def game_loop(self):
        self.reset_game()
        
        # Включаем музыку для игры
        self.assets.play_music("game_theme.mp3")
        
        # Загружаем фон для самой игры (например, земля/трава/асфальт)
        bg_game = self.assets.get_image("bg_game.png", (WIDTH, HEIGHT), (40, 40, 40))
        
        while self.state == "PLAYING":
            # Вместо заливки цветом рисуем фон
            self.screen.blit(bg_game, (0, 0))
            
            self.handle_input()
            self.update()
            
            self.all_sprites.draw(self.screen)
            self.draw_player_weapon()
            self.bullets.draw(self.screen)
            self.enemy_bullets.draw(self.screen)
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(FPS)

    def show_records(self):
        while self.state == "RECORDS":
            self.screen.fill((10, 10, 15))
            scores = load_scores()
            title = self.font.render("TOP 10 HEROES", True, (255, 215, 0))
            self.screen.blit(title, (WIDTH//2-title.get_width()//2, 50))
            for i, s in enumerate(scores):
                color = (255, 255, 255) if i > 0 else (0, 255, 0)
                txt = self.small_font.render(f"{i+1}. {s['name']}: {s['score']}", True, color)
                self.screen.blit(txt, (WIDTH//2-100, 150 + i*40))
            back_txt = self.small_font.render("Press ESC to Menu", True, (150, 150, 150))
            self.screen.blit(back_txt, (WIDTH//2-back_txt.get_width()//2, HEIGHT-80))
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "MENU"
            pygame.display.flip()
            self.clock.tick(FPS)

    def draw_ui(self):
        hp = self.font.render(f"HP: {int(max(0, self.player.hp))}", True, (255, 0, 0))
        wv = self.font.render(f"Wave: {self.current_wave_idx}", True, (255, 255, 255))
        sc = self.font.render(f"Score: {self.score}", True, (255, 255, 0))
        
        # Отображение патронов (ammo)
        weapon = self.player.current_weapon
        ammo_text = str(weapon.ammo) if weapon.max_ammo != float('inf') else "INF"
        am = self.font.render(f"[{weapon.name.upper()}] AMMO: {ammo_text}", True, (0, 255, 255))

        self.screen.blit(hp, (20, 20))
        self.screen.blit(wv, (WIDTH - 150, 20))
        self.screen.blit(sc, (WIDTH // 2 - 50, 20))
        self.screen.blit(am, (20, HEIGHT - 50))

    def show_help(self):
        rules_text = [
            "ПРАВИЛА И УПРАВЛЕНИЕ",
            "",
            "WASD - Движение персонажа",
            "Левая кнопка мыши - Стрельба / Атака",
            "Клавиши 1, 2, 3 - Смена оружия (Меч, Пистолет, Ружье)",
            "",
            "ЦЕЛЬ ИГРЫ:",
            "Отражайте волны врагов и выживайте как можно дольше.",
            "Собирайте выпадающий дроп для пополнения HP и патронов.",
            "",
            "Нажмите ESC для возврата в меню"
        ]

        while self.state == "HELP":
            self.screen.fill((20, 25, 30)) # Темно-синий фон
            
            for i, line in enumerate(rules_text):
                # Цветовое выделение для заголовка и футера
                if i == 0:
                    color = (255, 215, 0)
                    current_font = self.font
                elif i == len(rules_text) - 1:
                    color = (150, 150, 150)
                    current_font = self.small_font
                else:
                    color = (200, 220, 255)
                    current_font = self.small_font
                
                txt_surf = current_font.render(line, True, color)
                self.screen.blit(txt_surf, (WIDTH//2 - txt_surf.get_width()//2, 120 + i * 35))
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "MENU"
                    
            pygame.display.flip()
            self.clock.tick(FPS)

    def draw_player_weapon(self):
            if self.player.state == "death": return
            weapon = self.player.current_weapon
            mouse_pos = pygame.mouse.get_pos()
            
            # Вычисляем угол
            rel_x, rel_y = mouse_pos[0] - self.player.pos.x, mouse_pos[1] - self.player.pos.y
            angle = math.degrees(math.atan2(-rel_y, rel_x))
            
            # Смещение: выносим оружие на 25 пикселей от центра игрока в сторону мыши
            offset = 50
            weapon_pos_x = self.player.pos.x + math.cos(math.radians(-angle)) * offset
            weapon_pos_y = self.player.pos.y + math.sin(math.radians(-angle)) * offset
            
            # Вращаем спрайт
            rotated_weapon = pygame.transform.rotate(weapon.sprite, angle)
            weap_rect = rotated_weapon.get_rect(center=(weapon_pos_x, weapon_pos_y))
            
            self.screen.blit(rotated_weapon, weap_rect)

    def game_loop(self):
            self.reset_game()
            
            # Включаем музыку для игры
            self.assets.play_music("music.wav")
            
            # Загружаем фон для самой игры (например, земля/трава/асфальт)
            bg_game = self.assets.get_image("bg_game.png", (WIDTH, HEIGHT), (40, 40, 40))
            
            while self.state == "PLAYING":
                # Вместо заливки цветом рисуем фон
                self.screen.blit(bg_game, (0, 0))
                
                self.handle_input()
                self.update()
                
                self.all_sprites.draw(self.screen)
                self.draw_player_weapon()
                self.bullets.draw(self.screen)
                self.enemy_bullets.draw(self.screen)
                self.draw_ui()
                
                pygame.display.flip()
                self.clock.tick(FPS)

    def run(self):
            while True:
                if self.state == "MENU": self.show_menu()
                elif self.state == "PLAYING": self.game_loop()
                elif self.state == "RECORDS": self.show_records()
                elif self.state == "NEW_RECORD": self.input_record()
                elif self.state == "HELP": self.show_help() 