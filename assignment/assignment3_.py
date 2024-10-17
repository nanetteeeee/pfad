import pygame
import pyaudio
import numpy as np
import random

# Initialize pygame
pygame.init()

# Set screen size
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Click the colored dots and play random music")

# define color
colors = [
    (255, 0, 0),  # red
    (0, 255, 0),  # green
    (0, 0, 255),  # blue
    (255, 255, 0),  # yellow
    (255, 0, 255),  # purpose
    (0, 255, 255),   # cyan
    (255, 192, 203) #pink
]

# Initialize pyaudio
p = pyaudio.PyAudio()

# A function that generates sound
def generate_sound(frequency, duration=0.5, volume=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    # Generates a sinusoidal waveform
    tone = np.sin(frequency * t * 2 * np.pi)

    # Adjust the volume
    audio = tone * volume

    # Convert to 16-bit PCM format
    audio = np.int16(audio * 32767)

    # Create a stream and play the sound
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, output=True)
    stream.write(audio.tobytes())
    stream.stop_stream()
    stream.close()

# Running mark
running = True

# Main cycle
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get click position
            x, y = event.pos
            
            # Randomly generate the color and size of the circle
            color = random.choice(colors)
            radius = random.randint(10, 50)
            
            # Dot drawing
            pygame.draw.circle(screen, color, (x, y), radius)
            
            # Generate random frequency sounds (between 200Hz and 1000Hz)
            frequency = random.randint(200, 1000)
            generate_sound(frequency)

    # Update screen
    pygame.display.flip()

# quit pygame
pygame.quit()

# end pyaudio
p.terminate()