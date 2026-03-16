import numpy as np
import pygame as pg
import cv2
from numba import njit
from loguru import logger as log

class ArtConverter:
    def __init__(self, path = 'img/151806_87oel2bil.png'):
        self.path = path
        pg.init()
        self.image = self.get_image()
        log.debug(self.image)
        self.RES = self.width, self.height = self.image.shape[0], self.image.shape[1]
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()

    def draw(self):
        pg.surfarray.blit_array(self.screen, self.image)
        cv2.imshow('Window', self.cv2_image)

    def get_image(self):
        self.cv2_image = cv2.imread(self.path)
        transposed_image = cv2.transpose(self.cv2_image)
        image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2GRAY)
        return image

    def draw_converted_image(self):
        char_indices = self.image // self.ASCII_COEFF

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
