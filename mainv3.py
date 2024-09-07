import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600  # Default for Easy mode
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
cooldown_reduction = 50  # reduction in ms after every 5 kills
last_shot_time = 0

# Bullet Settings
bullet_radius = player_radius // 3
bullet_speed = 7
bullets = []

# Enemy Settings
enemy_size = 40
enemy_speed = 2
enemies = []
enemy_spawn_rate = 4000  # in ms, starts at 1 enemy every 4 seconds
last_enemy_spawn = 0
spawn_decrease_rate = 1000  # decrease in ms after 1.5 minutes (90000 ms)

# Score and Game State
score = 0
kill_count = 0
game_over = False
font = pygame.font.SysFont(None, 48)

# Difficulty Settings
difficulty = 'Easy'
in_menu = True  # Flag for menu mode

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
    if keys[pygame.K_k]:  # Swapped K (left rotation)
        global player_angle
        player_angle += 5
    if keys[pygame.K_j]:  # Swapped J (right rotation)
        player_angle -= 5
    if keys[pygame.K_SPACE]:
        shoot_bullet()

    # Prevent player from going out of bounds
    if player_pos[0] - player_radius < 0:
        player_pos[0] = player_radius
    if player_pos[0] + player_radius > WIDTH:
        player_pos[0] = WIDTH - player_radius
    if player_pos[1] - player_radius < 0:
        player_pos[1] = player_radius
    if player_pos[1] + player_radius > HEIGHT:
        player_pos[1] = HEIGHT - player_radius

def draw_player():
    """Draw the player with a rotating aim marker."""
    pygame.draw.circle(screen, player_color, (int(player_pos[0]), int(player_pos[1])), player_radius)

    # Draw the aim marker (a line at the perimeter)
    aim_point = rotate_point(player_pos, [player_pos[0], player_pos[1] - player_radius], player_angle)
    pygame.draw.line(screen, BLACK, player_pos, aim_point, 2)

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

                # Update cooldown after every 5 kills
                if kill_count % 5 == 0 and shoot_cooldown > 100:
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

def select_difficulty():
    """Display difficulty selection menu and return selected difficulty."""
    difficulties = ["Easy", "Normal", "Hard"]
    selected_idx = 0
    selected = False

    while not selected:
        screen.fill(WHITE)
        for idx, diff in enumerate(difficulties):
            color = GREEN if idx == selected_idx else BLACK
            text = font.render(diff, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3 + idx * 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    selected_idx = (selected_idx - 1) % 3
                elif event.key == pygame.K_s:
                    selected_idx = (selected_idx + 1) % 3
                elif event.key == pygame.K_SPACE:
                    selected = True

        pygame.display.update()
        clock.tick(60)

    return difficulties[selected_idx]

def show_welcome_screen():
    """Display the welcome screen with the game title and press spacebar instruction."""
    welcome = True
    while welcome:
        screen.fill(WHITE)
        
        # Title text
        title_text = font.render("Circle vs Squares:", True, BLACK)
        subtitle_text = font.render("The SHOWDOWN", True, BLACK)
        credit_text = pygame.font.SysFont(None, 24).render("by DheliriouS Artworks", True, BLACK)
        instruction_text = font.render("Press SPACEBAR to continue", True, BLACK)

        # Center the text
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        screen.blit(subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, HEIGHT // 3 + 50))
        screen.blit(credit_text, (WIDTH // 2 - credit_text.get_width() // 2, HEIGHT // 3 + 100))
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 3 + 200))

        pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                welcome = False  # Exit the welcome screen when spacebar is pressed

# Call the welcome screen before the game starts
show_welcome_screen()
# Game loop
running = True
difficulty_selected = False
selected_difficulty = None
in_menu = True  # Added flag to control menu and gameplay switch

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and in_menu:
            # Handle menu input only when in menu mode
            if event.key == pygame.K_w:
                # Code for moving selection up
                pass
            elif event.key == pygame.K_s:
                # Code for moving selection down
                pass
            elif event.key == pygame.K_SPACE:
                selected_difficulty = select_difficulty()
                in_menu = False  # Exit menu, start game

                # Set up the game based on the selected difficulty
                if selected_difficulty == "Easy":
                    WIDTH, HEIGHT = 1000, 600
                elif selected_difficulty == "Normal":
                    WIDTH, HEIGHT = 600, 400
                elif selected_difficulty == "Hard":
                    WIDTH, HEIGHT = 300, 200
                
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                reset_game()  # Reset game state after selecting difficulty
                difficulty_selected = True
                break  # Break out of event loop to avoid continuous menu input

    # Fill the screen with white background
    screen.fill(WHITE)

    # Gameplay starts here after difficulty is selected
    if difficulty_selected and not game_over:
        # Handle player input, movement, and shooting
        handle_input()

        # Handle game logic
        handle_bullets()
        handle_enemies()

        # Spawn enemies at increasing speed
        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_spawn > enemy_spawn_rate:
            spawn_enemy()
            last_enemy_spawn = current_time
            if enemy_spawn_rate > 1000:
                enemy_spawn_rate -= spawn_decrease_rate

        # Draw the player and game elements
        draw_player()

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

    elif game_over:
        # Game over screen
        game_over_text = font.render("You Lost", True, BLACK)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))

        pygame.display.update()
        pygame.time.wait(2000)  # Wait 2 seconds before resetting the game
        reset_game()

    pygame.display.update()
    clock.tick(60)

pygame.quit()

