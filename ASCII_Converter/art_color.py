import numpy as np
import pygame as pg
import cv2
from numba import njit
from loguru import logger as log
import os

image = 'img\\151806_87oel2bil.png'
class ArtConverter:
    # def __init__(self, path = image, font_size=2, color_level = 12):
    #     self.path = path
    #     self.color_level = color_level
    #     pg.init()
        
    #     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #     self.path = os.path.join(BASE_DIR, self.path)
        
    #     # self.ASCII_CHARS = ' .",:!;~+-xmo*#W&8@'
    #     self.ASCII_CHARS = ' ixzao*MW&8%B@$#'
    #     self.font_size = font_size
    #     self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)
    #     self.font = pg.font.SysFont('Consolas', font_size, bold=True)
    #     self.CHAR_STEP = int(font_size * 0.6)
    #     # self.RENDERED_ASCII_CHARS = [
    #     #     self.font.render(char, False, 'white')
    #     #     for char in self.ASCII_CHARS
    #     # ]
    #     #self.rgb_image, self.gray_image = self.get_image()
    #     self.PALETTE, self.COLOR_COEFF = self.create_palette()
    #     self.path = image
    #     #self.image = self.get_image()
    #     #log.debug(self.rgb_image)
    #     self.RES = self.width, self.height = self.rgb_image.shape[0], self.rgb_image.shape[1]
    #     self.screen = pg.display.set_mode(self.RES)
    #     self.clock = pg.time.Clock()
    
    def __init__(self, font_size=2, color_level=18):

        self.color_level = color_level
        pg.init()

        self.ASCII_CHARS = ' ixzao*MW&8%B@$#'
        self.font_size = font_size

        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)

        self.font = pg.font.SysFont('Consolas', font_size, bold=True)

        self.CHAR_STEP = int(font_size * 0.6)
        self.PALETTE, self.COLOR_COEFF = self.create_palette()

        self.path = None

    def draw(self):
        # pg.surfarray.blit_array(self.screen, self.image)
        # cv2.imshow('Window', self.cv2_image)
        self.screen.fill('black')
        self.draw_converted_image()

    def get_image(self, path=None):

        if path is not None:
            self.path = path

        self.cv2_image = cv2.imread(self.path)

        if self.cv2_image is None:
            log.error(f"Не удалось загрузить изображение: {self.path}")
            raise FileNotFoundError(f"Изображение не найдено: {self.path}")

        #transposed_image = cv2.transpose(self.cv2_image)

        self.gray_image = cv2.cvtColor(
            self.cv2_image,
            cv2.COLOR_BGR2GRAY
        )

        self.rgb_image = cv2.cvtColor(
            self.cv2_image,
            cv2.COLOR_BGR2RGB
        )

        self.height, self.width = self.rgb_image.shape[:2]

        self.screen = pg.Surface((self.width, self.height))

        return self.rgb_image, self.gray_image

    def create_palette(self):
        colors, color_coeff = np.linspace(0, 255, num=self.color_level, dtype=int, retstep=True)
        color_palette = [np.array([r, g, b]) for r in colors for g in colors for b in colors]
        palette = dict.fromkeys(self.ASCII_CHARS, None)
        color_coeff = int(color_coeff)
        for char in palette:
            char_palette = {}
            for color in color_palette:
                color_key = tuple(color//color_coeff)
                char_palette[color_key] = self.font.render(char, False, tuple(color))
            palette[char] = char_palette
        return palette, color_coeff

    def draw_converted_image(self):
        char_indices = self.gray_image // self.ASCII_COEFF
        color_indices = self.rgb_image // self.COLOR_COEFF
        # Цикл по пикселям с заданным шагом [cite: 53]
        for x in range(0, self.width, self.CHAR_STEP):
            for y in range(0, self.height, self.CHAR_STEP):
                char_index = char_indices[y, x]
                # Если индекс существует, отрисовываем символ на экране [cite: 55]
                if char_index:
                    char = self.ASCII_CHARS[char_index]
                    color = tuple(color_indices[y, x])
                    self.screen.blit(self.PALETTE[char][color], (x, y))
    
    def save_ascii_art(self, output_path = 'ascii_art.png'):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(
        base_dir,
        "img",
        "ascii_output.png"
        )
        self.screen.fill('black')

        self.draw_converted_image()
        pg.image.save(self.screen, output_path)
        return output_path


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
