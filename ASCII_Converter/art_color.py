import numpy as np
import pygame as pg
import cv2
from numba import njit
from loguru import logger as log

class ArtConverter:
    def __init__(self, path = 'img/151806_87oel2bil.png', font_size=2):
        self.path = path
        pg.init()

        self.ASCII_CHARS = ' .",:!;~+-xmo*#W&8@'
        self.font_size = font_size
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)
        self.font = pg.font.SysFont('Consolas', font_size, bold=True)
        self.CHAR_STEP = int(font_size * 0.6)
        self.RENDERED_ASCII_CHARS = [
            self.font.render(char, False, 'white')
            for char in self.ASCII_CHARS
        ]

        self.image = self.get_image()
        log.debug(self.image)
        self.RES = self.width, self.height = self.image.shape[0], self.image.shape[1]
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()

    def draw(self):
        # pg.surfarray.blit_array(self.screen, self.image)
        # cv2.imshow('Window', self.cv2_image)
        self.screen.fill('black')
        self.draw_converted_image()

    def get_image(self):
        self.cv2_image = cv2.imread(self.path)
        transposed_image = cv2.transpose(self.cv2_image)
        image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2GRAY)
        return image

    def draw_converted_image(self):
        char_indices = self.image // self.ASCII_COEFF
        # Цикл по пикселям с заданным шагом [cite: 53]
        for x in range(0, self.width, self.CHAR_STEP):
            for y in range(0, self.height, self.CHAR_STEP):
                char_index = char_indices[x, y]
                # Если индекс существует, отрисовываем символ на экране [cite: 55]
                if char_index:
                    self.screen.blit(self.RENDERED_ASCII_CHARS[char_index], (x, y))


    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
            self.draw()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick()

if __name__ == '__main__':
    app = ArtConverter()
    app.run()
