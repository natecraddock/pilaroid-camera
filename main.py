import os
import os.path
import pygame
from pygame.locals import *
import RPi.GPIO as GPIO
from time import sleep
import subprocess
import camera
import gallery

import qrcode
import PIL

# Globals
MAX_RESOLUTION = (2592, 1944)
SCREEN_RESOLUTION = (320, 240)
MODE = "camera"
LAST_MODE = None
BUTTONS = [22, 23, 17, 27]


class Icon:
    def __init__(self, path):
        self.name = os.path.splitext(os.path.basename(path))[0]
        print(self.name, end=" ")

        try:
            self.bitmap = pygame.image.load(path)

        except:
            print("Bitmap loading failed")


def load_icons(path):
    print("Loading Icons: ", end="")
    icons = {}
    for icon in os.listdir(path):
        i = Icon(os.path.join(path, icon))
        icons[i.name] = i
    print()
    return icons


def switch_mode(mode):
    global LAST_MODE, MODE

    LAST_MODE = MODE
    MODE = mode


def draw_alpha_rect(screen):
    s = pygame.Surface((32, 240))
    s.set_alpha(100)
    s.fill((173, 41, 105))
    screen.blit(s, (288, 0))


def create_qr_code(url):
    subprocess.call(['qr ' + url + ' > qr.jpg'], shell=True)


# START CAMERA
print("Welcome to Pilaroid")

# Initialize Buttons
GPIO.setmode(GPIO.BCM)
for b in BUTTONS:
    GPIO.setup(b, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Init framebuffer/touchscreen environment variables
print("Initializing Framebuffer")
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
print("Initializing Touchscreen")
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

# Init pygame and screen
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Splash Screen
splash = pygame.image.load("splash.png")
screen.blit(splash, (0, 0))
pygame.display.update()

print("Creating Gallery")
gallery = gallery.Gallery()
camera = camera.Camera(gallery)
icons = load_icons("icons")

# UI
#      mode      events
ui = {"camera":   ["settings", "gallery", "", "capture", "capture"],
      "settings": ["", "", "", "", ""],
      "gallery":  ["back", "share", "left", "right"],
      "share":    ["back", "", "upload", "print"],

      "": []}

# Input is a value 0 - 4, 0-3 are push buttons 22, 23, 17, 27, and 4 is touchscreen
input = -1
event = None

# Main UI loop
while(True):

    # Get input from buttons
    for b in BUTTONS:
        if GPIO.input(b) == False:
            # Only take one press per loop
            print("pressed ", b)
            input = BUTTONS.index(b)
            break


    # Get input from touchscreen
    for e in pygame.event.get():
        if(e.type is MOUSEBUTTONDOWN):
            position = pygame.mouse.get_pos()

            # Only handle input on right border
            if position[0] > 320 - 40:
                if position[1] > 10 and position[1] < 50:
                    input = 0
                elif position[1] > 70 and position[1] < 110:
                    input = 1
                elif position[1] > 130 and position[1] < 170:
                    input = 2
                elif position[1] > 190 and position[1] < 230:
                    input = 3

    # Handle input
    if input is not -1:
        event = ui[MODE][input]

    if MODE == "camera":
        # Handle Events
        if event == "capture":
            # Take a picture! :D
            print("SNAP! :D")
            camera.take_picture()

            """
            screen.blit(pygame.image.load("testing.jpg"), (0, 0))
            pygame.display.update()
            sleep(3)
            """
        elif event == "gallery":
            switch_mode("gallery")
        elif event == "settings":
            pass
        elif event == "gif":
            print("taking GIF")
            camera.take_gif()

        # Load Camera Stream
        img = camera.get_camera_image()

        # Draw Camera on screen
        if img:
            screen.blit(img, ((320 - img.get_width()) / 2, (240 - img.get_height()) / 2))

    elif MODE == "gallery":
        if event == "left":
            gallery.previous_image()
        if event == "right":
            gallery.next_image()
        if event == "back":
            switch_mode("camera")
            continue
        if event == "share":
            switch_mode("share")

        img = pygame.image.load(gallery.get_current_image())
        screen.blit(img, (0, 0))

        # Draw counter
        label = gallery.font.render(gallery.get_counter_text(), 1, (255, 255, 255))
        screen.blit(label, (2, 228))

    elif MODE == "share":
        if event == "print":
            gallery.print_image()
        if event == "back":
            switch_mode(LAST_MODE)
        if event == "upload":
            print("uploading image")
            screen.fill((0, 0, 0))
            label = gallery.font_large.render("Uploading Image...", 1, (255, 255, 255))
            screen.blit(label, ((320 - label.get_width()) / 2, 5))
            pygame.display.update()

            # Upload image
            url = gallery.upload_image(gallery.get_current_image())
            screen.fill((0, 0, 0))
            label = gallery.font_large.render(url, 1, (255, 255, 255))
            screen.blit(label, ((320 - label.get_width()) / 2, 5))
            label = gallery.font_large.render("Touch screen to continue", 1, (255, 255, 255))
            screen.blit(label, (5, 220))
            create_qr_code(url)
            qr = pygame.image.load("qr.jpg")
            qr = pygame.transform.scale(qr, (150, 150))
            screen.blit(qr, (85, 45))

            pygame.display.update()

            # Show the stuff until screen is touched
            running = True
            while running:
                for e in pygame.event.get():
                    if(e.type is MOUSEBUTTONDOWN):
                        running = False

            # Display current image otherwise
            img = pygame.image.load(gallery.get_current_image())
            screen.blit(img, (0, 0))

    # Draw transparent box for iconsd
    draw_alpha_rect(screen)
    # Draw icons over screen based on current mode
    for i, icon_name in enumerate(ui[MODE]):
        if icon_name:
            screen.blit(icons[icon_name].bitmap, (320 - 32, (60 * i) + 14))

    pygame.display.update()

    # Reset input to -1
    input = -1
    event = None
