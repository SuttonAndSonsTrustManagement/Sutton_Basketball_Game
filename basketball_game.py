import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atari-Style Basketball Game with Resized Images")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Load images
player_image = pygame.image.load("player.png")
ball_image = pygame.image.load("ball.png")
basket_image = pygame.image.load("basket.png")

# Scale images (2/3 of current size)
player_image = pygame.transform.scale(player_image, (int(150 * 2 / 3), int(210 * 2 / 3)))  # Previous size was (150, 210)
ball_image = pygame.transform.scale(ball_image, (int(60 * 2 / 3), int(60 * 2 / 3)))        # Previous size was (60, 60)
basket_image = pygame.transform.scale(basket_image, (int(300 * 2 / 3), int(150 * 2 / 3)))  # Previous size was (300, 150)

# Game variables
player_x, player_y = WIDTH // 2, HEIGHT - 160  # Adjusted for smaller size
player_speed = 5
ball_x, ball_y = player_x, player_y - 40
ball_dx, ball_dy = 0, 0
basket_x, basket_y = random.randint(100, WIDTH - 300), 50  # Adjusted for smaller basket size
score = 0
shooting = False

# Dribbling variables
dribble_up = True  # Direction of ball dribble
dribble_height = 10  # Height of dribble (adjusted for smaller ball)

# Fonts
font = pygame.font.Font(None, 36)

# Functions
def draw_player(x, y):
    screen.blit(player_image, (x - player_image.get_width() // 2, y - player_image.get_height()))

def draw_ball(x, y):
    screen.blit(ball_image, (x - ball_image.get_width() // 2, y - ball_image.get_height() // 2))

def draw_basket(x, y):
    screen.blit(basket_image, (x, y))

def display_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

# Game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 50:  # Adjust for smaller image size
        player_x -= player_speed
        if not shooting:
            ball_x -= player_speed
            # Dribble logic
            ball_y += -dribble_height if dribble_up else dribble_height
            dribble_up = not dribble_up
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
        player_x += player_speed
        if not shooting:
            ball_x += player_speed
            # Dribble logic
            ball_y += -dribble_height if dribble_up else dribble_height
            dribble_up = not dribble_up
    if keys[pygame.K_SPACE] and not shooting:  # Shoot the ball
        ball_dx = 0
        ball_dy = -10
        shooting = True

    # Ball movement
    if shooting:
        ball_y += ball_dy
        ball_x += ball_dx

    # Check if the ball scores
    if (basket_x < ball_x < basket_x + basket_image.get_width()) and (basket_y < ball_y < basket_y + basket_image.get_height()):
        score += 1
        shooting = False
        ball_x, ball_y = player_x, player_y - 40
        basket_x, basket_y = random.randint(100, WIDTH - 300), 50

    # Reset ball if it goes out of bounds
    if ball_y < 0:
        shooting = False
        ball_x, ball_y = player_x, player_y - 40

    # Draw game objects
    draw_player(player_x, player_y)
    draw_ball(ball_x, ball_y)
    draw_basket(basket_x, basket_y)
    display_score(score)

    # Update the screen
    pygame.display.flip()
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()