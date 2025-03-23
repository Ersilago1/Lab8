import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

# Установка FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Размеры экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5  # Скорость движения врага
SCORE = 0  # Счетчик очков
coinscore = 0  # Счетчик монет

# Настройка шрифтов и текста
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, "black")

# Загрузка изображений
background = pygame.image.load(r"C:\Users\Admin\OneDrive\Рабочий стол\KBTU\PP2\Lab8\picandsound\road (1).png")
coin = pygame.image.load(r"C:\Users\Admin\OneDrive\Рабочий стол\KBTU\PP2\Lab8\picandsound\coin.png"),
coini = 0
coins = 0

# Переменные для фона и звука
bgy = 0
bgsound = pygame.mixer.Sound(r"C:\Users\Admin\OneDrive\Рабочий стол\KBTU\PP2\Lab8\picandsound\background.wav")
catchingcoin = pygame.mixer.Sound(r"C:\Users\Admin\OneDrive\Рабочий стол\KBTU\PP2\Lab8\picandsound\catch.mp3")
bgsound.play(1000000)

# Создание окна
DISPLAYSURF = pygame.display.set_mode((400,600))
pygame.display.set_caption("Racer")

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\Users\Admin\OneDrive\Рабочий стол\KBTU\PP2\Lab8\picandsound\Enemy (1).png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:  # Если враг ушел за границу экрана, он появляется заново
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\Users\Admin\OneDrive\Рабочий стол\KBTU\PP2\Lab8\picandsound\Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:  # Движение влево
                self.rect.move_ip(-7, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:  # Движение вправо
                self.rect.move_ip(7, 0)

# Класс монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin[coini]  # Использование монеты
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(32, SCREEN_WIDTH-32), -31)
        self.a = random.randint(600, 1000)
    
    def move(self):
        global coinscore
        self.rect.move_ip(0, 10)
        if self.rect.top > 600:  # Если монета ушла за экран, она появляется заново
            self.rect.top = -62
            self.rect.center = (random.randint(32, SCREEN_WIDTH-32), -31)
        elif self.rect.colliderect(P1):  # Проверка столкновения с игроком
            catchingcoin.play()
            coinscore += 1
            self.rect.top = -62
            self.rect.center = (random.randint(32, SCREEN_WIDTH-32), -31) 

# Создание спрайтов
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группы спрайтов
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
Coins = pygame.sprite.Group()
Coins.add(C1)

# Добавление события увеличения скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)


# Игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.3  # Увеличение скорости
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # Прокрутка фона
    DISPLAYSURF.blit(background, (0, bgy))
    DISPLAYSURF.blit(background, (0, bgy-600))
    if coini == 23:
        coini = 0
    else:
        coini += 1
    if bgy < 600:
        bgy += 7
    else:
        bgy = 0
    
    # Отображение очков
    scores = font_small.render(str(SCORE), True, "BLACK")
    coinscores = font_small.render(str(coinscore), True, "BLACK")
    DISPLAYSURF.blit(scores, (10,10))
    DISPLAYSURF.blit(coinscores, (360,10))
    
    # Отрисовка и движение спрайтов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    for el in Coins:
        DISPLAYSURF.blit(el.image, el.rect)
        el.move()
    
    # Проверка столкновения с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        bgsound.stop()
        pygame.mixer.Sound(r"C:\Users\Admin\OneDrive\Рабочий стол\KBTU\PP2\Lab8\picandsound\crash.wav").play()
        time.sleep(0.5)
        DISPLAYSURF.fill("RED")
        DISPLAYSURF.blit(game_over, (30,250))
        pygame.display.update()
        
        # Удаление спрайтов и завершение игры
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()
    
    pygame.display.update()
    FramePerSec.tick(FPS)