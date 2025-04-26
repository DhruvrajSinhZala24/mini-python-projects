import pygame
import random
import sys
import os

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (50, 150, 255)
LIGHT_BLUE = (135, 206, 235)
PIPE_COLOR = (34, 177, 76)
BIRD_COLOR = (255, 223, 0)
TEXT_COLOR = (255, 255, 255)
GREEN = (34, 177, 76)

# Clock and Font
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32, bold=True)
large_font = pygame.font.SysFont("Arial", 48, bold=True)

# Load Sounds
def load_sound(filename):
    try:
        return pygame.mixer.Sound(os.path.join(filename))
    except pygame.error:
        print(f"Warning: Couldn't load sound: {filename}")
        return None

jump_sound = load_sound("jump.mp3")
hit_sound = load_sound("hit.mp3")
score_sound = load_sound("score.mp3")

# Bird image and properties
bird_img = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.circle(bird_img, BIRD_COLOR, (20, 20), 20)
bird_rect = bird_img.get_rect(center=(100, HEIGHT // 2))
bird_velocity = 0
gravity = 0.5
jump_strength = -10

# Pipes
pipe_width = 80
pipe_gap = 200
pipe_velocity = -5
pipes = []

# Clouds
clouds = []

# Game state
score = 0
best_score = 0
scored_pipes = []
game_active = False
background_scroll = 0
cloud_scroll = 0

# Particle system
particles = []

# Load best score 
if os.path.exists("highscore.txt"):
    with open("highscore.txt") as f:
        best_score = int(f.read())

def create_pipe():
    height = random.randint(150, 450)
    top = pygame.Rect(WIDTH, 0, pipe_width, height - pipe_gap // 2)
    bottom = pygame.Rect(WIDTH, height + pipe_gap // 2, pipe_width, HEIGHT)
    return top, bottom

def move_pipes(pipes):
    for pipe in pipes:
        pipe.x += pipe_velocity
    return [pipe for pipe in pipes if pipe.right > 0]

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            if hit_sound: hit_sound.play()
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        if hit_sound: hit_sound.play()
        return False
    return True

def display_score(score, best_score):
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    best_score_text = font.render(f"Best: {best_score}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))
    screen.blit(best_score_text, (WIDTH - best_score_text.get_width() - 10, 10))

def spawn_particles(x, y):
    for _ in range(5):
        particles.append([[x, y], [random.uniform(-1, 1), random.uniform(-2, 0)], random.randint(2, 4)])

def update_particles():
    for particle in particles[:]:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        if particle[2] <= 0:
            particles.remove(particle)
        else:
            pygame.draw.circle(screen, BLACK, (int(particle[0][0]), int(particle[0][1])), int(particle[2]))

def create_cloud():
    cloud_width = random.randint(100, 200)
    cloud_height = random.randint(50, 100)
    cloud_x = WIDTH
    cloud_y = random.randint(50, 150)
    return pygame.Rect(cloud_x, cloud_y, cloud_width, cloud_height)

def move_clouds(clouds):
    for cloud in clouds:
        cloud.x -= 1
    return [cloud for cloud in clouds if cloud.right > 0]

def show_game_over_screen(score, best_score):
    game_over_text = large_font.render("Flappy Bird", True, TEXT_COLOR)
    restart_text = font.render("Press Space to Start", True, TEXT_COLOR)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
    display_score(score, best_score)

# Game timer
pipe_timer = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save high score on exit
            with open("highscore.txt", "w") as f:
                f.write(str(best_score))
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active:
                    game_active = True
                    bird_rect.center = (100, HEIGHT // 2)
                    bird_velocity = 0
                    pipes.clear()
                    clouds.clear()
                    scored_pipes.clear()
                    score = 0
                    spawn_particles(bird_rect.centerx, bird_rect.centery)
                else:
                    bird_velocity = jump_strength
                    spawn_particles(bird_rect.centerx, bird_rect.centery)
                    if jump_sound: jump_sound.play()

            if event.key == pygame.K_r and not game_active:
                bird_rect.center = (100, HEIGHT // 2)
                bird_velocity = 0
                pipes.clear()
                clouds.clear()
                scored_pipes.clear()
                score = 0
                game_active = True

        if event.type == pipe_timer and game_active:
            pipes.extend(create_pipe())

    # Scroll background
    background_scroll -= 1
    if background_scroll <= -WIDTH:
        background_scroll = 0

    cloud_scroll -= 0.5
    if cloud_scroll <= -200:
        cloud_scroll = 0
        clouds.append(create_cloud())

    # Draw background
    screen.fill(LIGHT_BLUE)
    for cloud in clouds:
        pygame.draw.ellipse(screen, WHITE, cloud)
    clouds = move_clouds(clouds)

    if game_active:
        bird_velocity += gravity
        bird_rect.y += int(bird_velocity)

        # Draw bird shadow
        shadow = bird_img.copy()
        shadow.fill((0, 0, 0, 50), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(shadow, (bird_rect.x + 5, bird_rect.y + 5))
        screen.blit(bird_img, bird_rect)

        pipes = move_pipes(pipes)
        for pipe in pipes:
            pygame.draw.rect(screen, PIPE_COLOR, pipe)

        if not check_collision(pipes):
            game_active = False
            # Save high score
            if score > best_score:
                best_score = score
                with open("highscore.txt", "w") as f:
                    f.write(str(best_score))

        # Scoring logic
        for i in range(0, len(pipes), 2):  # Step through top-bottom pairs
            top_pipe = pipes[i]
            if top_pipe.centerx < bird_rect.centerx and top_pipe not in scored_pipes:
                score += 1
                scored_pipes.append(top_pipe)
                if score_sound: score_sound.play()


        display_score(score, best_score)
        update_particles()
    else:
        show_game_over_screen(score, best_score)

    pygame.display.update()
    clock.tick(60)