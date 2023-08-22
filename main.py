import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700

# Colors
WHITE = (255, 255, 255)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Angry Birds Showdown")

# Load bird images
player_bird_image = pygame.image.load("angry_bird_pygame/player_bird1.png")  # Replace with actual image
enemy_bird_image = pygame.image.load("angry_bird_pygame/enemy_bird1.png")    # Replace with actual image

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = [0, 0]
        self.dragging = False
        self.drag_start_pos = (0, 0)

    def update(self):
        if self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.centerx = mouse_pos[0]
            self.rect.centery = mouse_pos[1]
        else:
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]

    def start_drag(self):
        self.dragging = True
        self.drag_start_pos = self.rect.center

    def end_drag(self):
        self.dragging = False
        mouse_pos = pygame.mouse.get_pos()
        direction = math.atan2(self.drag_start_pos[1] - mouse_pos[1], self.drag_start_pos[0] - mouse_pos[0])
        speed = 10
        self.velocity = [speed * math.cos(direction), speed * math.sin(direction)]

# Button class
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, action):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.action = action

# Create player bird
player_bird = Bird(100, SCREEN_HEIGHT // 2, player_bird_image)

# Create enemy birds
enemy_birds = pygame.sprite.Group()
for _ in range(5):
    x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 50)
    y = random.randint(50, SCREEN_HEIGHT - 50)
    enemy_bird = Bird(x, y, enemy_bird_image)
    enemy_birds.add(enemy_bird)

# ... (Button and game loop code remains the same)
# Calculate button positions (top left corner)
button_margin = 10
button_top = button_margin
button_left = button_margin
button_spacing = 5

# Create buttons
quit_button_image = pygame.image.load("angry_bird_pygame/quit_button.png")        # Replace with actual image
refresh_button_image = pygame.image.load("angry_bird_pygame/refresh_button.png")  # Replace with actual image

quit_button = Button(button_left, button_top, quit_button_image, "quit")
refresh_button = Button(button_left + quit_button_image.get_width() + button_spacing, button_top, refresh_button_image, "refresh")

# Game loop
clock = pygame.time.Clock()

# Initialize game state
try_again_counter = 0
max_try_again = 3

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button.rect.collidepoint(event.pos):
                # Quit button clicked - exit the game
                pygame.quit()
                sys.exit()

            elif refresh_button.rect.collidepoint(event.pos):
                # Refresh button clicked - reset game
                player_bird.rect.center = (100, SCREEN_HEIGHT // 2)  # Reset player bird position
                player_bird.velocity = [0, 0]

                enemy_birds.empty()
                for _ in range(5):
                    x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 50)
                    y = random.randint(50, SCREEN_HEIGHT - 50)
                    enemy_bird = Bird(x, y, enemy_bird_image)
                    enemy_birds.add(enemy_bird)

            elif player_bird.rect.collidepoint(event.pos):
                # Player bird clicked - start dragging
                player_bird.start_drag()

        elif event.type == pygame.MOUSEBUTTONUP:
            if player_bird.dragging:
                # Release the player bird
                player_bird.end_drag()
            else:
                break

    # Update enemy bird positions and collisions
    hits = pygame.sprite.spritecollide(player_bird, enemy_birds, True)
    if hits:
        try_again_counter = 0
    else:
        try_again_counter += 1

    if len(enemy_birds) == 0:
        try_again_counter = 0

    if try_again_counter >= max_try_again:
        try_again_counter = 0

    # Reset player bird to origin position if it goes out of the screen
    if player_bird.rect.left > SCREEN_WIDTH or player_bird.rect.right < 0 or \
            player_bird.rect.top > SCREEN_HEIGHT or player_bird.rect.bottom < 0:
        player_bird.rect.center = (100, SCREEN_HEIGHT // 2)
        player_bird.velocity = [0, 0]

    # Clear the screen
    screen.fill(WHITE)

    # Update and draw player bird
    player_bird.update()
    screen.blit(player_bird.image, player_bird.rect)

    # Update and draw enemy birds
    enemy_birds.update()
    enemy_birds.draw(screen)

    # Draw buttons
    screen.blit(quit_button.image, quit_button.rect)
    screen.blit(refresh_button.image, refresh_button.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


