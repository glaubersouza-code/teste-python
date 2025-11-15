import random
import math
from pygame import Rect

WIDTH = 800
HEIGHT = 600
TITLE = "Platform Adventure"

# Estados do jogo
MENU = 0
PLAYING = 1
GAME_OVER = 2

# Cores
BLUE = (100, 150, 255)
GREEN = (100, 200, 100)
RED = (255, 100, 100)
BROWN = (150, 100, 50)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Variáveis globais
game_state = MENU
music_on = True
sounds_on = True
score = 0

class Player:
    def __init__(self):
        self.x = 100
        self.y = 300
        self.width = 40
        self.height = 60
        self.velocity_y = 0
        self.jumping = False
        self.direction = 1
        self.animation_frame = 0
        self.is_running = False
        
    def update(self, platforms):
        # Gravidade
        self.velocity_y += 0.5
        self.y += self.velocity_y
        
        # Colisão com plataformas
        on_ground = False
        player_rect = Rect(self.x, self.y, self.width, self.height)
        
        for platform in platforms:
            platform_rect = Rect(platform.x, platform.y, platform.width, platform.height)
            if player_rect.colliderect(platform_rect):
                if self.velocity_y > 0 and self.y + self.height > platform.y and self.y < platform.y:
                    self.y = platform.y - self.height
                    self.velocity_y = 0
                    on_ground = True
                    self.jumping = False
        
        # Animação
        self.animation_frame += 1
        return on_ground
    
    def jump(self):
        if not self.jumping:
            self.velocity_y = -12
            self.jumping = True
            # SOM DO PULO - usando beep simples
            if sounds_on:
                try:
                    # Tenta tocar um som simples
                    import os
                    os.system('echo -e "\a"')  # Beep do sistema
                except:
                    pass
    
    def move_left(self):
        self.x = max(0, self.x - 5)
        self.direction = -1
        self.is_running = True
    
    def move_right(self):
        self.x = min(WIDTH - self.width, self.x + 5)
        self.direction = 1
        self.is_running = True
    
    def stop(self):
        self.is_running = False
    
    def draw(self):
        # Desenhar personagem
        player_rect = Rect(self.x, self.y, self.width, self.height)
        screen.draw.filled_rect(player_rect, BLUE)
        
        # Olhos
        eye_x = self.x + 30 if self.direction == 1 else self.x + 10
        screen.draw.filled_circle((eye_x, self.y + 20), 5, BLACK)
        
        # Pernas animadas
        leg_offset = math.sin(self.animation_frame * 0.5) * 5 if self.is_running else 0
        screen.draw.line((self.x + 10, self.y + self.height), 
                         (self.x + 10, self.y + self.height + 15 + leg_offset), BLACK)
        screen.draw.line((self.x + 30, self.y + self.height), 
                         (self.x + 30, self.y + self.height + 15 - leg_offset), BLACK)

class Enemy:
    def __init__(self, x, y, width, height, patrol_distance):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.start_x = x
        self.patrol_distance = patrol_distance
        self.direction = 1
        self.speed = 2
        self.animation_frame = 0
        
    def update(self):
        # Movimento de patrulha
        self.x += self.speed * self.direction
        if self.x > self.start_x + self.patrol_distance:
            self.direction = -1
        elif self.x < self.start_x:
            self.direction = 1
        
        self.animation_frame += 1
    
    def draw(self):
        # Desenhar inimigo
        enemy_rect = Rect(self.x, self.y, self.width, self.height)
        screen.draw.filled_rect(enemy_rect, RED)
        
        # Olhos
        eye_x = self.x + 15 if self.direction == 1 else self.x + 5
        screen.draw.filled_circle((eye_x, self.y + 15), 4, BLACK)
        
        # Pernas animadas
        leg_offset = math.sin(self.animation_frame * 0.5) * 3
        screen.draw.line((self.x + 5, self.y + self.height), 
                         (self.x + 5, self.y + self.height + 10 + leg_offset), BLACK)
        screen.draw.line((self.x + 15, self.y + self.height), 
                         (self.x + 15, self.y + self.height + 10 - leg_offset), BLACK)

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self):
        platform_rect = Rect(self.x, self.y, self.width, self.height)
        screen.draw.filled_rect(platform_rect, BROWN)

