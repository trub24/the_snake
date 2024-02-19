from random import choice, randrange

import pygame

pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
    """Функция - бинд клавиш, под направления движения."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Родительский класс всех объектов игры."""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = (0, 0, 0)

    def draw(self, surface, body_color, rect):
        """Метод родительского класса отрисовывающий 1 клетку"""
        pygame.draw.rect(surface, body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс описывающий игровой объект яюлоко."""

    def __init__(self):
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Метод, который создает новую случайную позицию."""
        position = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                    randrange(0, SCREEN_HEIGHT, GRID_SIZE))
        return position

    def draw(self, surface):
        """Метод отрисовывающий яблоко"""
        body_color = self.body_color
        rect = pygame.Rect((self.position[0], self.position[1]),
                           (GRID_SIZE, GRID_SIZE))
        GameObject.draw(Apple, surface, body_color, rect)


class Snake(GameObject):
    """Класс описывающий игровой объект змейка."""

    def __init__(self):
        super().__init__()
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Метод - обнавляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод - описывате движения змейки."""
        head_pos = self.get_head_position()
        directions = {
            RIGHT: (head_pos[0] + GRID_SIZE, head_pos[1]),
            LEFT: (head_pos[0] - GRID_SIZE, head_pos[1]),
            UP: (head_pos[0], head_pos[1] - GRID_SIZE),
            DOWN: (head_pos[0], head_pos[1] + GRID_SIZE)
        }
        new_pos = directions[self.direction]
        if new_pos in self.positions:
            self.reset()

        x, y = new_pos
        if x < 0:
            x = SCREEN_WIDTH - GRID_SIZE
        elif x >= SCREEN_WIDTH:
            x = 0
        else:
            x = x

        if y < 0:
            y = SCREEN_HEIGHT - GRID_SIZE
        elif y >= SCREEN_HEIGHT:
            y = 0
        else:
            y = y

        self.positions.insert(0, (x, y))
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop(-1)

    def draw(self, surface):
        """Метод, который отрисовывает змейку."""
        body_color = self.body_color
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            GameObject.draw(Snake, surface, body_color, rect)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        GameObject.draw(Snake, surface, body_color, head_rect)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод - возвращает координаты 1  элемента змейки."""
        return self.positions[0]

    def reset(self):
        """Метод, который отвечает за откат змейки в начальное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        screen.fill(BOARD_BACKGROUND_COLOR)


def main():
    """Функция, в кторой прописана логика игры."""
    apple = Apple()
    snake = Snake()

    while True:
        handle_keys(snake)
        clock.tick(SPEED)
        snake.update_direction()
        snake.move()
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
