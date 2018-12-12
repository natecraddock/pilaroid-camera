# pilaroid-camera
A raspberry pi Polaroid camera

## Parts
- [Adafruit PiTFT 3.2" Touchscreen](https://www.adafruit.com/product/2616)
- [Nano Thermal Printer](https://www.adafruit.com/product/2752)
- [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
- [Raspberry Pi Camera v2.1](https://www.raspberrypi.org/products/camera-module-v2/)

## Requirements / Setup
- [Setup PiTFT Screen](https://learn.adafruit.com/adafruit-pitft-28-inch-resistive-touchscreen-display-raspberry-pi)
  - Set up the screen to boot to console, the camera interface is written to the framebuffer in pygame
- [Setup Thermal Printer](https://learn.adafruit.com/networked-thermal-printer-using-cups-and-raspberry-pi)
- Python Modules
  - [qrcode](https://pypi.org/project/qrcode/)
  - [img2pdf](https://pypi.org/project/img2pdf/)

## Running
Due to the pygame framebuffer requirements, the python script must be run as `sudo`

Run `sudo python3 main.py` from the project directory to start the camera. After about 10-15 seconds the camera splash screen will show followed by the camera software