class Button:
    def __init__(self, x, y, width, height, text, color=GREEN):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
    
    def is_clicked(self, pos):
        x, y = pos
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)
    
    def draw(self):
        button_rect = Rect(self.x, self.y, self.width, self.height)
        screen.draw.filled_rect(button_rect, self.color)
        screen.draw.text(self.text, (self.x + 10, self.y + 10), color=BLACK, fontsize=24)

# Inicializar objetos do jogo
player = Player()
platforms = [
    Platform(0, 500, 800, 100),
    Platform(100, 400, 200, 20),
    Platform(400, 350, 150, 20),
    Platform(200, 250, 200, 20),
    Platform(500, 200, 150, 20)
]

enemies = [
    Enemy(150, 380, 30, 40, 100),
    Enemy(450, 330, 30, 40, 80),
    Enemy(250, 230, 30, 40, 120)
]

# Botões do menu
start_button = Button(300, 200, 200, 50, "Start Game")
music_button = Button(300, 270, 200, 50, "Music: ON")
sounds_button = Button(300, 340, 200, 50, "Sounds: ON")
exit_button = Button(300, 410, 200, 50, "Exit")

def play_game_over_sound():
    """Toca um som simples de game over"""
    if sounds_on:
        try:
            # Beep duplo para game over
            import os
            os.system('echo -e "\a"')
        except:
            pass

def draw():
    screen.fill((50, 50, 80))
    
    if game_state == MENU:
        screen.draw.text("PLATFORM ADVENTURE", (200, 100), color=WHITE, fontsize=48)
        start_button.draw()
        music_button.draw()
        sounds_button.draw()
        exit_button.draw()
    
    elif game_state == PLAYING:
        for platform in platforms:
            platform.draw()
        
        for enemy in enemies:
            enemy.draw()
        
        player.draw()
        screen.draw.text(f"Score: {score}", (10, 10), color=WHITE, fontsize=24)
    
    elif game_state == GAME_OVER:
        screen.draw.text("GAME OVER", (250, 200), color=RED, fontsize=48)
        screen.draw.text("Click to return to menu", (250, 300), color=WHITE, fontsize=24)

def update():
    global game_state, score
    
    if game_state == PLAYING:
        player.update(platforms)
        score += 1
        
        for enemy in enemies:
            enemy.update()
            
            # Verificar colisão com inimigos
            player_rect = Rect(player.x, player.y, player.width, player.height)
            enemy_rect = Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            
            if player_rect.colliderect(enemy_rect):
                game_state = GAME_OVER
                play_game_over_sound()

def on_key_down(key):
    if game_state == PLAYING:
        if key == keys.SPACE:
            player.jump()
        elif key == keys.LEFT:
            player.move_left()
        elif key == keys.RIGHT:
            player.move_right()

def on_key_up(key):
    if game_state == PLAYING:
        if key == keys.LEFT or key == keys.RIGHT:
            player.stop()

def on_mouse_down(pos):
    global game_state, music_on, sounds_on, score
    
    if game_state == MENU:
        if start_button.is_clicked(pos):
            game_state = PLAYING
            # Resetar jogo
            player.x = 100
            player.y = 300
            player.velocity_y = 0
            player.jumping = False
            score = 0
        
        elif music_button.is_clicked(pos):
            music_on = not music_on
            music_button.text = f"Music: {'ON' if music_on else 'OFF'}"
        
        elif sounds_button.is_clicked(pos):
            sounds_on = not sounds_on
            sounds_button.text = f"Sounds: {'ON' if sounds_on else 'OFF'}"
        
        elif exit_button.is_clicked(pos):
            exit()
    
    elif game_state == GAME_OVER:
        game_state = MENU