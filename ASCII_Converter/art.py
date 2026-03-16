import pygame as pg

class Art:
    def __init__(self, path = 'img/151806_87oel2bil.png', font_size = 12):
        self.ASCII_CHARS = ' .",:!;~+-xmo*#W&8@'
        self.font_size = font_size
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)
        self.font = pg.font.SysFont('Consolas', font_size, bold=True)
        self.CHAR_STEP = int(font_size * 0.6)
        self.RENDERED_ASCII_CHARS = [self.font.render(char, False, 'white') for char in self.ASCII_CHARS]