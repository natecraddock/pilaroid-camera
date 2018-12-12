import atexit
import io
import os
import os.path
import picamera
import pygame
import yuv2rgb
from pygame.locals import *
from time import sleep
import subprocess


class Camera:
    def __init__(self, gallery):
        self.MAX_RESOLUTION = (2592, 1944)
        self.SCREEN_RESOLUTION = (320, 240)
        self.camera = picamera.PiCamera()
        self.camera.resolution = self.SCREEN_RESOLUTION
        self.camera.rotation = 90

        # Makes sure the camera closes cleanly on exit
        atexit.register(self.camera.close)

        self.gallery = gallery

        self.temp = "temp"

    def take_picture(self):
        filename = self.gallery.get_next_filename() + ".jpg"
        print("Writing", filename)
        #self.camera.resolution = self.MAX_RESOLUTION
        self.camera.capture(filename)
        # The user will probably want to preview the most recent picture
        # Reset the current image of the Gallery
        self.gallery.current_image = self.gallery.counter
        self.gallery.counter += 1
        #self.camera.resolution = self.SCREEN_RESOLUTION

    # Create a 3 seocnd GIF image
    def take_gif(self):
        filename = self.gallery.get_next_filename() + ".gif"
        for f in os.listdir(self.temp):
            os.remove(os.path.join(self.temp, f))

        self.camera.resolution = self.SCREEN_RESOLUTION
        print("Creating GIF")

        for i in range(20):
            self.camera.capture(os.path.join(self.temp, (str(i).zfill(2) + '.jpg')), use_video_port=True)

        # Now write GIF to file path
        subprocess.call(["convert", "temp/*", filename])


    # Returns an RGB image suitible for use in pygame
    def get_camera_image(self):
        rgb = bytearray(320 * 240 * 3)
        yuv = bytearray(int(320 * 240 * 3 / 2))

        stream = io.BytesIO()  # Capture into in-memory stream
        self.camera.capture(stream, use_video_port=True, format='raw')
        stream.seek(0)
        stream.readinto(yuv)  # stream -> YUV buffer
        stream.close()
        yuv2rgb.convert(yuv, rgb, self.SCREEN_RESOLUTION[0], self.SCREEN_RESOLUTION[1])

        img = pygame.image.frombuffer(rgb[0:(self.SCREEN_RESOLUTION[0] * self.SCREEN_RESOLUTION[1] * 3)], self.SCREEN_RESOLUTION, 'RGB')
        return img
