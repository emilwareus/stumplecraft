import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Shark Navigator')

# Load the shark images
shark_open_o = pygame.image.load('assets/shark1_o.png')
shark_close_o = pygame.image.load('assets/shark1_c.png')
fish_images = [
    pygame.image.load('assets/fish1.png'),
    pygame.image.load('assets/fish2.png'),
    pygame.image.load('assets/fish3.png')
]
mega_image = pygame.image.load('assets/mega.png')

# Scale the images to the new size, for example, 50x50 pixels
new_size = (50, 50)
max_shark_size = (120, 120)
mega_size = (400, 400)
shark_open = pygame.transform.scale(shark_open_o, new_size)
shark_close = pygame.transform.scale(shark_close_o, new_size)
fish_images = [
    pygame.transform.scale(f, new_size) for f in fish_images
]
mega_image = pygame.transform.scale(mega_image, mega_size)

# Set the current shark image
current_shark = shark_open

# Get rect of the shark image for positioning
shark_rect = current_shark.get_rect()

# Start the shark in the middle of the screen
shark_rect.x = screen_width // 2
shark_rect.y = screen_height // 2

shark_speed = 5  # How many pixels the shark moves per frame

# Time tracking for image switch
switch_time = 1000  # milliseconds
last_switch = pygame.time.get_ticks()

# RGB color for water blue
background_color = (94, 196, 255)

# Fish properties
fish_list = []
fish_spawn_time = 2000  # milliseconds
last_fish_spawn = pygame.time.get_ticks()
fish_speeds = [2, 4, 6]  # slow, medium, fast speeds

# Megaledon properties
current_mega_image = None
mega_speed = 1
mega_spawn_points = 30
mega_direction = 1
mega_x = 0
mega_y = 0
mega_collided = False

# Define growth factors
shark_growth_factor = 1.02  # The shark grows by 10% of its current size
shark_slowdown_factor = 1  # The shark's speed is reduced by 5%

# Score
score = 0
score_font = pygame.font.SysFont('Arial', 24)  # Choose an appropriate font and size

# Main game loop
running = True
while running:

    ## Fish Spawning logic
    current_time = pygame.time.get_ticks()

    # Spawn a new fish at a random time
    if current_time - last_fish_spawn >= fish_spawn_time:
        fish_image = random.choice(fish_images)
        fish_speed = random.choice(fish_speeds)
        fish_direction = random.choice([-1, 1])  # -1 for left, 1 for right
        
        # if left, flip the fish
        if fish_direction == 1: 
            fish_image = pygame.transform.flip(fish_image, True, False)

        fish_x = 0 if fish_direction == 1 else screen_width
        fish_y = random.randint(0, screen_height - fish_image.get_height())
        fish_list.append({'image': fish_image, 'x': fish_x, 'y': fish_y, 'speed': fish_speed * fish_direction})
        last_fish_spawn = current_time
        fish_spawn_time = random.randint(1000, 3000)  # randomize time for next fish


    ## Shark logic 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get pressed keys to determine movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        shark_rect.x -= shark_speed
    if keys[pygame.K_RIGHT]:
        shark_rect.x += shark_speed
    if keys[pygame.K_UP]:
        shark_rect.y -= shark_speed
    if keys[pygame.K_DOWN]:
        shark_rect.y += shark_speed

    # Keep the shark on the screen
    shark_rect.x = max(0, min(shark_rect.x, screen_width - shark_rect.width))
    shark_rect.y = max(0, min(shark_rect.y, screen_height - shark_rect.height))

    # Check if it's time to switch the image
    current_time = pygame.time.get_ticks()
    if current_time - last_switch >= switch_time:
        current_shark = shark_open if current_shark == shark_close else shark_close
        last_switch = current_time

    # Set the background color
    screen.fill(background_color)

    # Move and draw each fish and check for collisions
    for fish in fish_list[:]:
        fish['x'] += fish['speed']
        fish_rect = fish['image'].get_rect(topleft=(fish['x'], fish['y']))
        if shark_rect.colliderect(fish_rect):
            # Shark eats the fish
            fish_list.remove(fish)

            # Increase points
            score += 10
            if score % mega_spawn_points== 0:
                mega_collided = False
                current_mega_image = mega_image
                mega_direction = random.choice([-1, 1])  
                if mega_direction == -1: 
                    current_mega_image = pygame.transform.flip(current_mega_image, True, False)
                mega_x = -mega_size[0] if mega_direction == 1 else screen_width
                mega_y = random.randint(0, screen_height - mega_image.get_height())

            # Shark grows in size
            shark_size = (min(int(shark_rect.width * shark_growth_factor), 100), min(int(shark_rect.height * shark_growth_factor), 100))
            shark_open = pygame.transform.scale(shark_open_o, shark_size)
            shark_close = pygame.transform.scale(shark_close_o, shark_size)
            
            # Shark becomes slower
            shark_speed *= shark_slowdown_factor
            
            # Update the current shark image and rectangle
            current_shark = shark_open
            shark_rect = current_shark.get_rect(center=shark_rect.center)
        else:
            # Draw fish if it's not eaten
            screen.blit(fish['image'], fish_rect.topleft)

    if current_mega_image:
        mega_x += mega_speed * mega_direction
        mega_react = current_mega_image.get_rect(topleft=(mega_x, mega_y))
        
        if shark_rect.colliderect(mega_react) and not mega_collided:
            score -= 50
            mega_collided = True
        elif not shark_rect.colliderect(mega_react) and mega_collided:
            mega_collided = False
        
        screen.blit(current_mega_image, mega_react.topleft)    
        


    # Draw the current shark image
    screen.blit(current_shark, shark_rect)

    # Display the score
    score_text = score_font.render(f'Score: {score}', True, (255, 255, 255))  # White text for score
    screen.blit(score_text, (10, 10))  # Position the score in the top-left corner

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit the game
pygame.quit()
sys.exit()
