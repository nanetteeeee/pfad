import pygame
import random
import os

# initialize pygame
pygame.init()

# Set screen size
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Click the colored dots")

# difine color
colors = [
    (255, 0, 0),  # red
    (0, 255, 0),  # green
    (0, 0, 255),  # blue
    (255, 255, 0),  # yellow
    (255, 0, 255),  # purpose
    (0, 255, 255)   # cyan
]

# Load music file (specify path)
#music_file = "E:\polyu\programming\piano music\piano music.MP3"
music_file = "assignment3\piano music.MP3"
if os.path.exists(music_file):
    pygame.mixer.music.load(music_file)
else:
    print("are you sure")

# Running mark
running = True

# Store a list of dots
dots = []

# Music playing status flag
music_playing = False

# major cycle
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check mouse button status
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:  
        x, y = pygame.mouse.get_pos()
        # Generate more smaller and denser dots
        for _ in range(5):  
            color = random.choice(colors)
            radius = random.randint(2, 9)
            dot_x = x + random.randint(-50, 50)
            dot_y = y + random.randint(-50, 50)
            alpha = 255  # Initial transparency
            dots.append([dot_x, dot_y, color, radius, alpha])
        
        # If the music is not playing, start playing
        if not music_playing:
            pygame.mixer.music.play(-1)
            music_playing = True
        else:
            pygame.mixer.music.unpause()
    else:
        # pause music
        pygame.mixer.music.pause()

    # set black background
    screen.fill((0, 0, 0))

    # Updated dot transparency
    for dot in dots[:]:
        dot[4] -= 0.3 # Reduced transparency per frame, slower speed
        if dot[4] <= 0:
            dots.remove(dot)

    for dot in dots:
        # Create a temporary surface to support transparency
        temp_surface = pygame.Surface((dot[3]*2, dot[3]*2), pygame.SRCALPHA)
        pygame.draw.circle(temp_surface, dot[2] + (dot[4],), (dot[3], dot[3]), dot[3])
        screen.blit(temp_surface, (int(dot[0] - dot[3]), int(dot[1] - dot[3])))

    # Update screen
    pygame.display.flip()

# quit pygame
pygame.quit()