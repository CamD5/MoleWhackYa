import pygame
import serial
import time
import random
from pygame import mixer

# Initialize Pygame
pygame.init()
mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pico Whack-a-Mole")

# Serial connection to Pico
ser = serial.Serial('COM8', 115200)  # Cameron's is COM8. It may be different for everyone

# Game variables
score = 0
game_time = 60
current_time = game_time
game_active = False
mole_visible = False

# Colors and fonts (same as before)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
title_font = pygame.font.SysFont('Arial', 60)
button_font = pygame.font.SysFont('Arial', 30)

def send_to_pico(command):
    ser.write(f"{command}\n".encode())
    return ser.readline().decode().strip()  # Wait for response

def raise_mole():
    send_to_pico("RAISE")
    
def lower_mole():
    send_to_pico("LOWER")

def check_hammer_hit():
    send_to_pico("CHECK_HIT")
    return "HIT" in ser.readline().decode()

# ... [Rest of your Pygame code (home screen, buttons, etc.)] ...

# In your game loop:
while True:
    if game_active:
        # Check for physical hits
        if check_hammer_hit():
            if mole_visible:
                score += 10
                lower_mole()
                mole_visible = False
        
        # Randomly show mole
        if not mole_visible and random.random() < 0.02:
            raise_mole()
            mole_visible = True
            mole_timer = time.time()
