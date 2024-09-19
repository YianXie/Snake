import pygame
import random
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

pygame.init()
pygame.font.init()
pygame.display.set_caption("Snake Game")

def game_over():
    global run
    run = False
    print("Game Over!")
    pygame.quit()

class Snake:
    def __init__(self, body_length, body_size):
        self.snakes = []
        self.body_length = body_length
        self.body_size = body_size
        self.direction = "right"
        self.snake_speed = self.body_size
        self.snake_color = "green"
        
    def initialize_snake(self):
        for i in range(self.body_length):
            snake = pygame.rect.Rect(SCREEN_WIDTH // 2 - i * self.body_size, SCREEN_HEIGHT // 2, self.body_size, self.body_size)
            self.snakes.append({"x": snake.x, "y": snake.y})
            
    def move_snake(self):
        for i in range(len(self.snakes) - 1, 0, -1):
            self.snakes[i]['x'] = self.snakes[i - 1]['x']
            self.snakes[i]['y'] = self.snakes[i - 1]['y']

        if self.direction == "left":
            self.snakes[0]['x'] -= self.snake_speed
        if self.direction == "right":
            self.snakes[0]['x'] += self.snake_speed
        if self.direction == "up":
            self.snakes[0]['y'] -= self.snake_speed
        if self.direction == "down":
            self.snakes[0]['y'] += self.snake_speed
            
    def draw_snake(self, screen):
        for snake in self.snakes:
            pygame.draw.rect(screen, self.snake_color, (snake['x'], snake['y'], self.body_size, self.body_size))
            
    def increase_body(self):
        last_snake = self.snakes[-1]
        self.snakes.append({"x": last_snake['x'], "y": last_snake['y']})

class Score:
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    
    def __init__(self, default_score):
        self.score = default_score
        self.background_height = 50
        self.FONT_SIZE = 30
        
    def update_score(self, amount=0):
        self.score += amount
        self.text_surface = self.my_font.render(f'Score: {self.score}', False, (0, 0, 0))
    
    def draw_score(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, SCREEN_WIDTH, self.background_height))
        screen.blit(self.text_surface, (SCREEN_WIDTH // 2 - self.FONT_SIZE * 2, 0))

class Fruit:
    def __init__(self, snake_body_size=25, score_background_height=50):
        self.fruit_size = 25
        self.fruit_color = "red"
        self.snake_body_size = snake_body_size
        self.score_background_height = score_background_height
        self.fruit = pygame.rect.Rect(
            random.randint(0, SCREEN_WIDTH // self.fruit_size) * self.fruit_size, 
            random.randint(0, SCREEN_HEIGHT // self.fruit_size) * self.fruit_size, 
            self.fruit_size, 
            self.fruit_size
        )
    
    def generate_fruit(self):
        valid_position = False
        while not valid_position:
            self.fruit.x = random.randint(0, SCREEN_WIDTH - self.snake_body_size)
            self.fruit.y = random.randint(self.score_background_height, SCREEN_HEIGHT - self.snake_body_size)
            if abs(self.fruit.x) % self.snake_body_size == 0 and abs(self.fruit.y) % self.snake_body_size == 0:
                valid_position = True
    
    def draw_fruit(self, screen):
        pygame.draw.rect(screen, self.fruit_color, self.fruit)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
snake = Snake(3, 25)
snake.initialize_snake()
score = Score(0)
score.update_score()
fruit = Fruit()
fruit.generate_fruit()

run = True
while run:
    pygame.time.delay(100)
    screen.fill((0, 0, 0))
    fruit.draw_fruit(screen)
    score.draw_score(screen)
    snake.draw_snake(screen)
    
    if snake.snakes[0]['x'] == fruit.fruit.x and snake.snakes[0]['y'] == fruit.fruit.y:
        score.update_score(1)
        fruit.generate_fruit()
        snake.increase_body()
    
    # check if the snake has collided with itself
    if snake.snakes[0]['x'] not in range(0, SCREEN_WIDTH) or snake.snakes[0]['y'] not in range(score.background_height, SCREEN_HEIGHT):
        game_over()
    
    key = pygame.key.get_pressed()
    if (key[pygame.K_LEFT] or key[pygame.K_a]) and snake.direction != "right":
        snake.direction = "left"
    if (key[pygame.K_RIGHT] or key[pygame.K_d]) and snake.direction != "left":
        snake.direction = "right"
    if (key[pygame.K_UP] or key[pygame.K_w]) and snake.direction != "down":
        snake.direction = "up"
    if (key[pygame.K_DOWN] or key[pygame.K_s]) and snake.direction != "up":
        snake.direction = "down"
    
    snake.move_snake()
    os.system('clear')
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()