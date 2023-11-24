# Tim Lauber
# L2 Electron Design

import serial
import time

class l2_christmas_tree:
    def __init__(self, com, verbose=True):
        # Constructor
        # com: COM port string
        self.com = com
        self.verbose = verbose
        self.state = [[0,0,0,0]]*24

    def connect(self):
        # Connect to device
        self.ser = serial.Serial(
            baudrate = 9600,
            port = self.com
        )
        if self.verbose: print('Connected!')

    def trigger_leds(self):
        # Turns LEDs On/Off
        self.ser.write(b't\n')

    def choose_picture(self, picture_index = 0):
        # Chooses a picture.
        # picture_index: between 0 and 15
        if picture_index < 16:
            string_to_send = 'p' + str(picture_index).zfill(2) + '\n'
            self.ser.write(string_to_send.encode('utf-8'))
            if self.verbose: print(f'Picture changed to index {picture_index}!')
        else:
            if self.verbose: print(f'Choose an index within 0 to 15 bounds.')

    def set_pixel(self, pixel_index, r, g, b, w):
        # Set a specific pixel in the custom picture
        # pixel_index: pixel to set. Between 0 and 23
        # r: red, 0-255
        # g: green, 0-255
        # b: blue, 0-255
        # w: white, 0-255
        if (self.state[pixel_index][0] != r) or (self.state[pixel_index][1] != g) or (self.state[pixel_index][2] != b) or (self.state[pixel_index][3] != w):
            if (pixel_index < 24) and (r < 256) and (g < 256) and (b < 256) and (w < 256):
                string_to_send = 'c' + str(pixel_index).zfill(2) + str(r).zfill(3) + str(g).zfill(3) + str(b).zfill(3) + str(w).zfill(3) + '\n'
                self.ser.write(string_to_send.encode('utf-8'))
                self.state[pixel_index] = [r, g, b, w]
                if self.verbose: print(f'Pixel {pixel_index} changed to r = {r}, g = {g}, b = {b}, w = {w}!')
            else:
                if self.verbose: print(f'Either the pixel index or one of the colors was out of range!')
        else:
            if self.verbose: print('This pixel was already set to this color. No new data has been sent!')

    def set_pixel_array(self, pixel_array):
        # Send array of data.
        # pixel_array: All the pixels that should be set. Can also be a subset of all pixels. Format should be [index, r, g, b, w]
        for pixel in pixel_array:
            self.set_pixel(pixel[0], pixel[1], pixel[2], pixel[3], pixel[4])

    def save(self):
        # Save current picture to EEPROM
        self.ser.write(b'v\n')

    def close(self):
        # Closes COM port. Always use at the end of script!
        self.ser.close()