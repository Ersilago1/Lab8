import pygame
import math

# Инициализация Pygame
pygame.init()

# Размеры экрана
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GFG Paint")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Задний фон (чёрный)
screen.fill(WHITE)
Dict = {1 : 3, 2 : 4}
print(Dict[1])
# Кнопки выбора цветов
COLOR_BUTTONS = [
    {"color": RED, "rect": pygame.Rect(10, 10, 50, 50)},
    {"color": YELLOW, "rect": pygame.Rect(70, 10, 50, 50)},
    {"color": GREEN, "rect": pygame.Rect(130, 10, 50, 50)},
    {"color": BLUE, "rect": pygame.Rect(190, 10, 50, 50)},
    {"color": PURPLE, "rect": pygame.Rect(250, 10, 50, 50)}
]

# Загрузка изображений инструментов
eraser_img = pygame.image.load('picandsound/eraser.png')
eraser_img = pygame.transform.scale(eraser_img, (50, 50))

# Кнопки выбора фигур
TOOLS = [
    {"name": "Линия", "rect": pygame.Rect(320, 10, 90, 40), "type": "pencil"},
    {"name": "Прямоугольник", "rect": pygame.Rect(420, 10, 150, 40), "type": "rectangle"},
    {"name": "Круг", "rect": pygame.Rect(580, 10, 90, 40), "type": "circle"},
]

# Кнопка выбора ластика
eraser_button = pygame.Rect(680, 10, 50, 50)

# Текущие настройки
current_color = WHITE
current_tool = "pencil"
drawing = False
start_pos = None
last_pos = None

# Оригинальные функции для рисования
def draw_pencil(surface, color, start, end, width=3):
    pygame.draw.line(surface, color, start, end, width)

def draw_rectangle(surface, color, start, end):
    x1, y1 = start
    x2, y2 = end
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    pygame.draw.rect(surface, color, (min(x1, x2), min(y1, y2), width, height), 3)

def draw_circle(surface, color, start, end):
    x1, y1 = start
    x2, y2 = end
    radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
    pygame.draw.circle(surface, color, start, radius, 3)

def erase_area(surface, position):
    pygame.draw.circle(surface, WHITE, position, 20)

# Основной цикл программы
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обработка клика мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # ЛКМ
                # Проверяем кнопки инструментов
                for button in TOOLS:
                    if button["rect"].collidepoint(event.pos):
                        current_tool = button["type"]

                # Проверяем кнопку ластика
                if eraser_button.collidepoint(event.pos):
                    current_tool = "eraser"

                # Проверяем кнопки цветов
                for button in COLOR_BUTTONS:
                    if button["rect"].collidepoint(event.pos):
                        current_color = button["color"]

                start_pos = event.pos
                last_pos = event.pos
                drawing = True

        # Отпускание кнопки мыши
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # ЛКМ
                drawing = False
                end_pos = event.pos
                if start_pos and end_pos:
                    if current_tool == "rectangle":
                        draw_rectangle(screen, current_color, start_pos, end_pos)
                    elif current_tool == "circle":
                        draw_circle(screen, current_color, start_pos, end_pos)

        # Движение мыши для рисования
        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if current_tool == "pencil":
                    draw_pencil(screen, current_color, last_pos, event.pos, 3)
                    last_pos = event.pos  # Обновляем последнюю позицию
                elif current_tool == "eraser":
                    erase_area(screen, event.pos)

    # Рисуем кнопки цветов
    for button in COLOR_BUTTONS:
        pygame.draw.rect(screen, button["color"], button["rect"])

    # Рисуем кнопки инструментов
    for button in TOOLS:
        pygame.draw.rect(screen, BLACK, button["rect"], 2)
        font = pygame.font.Font(None, 24)
        text = font.render(button["name"], True, BLACK)
        screen.blit(text, (button["rect"].x + 5, button["rect"].y + 10))

    # Кнопка ластика
    pygame.draw.rect(screen, BLACK, eraser_button, 2)
    screen.blit(eraser_img, (eraser_button.x, eraser_button.y))

    pygame.display.flip()

pygame.quit()
