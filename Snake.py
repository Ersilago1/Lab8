import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры окна и сетки
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
DARK_RED = (139, 0, 0)

# Направления движения змейки
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Класс змейки
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.alive = True  # Флаг для проверки, жива ли змейка

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        if not self.alive:
            return
        
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE)

        # Проверка столкновения со стеной
        if new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT:
            self.alive = False
            return

        # Проверка столкновения с самим собой
        if new_head in self.positions:
            self.alive = False
            return

        # Перемещение змейки
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сброс игры при смерти."""
        self.__init__()  # Перезапуск змейки

    def draw(self, surface):
        """Отрисовка змейки на экране."""
        for segment in self.positions:
            pygame.draw.rect(surface, self.color, pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, WHITE, pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE), 1)

    def handle_keys(self):
        """Обработка ввода с клавиатуры."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT

# Класс еды
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        """Генерация еды в случайной позиции, исключая змейку."""
        while True:
            new_position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if new_position not in snake_positions:
                self.position = new_position
                break

    def draw(self, surface):
        """Отрисовка еды на экране."""
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, WHITE, pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE), 1)

def draw_text(surface, text, x, y, size=36, color=WHITE):
    """Функция отрисовки текста на экране."""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def game_over_screen(score):
    """Экран смерти с возможностью перезапуска."""
    screen.fill(DARK_RED)
    draw_text(screen, "ВЫ УМЕРЛИ!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 50, WHITE)
    draw_text(screen, f"Ваш счет: {score}", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 40, WHITE)
    draw_text(screen, "Нажмите ПРОБЕЛ для рестарта или ESC для выхода", SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 50, 30, WHITE)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Перезапуск
                    return
                elif event.key == pygame.K_ESCAPE:  # Выход
                    pygame.quit()
                    exit()

# Основная функция игры
def main():
    while True:
        snake = Snake()
        food = Food()
        score = 0
        level = 1
        clock = pygame.time.Clock()

        while snake.alive:
            screen.fill(BLACK)  # Очистка экрана
            snake.handle_keys()
            snake.move()

            # Проверка на поедание еды
            if snake.get_head_position() == food.position:
                snake.length += 1
                score += 1
                food.randomize_position(snake.positions)

                # Повышение уровня каждые 3 очка
                if score % 3 == 0:
                    level += 1

            # Проверка смерти
            if not snake.alive:
                game_over_screen(score)
                break  # Выход из игрового цикла и рестарт

            # Отрисовка объектов
            snake.draw(screen)
            food.draw(screen)

            # Отображение счета и уровня
            draw_text(screen, f"Score: {score}", 10, 10)
            draw_text(screen, f"Level: {level}", 10, 40)

            pygame.display.update()
            clock.tick(8 + level)  # Увеличение скорости змейки при повышении уровня

if __name__ == '__main__':
    main()
