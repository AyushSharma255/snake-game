import pygame
from random import randint

from game_config_parser import background_color, border_color, snake_color, food_color

pygame.init()
pygame.font.init()
font = pygame.font.Font("font.ttf", 12)
width, height = 500, 500
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")

fps = 10
clock = pygame.time.Clock()
running = True


class Cube:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

    def move(self, x_vel, y_vel):
        (curr_x, curr_y) = self.pos
        self.pos = (curr_x + x_vel, curr_y + y_vel)

    def draw(self):
        pygame.draw.rect(display, self.color, (self.pos[0], self.pos[1], 10, 10))


class Snake:
    def __init__(self, x_vel, y_vel):
        self.body = [Cube((250, 250), snake_color), ]
        self.x_vel = x_vel
        self.y_vel = y_vel

    def draw(self):
        for cube in self.body:
            cube.draw()

    def eat(self):
        global score
        score += 1
        self.body.append(Cube(self.body[0].pos, snake_color))

        x_on_grid = randint(6, 34)
        y_on_grid = randint(6, 34)
        food.pos = (x_on_grid * 10, y_on_grid * 10)

        for cube in self.body:  # Food should not be on snake
            if cube.pos == food.pos:
                food.pos = (x_on_grid * 10, y_on_grid * 10)

    def move(self):
        # Move body except the head
        for cube in (self.body[1:])[::-1]:
            index = self.body.index(cube) - 1
            cube.pos = self.body[index].pos

        self.body[0].move(self.x_vel, self.y_vel)  # Move head


snake = Snake(x_vel=10, y_vel=0)
food = Cube((300, 250), food_color)

score = 1


def reset():
    global score, snake, food

    score = 1  # Reset score to 1
    snake = Snake(x_vel=10, y_vel=0)  # Reset snake to head only
    food = Cube((300, 250), food_color)  # Reset food


def draw():
    display.fill(background_color)

    # Border
    pygame.draw.rect(
        display, border_color, (45, 45, 410, 410)
    )  # Outer rectangle, actual border
    pygame.draw.rect(
        display, background_color, (50, 50, 400, 400)
    )  # Inner rectangle, covers inside

    # Score Text
    text = font.render(f"Score: {score}", True, border_color)
    display.blit(text, (50, 460))

    # Snake
    snake.draw()

    # Food
    food.draw()


while running:
    clock.tick(fps)  # Cap FPS
    draw()  # Draw
    pygame.display.update()  # Update drawing

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If quiting, terminate loop
            running = False
        # Move mechanic
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if snake.y_vel == 10:
                    if len(snake.body) == 1:
                        snake.y_vel = -10
                        snake.x_vel = 0
                else:
                    snake.y_vel = -10
                    snake.x_vel = 0
            elif event.key == pygame.K_s:
                if snake.y_vel == -10:
                    if len(snake.body) == 1:
                        snake.y_vel = 10
                        snake.x_vel = 0
                else:
                    snake.y_vel = 10
                    snake.x_vel = 0
            elif event.key == pygame.K_a:
                if snake.x_vel == 10:
                    if len(snake.body) == 1:
                        snake.x_vel = -10
                        snake.y_vel = 0
                else:
                    snake.x_vel = -10
                    snake.y_vel = 0
            elif event.key == pygame.K_d:
                if snake.x_vel == -10:
                    if len(snake.body) == 1:
                        snake.x_vel = 10
                        snake.y_vel = 0
                else:
                    snake.x_vel = 10
                    snake.y_vel = 0

    # Eat the food if collided with food
    if snake.body[0].pos == food.pos:
        snake.eat()

    # If you eat/collide your own body, you die
    for cube in snake.body[1:]:
        if (snake.body[0].pos[0] + snake.x_vel, snake.body[0].pos[1] + snake.y_vel) == cube.pos:
            reset()

    # If you hit the border, you die
    if not (40 < snake.body[0].pos[0] < 450 and 40 < snake.body[0].pos[1] < 450):
        reset()

    snake.move()


pygame.quit()  # Close window
