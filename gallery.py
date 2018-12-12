import os
import pygame
import json
import requests
from base64 import b64encode

import printer


class Gallery:
    def __init__(self):
        self.NUM_PLACES = 5
        self.output_folder = "images"

        self.printer = printer.Printer()

        # Initialize counter
        max = 0
        for i in os.listdir(self.output_folder):
            number = int(os.path.splitext(i)[0].split('_')[1])
            if number > max:
                max = number
        self.counter = max + 1
        print("Starting counter at:", self.counter)

        # Gallery Information
        self.current_image = self.counter - 1
        self.font = pygame.font.SysFont("monospace", 12)
        self.font_large = pygame.font.SysFont("monospace", 14)
        print("current image:", self.current_image)

    def _get_filename(self, number):
        for f in os.listdir(self.output_folder):
            if str(number).zfill(self.NUM_PLACES) in f:
                return os.path.join(self.output_folder, f)

    def get_next_filename(self):
        return os.path.join(self.output_folder, "IMG_" + str(self.counter).zfill(self.NUM_PLACES))

    # This is not zero-indexed
    def get_counter_text(self):
        return str(self.current_image + 1).zfill(self.NUM_PLACES) + "/" + str(self.get_num_images()).zfill(self.NUM_PLACES)

    def get_num_images(self):
        return len(os.listdir(self.output_folder))

    def get_current_image(self):
        return self._get_filename(self.current_image)

    def next_image(self):
        # We are trying to go to past the last image, wrap
        if (self.current_image + 1) is self.counter:
            self.current_image = 0
        else:
            self.current_image += 1

    def previous_image(self):
        # if we are trying to load an image that doesn't exist
        if (self.current_image - 1) is -1:
            self.current_image = self.counter - 1
        else:
            self.current_image -= 1

    def print_image(self):
        self.printer.print_image(self.get_current_image())

    def upload_image(self, image):
        url = "https://api.imgur.com/3/image"

        payload = {
                'image': b64encode(open(image, 'rb').read()),
                'type': 'base64',
                'name': image,
                'title': 'test'
            }
        headers = {
            'Authorization': "Client-ID d802bc96572640e"
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        url = json.loads(response.text)['data']['link']
        return url
