import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Circle vs Squares')

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Clock
clock = pygame.time.Clock()

# Player Settings
player_radius = 30
player_color = GREEN
player_pos = [WIDTH // 2, HEIGHT // 2]
player_angle = 0
player_speed = 5
shoot_cooldown = 1000  # ms
cooldown_reduction = 50  # reduction in ms after every 3 kills
last_shot_time = 0

# Bullet Settings
bullet_radius = player_radius // 3
bullet_speed = 7
bullets = []

# Enemy Settings
enemy_size = 40
enemy_speed = 2
enemies = []
enemy_spawn_rate = 3000  # in ms, starts at 1 enemy every 3 seconds
last_enemy_spawn = 0

# Score and Game State
score = 0
kill_count = 0
game_over = False
font = pygame.font.SysFont(None, 48)

def spawn_enemy():
    """Spawn an enemy at a random location, outside the screen."""
    x = random.choice([random.randint(-enemy_size, 0), random.randint(WIDTH, WIDTH + enemy_size)])
    y = random.choice([random.randint(-enemy_size, 0), random.randint(HEIGHT, HEIGHT + enemy_size)])
    enemies.append(pygame.Rect(x, y, enemy_size, enemy_size))

def rotate_point(origin, point, angle):
    """Rotate a point counterclockwise by a given angle around a given origin."""
    ox, oy = origin
    px, py = point
    angle = math.radians(angle)
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return [qx, qy]

def shoot_bullet():
    """Shoot a bullet from the player's position in the direction they're facing."""
    global last_shot_time, shoot_cooldown

    current_time = pygame.time.get_ticks()
    if current_time - last_shot_time >= shoot_cooldown:
        # Calculate bullet spawn point
        direction = rotate_point(player_pos, [player_pos[0], player_pos[1] - player_radius], player_angle)
        dx, dy = direction[0] - player_pos[0], direction[1] - player_pos[1]
        dist = math.sqrt(dx**2 + dy**2)
        dx, dy = dx / dist, dy / dist

        # Add the bullet with direction
        bullets.append({"pos": [player_pos[0], player_pos[1]], "dir": [dx, dy]})
        last_shot_time = current_time

def handle_input():
    """Handle player input for movement and shooting."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos[1] -= player_speed
    if keys[pygame.K_s]:
        player_pos[1] += player_speed
    if keys[pygame.K_a]:
        player_pos[0] -= player_speed
    if keys[pygame.K_d]:
        player_pos[0] += player_speed
    if keys[pygame.K_j]:
        global player_angle
        player_angle += 5
    if keys[pygame.K_k]:
        player_angle -= 5
    if keys[pygame.K_SPACE]:
        shoot_bullet()

def handle_bullets():
    """Update and draw bullets, handle collisions with enemies."""
    global kill_count, score, shoot_cooldown
    for bullet in bullets[:]:
        bullet["pos"][0] += bullet["dir"][0] * bullet_speed
        bullet["pos"][1] += bullet["dir"][1] * bullet_speed
        pygame.draw.circle(screen, BLACK, (int(bullet["pos"][0]), int(bullet["pos"][1])), bullet_radius)

        # Remove bullet if it goes off-screen
        if bullet["pos"][0] < 0 or bullet["pos"][0] > WIDTH or bullet["pos"][1] < 0 or bullet["pos"][1] > HEIGHT:
            bullets.remove(bullet)

        # Check for collision with enemies
        for enemy in enemies[:]:
            if pygame.Rect.collidepoint(enemy, bullet["pos"]):
                enemies.remove(enemy)
                if bullet in bullets:
                    bullets.remove(bullet)
                kill_count += 1
                score += 1

                # Update cooldown after every 3 kills
                if kill_count % 3 == 0 and shoot_cooldown > 100:
                    shoot_cooldown -= cooldown_reduction

def handle_enemies():
    """Update enemies, move them towards the player, and check for collisions."""
    global game_over
    for enemy in enemies[:]:
        # Move enemy towards player
        dx, dy = player_pos[0] - enemy.x, player_pos[1] - enemy.y
        dist = math.sqrt(dx**2 + dy**2)
        dx, dy = dx / dist, dy / dist
        enemy.x += dx * enemy_speed
        enemy.y += dy * enemy_speed

        # Draw the enemy as a square
        pygame.draw.rect(screen, RED, enemy)

        # Check collision with player
        if math.sqrt((enemy.centerx - player_pos[0])**2 + (enemy.centery - player_pos[1])**2) < player_radius:
            game_over = True

def reset_game():
    """Reset the game after the player loses."""
    global score, kill_count, game_over, enemies, bullets, player_pos, shoot_cooldown
    score = 0
    kill_count = 0
    game_over = False
    enemies = []
    bullets = []
    player_pos = [WIDTH // 2, HEIGHT // 2]
    shoot_cooldown = 1000

# Game loop
running = True
while running:
    screen.fill(WHITE)

    if game_over:
        # Display Game Over and Score
        game_over_text = font.render("You Lost", True, BLACK)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.update()

        # Reset if space bar is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()
        continue

    # Handle input
    handle_input()

    # Player Circle
    pygame.draw.circle(screen, player_color, (int(player_pos[0]), int(player_pos[1])), player_radius)

    # Bullets
    handle_bullets()

    # Enemies
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn >= enemy_spawn_rate:
        spawn_enemy()
        last_enemy_spawn = current_time

    handle_enemies()

    # Draw Score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update display
    pygame.display.update()

    # Frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
