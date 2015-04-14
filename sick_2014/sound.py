"""
A basic tools for sound playing.
"""

import pygame
import sys

pygame.mixer.init()

def raspySound( soundFile = "sound/Track03.wav" ):
    pygame.mixer.music.load("sound/Track03.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print __doc__
        sys.exit()
    soundFile = sys.argv[1]
    raspySound(soundFile)