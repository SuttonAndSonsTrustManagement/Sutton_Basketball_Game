import pygame
import random
import sys
import time
import os

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atari-Style Basketball Game with Leaderboard & Shot Clock")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Load images
player_image = pygame.image.load("player.png")
ball_image = pygame.image.load("ball.png")
basket_image = pygame.image.load("basket.png")

# Scale images (2/3 of original size)
player_image = pygame.transform.scale(player_image, (int(150 * 2 / 3), int(210 * 2 / 3)))
ball_image = pygame.transform.scale(ball_image, (int(60 * 2 / 3), int(60 * 2 / 3)))
basket_image = pygame.transform.scale(basket_image, (int(300 * 2 / 3), int(150 * 2 / 3)))

# Game variables
player_x, player_y = WIDTH // 2, HEIGHT - 160
player_speed = 5
ball_x, ball_y = player_x, player_y - 40
ball_dx, ball_dy = 0, 0
basket_x, basket_y = random.randint(100, WIDTH - 300), 50
shooting = False

# Dribbling variables
dribble_up = True
dribble_height = 10

# Score tracking
score = 0
makes = 0
misses = 0
fg_percentage = 0.0
sharp_shooter_percentage = 0.0
sharp_shooter_scores = []

# Shot clock variables
SHOT_CLOCK_START = 24  # 24-second shot clock
shot_clock = SHOT_CLOCK_START
last_reset_time = time.time()

# Fonts
font = pygame.font.Font(None, 36)
leaderboard_font = pygame.font.Font(None, 48)

# Leaderboard
LEADERBOARD_FILE = "leaderboard.txt"

def draw_player(x, y):
    screen.blit(player_image, (x - player_image.get_width() // 2, y - player_image.get_height()))

def draw_ball(x, y):
    screen.blit(ball_image, (x - ball_image.get_width() // 2, y - ball_image.get_height() // 2))

def draw_basket(x, y):
    screen.blit(basket_image, (x, y))

def display_score():
    """Displays the score, FG%, and shooting analytics in the lower-left corner."""
    text_y = HEIGHT - 150
    offset = 30

    score_text = font.render(f"Score: {score:.1f}", True, WHITE)
    makes_text = font.render(f"Makes: {makes}", True, WHITE)
    misses_text = font.render(f"Misses: {misses}", True, WHITE)
    fg_text = font.render(f"FG%: {fg_percentage:.1f}%", True, WHITE)
    sharp_text = font.render(f"Sharp Shooter%: {sharp_shooter_percentage:.1f}%", True, WHITE)
    shot_clock_text = font.render(f"{int(shot_clock)}", True, RED)

    screen.blit(score_text, (10, text_y))
    screen.blit(makes_text, (10, text_y + offset))
    screen.blit(misses_text, (10, text_y + offset * 2))
    screen.blit(fg_text, (10, text_y + offset * 3))
    screen.blit(sharp_text, (10, text_y + offset * 4))
    screen.blit(shot_clock_text, (WIDTH - 50, HEIGHT - 50))  # Bottom-right shot clock

def calculate_sharp_shooter_accuracy(ball_x, basket_x):
    """Calculate shot accuracy based on how close the ball lands to the basket's center."""
    basket_center_x = basket_x + basket_image.get_width() // 2
    max_distance = basket_image.get_width() // 2
    distance = abs(ball_x - basket_center_x)
    return max(0, 100 - (distance / max_distance) * 100)

def save_leaderboard(new_score):
    """Save and update the top 3 scores."""
    scores = []
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as file:
            scores = [float(line.strip()) for line in file.readlines()]
    
    scores.append(new_score)
    scores = sorted(scores, reverse=True)[:3]  # Keep top 3 scores

    with open(LEADERBOARD_FILE, "w") as file:
        for s in scores:
            file.write(f"{s:.1f}\n")

    return scores

def display_leaderboard(scores):
    """Show the leaderboard at the end of the game."""
    screen.fill(BLACK)
    title_text = leaderboard_font.render("Leaderboard", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - 100, 50))

    for i, s in enumerate(scores):
        score_text = font.render(f"{i+1}. {s:.1f}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - 50, 150 + i * 40))

    pygame.display.flip()
    time.sleep(5)  # Show leaderboard for 5 seconds

# Game loop
running = True
while running:
    screen.fill(BLACK)
    elapsed_time = time.time() - last_reset_time
    shot_clock = max(0, SHOT_CLOCK_START - elapsed_time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 50:
        player_x -= player_speed
        if not shooting:
            ball_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
        player_x += player_speed
        if not shooting:
            ball_x += player_speed
    if keys[pygame.K_SPACE] and not shooting:
        ball_dx = 0
        ball_dy = -10
        shooting = True
        last_reset_time = time.time()  # Reset shot clock

    if shooting:
        ball_y += ball_dy

    if (basket_x < ball_x < basket_x + basket_image.get_width()) and (basket_y < ball_y < basket_y + basket_image.get_height()):
        makes += 1
        sharp_shooter_percentage = calculate_sharp_shooter_accuracy(ball_x, basket_x)
        sharp_shooter_scores.append(sharp_shooter_percentage)
        score = sum(sharp_shooter_scores) / len(sharp_shooter_scores)
        shooting = False
        ball_x, ball_y = player_x, player_y - 40
        basket_x, basket_y = random.randint(100, WIDTH - 300), 50
    elif ball_y < 0:
        misses += 1
        shooting = False
        ball_x, ball_y = player_x, player_y - 40

    if makes + misses > 0:
        fg_percentage = (makes / (makes + misses)) * 100

    if shot_clock <= 0:
        running = False

    draw_player(player_x, player_y)
    draw_ball(ball_x, ball_y)
    draw_basket(basket_x, basket_y)
    display_score()
    pygame.display.flip()
    clock.tick(FPS)

leaderboard_scores = save_leaderboard(score)
display_leaderboard(leaderboard_scores)
pygame.quit()
sys.exit()
