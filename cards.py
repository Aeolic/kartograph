from enum import Enum

import pygame as pg
import pygame.freetype
from pygame.sprite import AbstractGroup

from pygame.surface import Surface

from tiles import forest_tile, water_tile, plains_tile, city_tile, monster_tile

pg.init()

GAME_FONT = pg.freetype.Font("gol.otf", 24)

CARD_WIDTH = 6 * 64
CARD_HEIGHT = 9 * 64

coin = pg.image.load("img/coin.png")


class ElmntType(Enum):
    forest = forest_tile
    water = water_tile
    plains = plains_tile
    city = city_tile
    monster = monster_tile


class Shape(Enum):
    gehoeft = [[0, 1, 0],
               [1, 1, 1]]
    ackerland_1 = [[1, 1]]
    ackerland_2 = [[0, 1, 0],
                   [1, 1, 1],
                   [0, 1, 0]]
    splitterland = [[1]]
    baumwipfel = [[0, 0, 1, 1],
                  [1, 1, 1, 0]]
    hinterland = [[1, 1, 1],
                  [0, 0, 1],
                  [0, 0, 1]]

    weiler_1 = [[1, 0],
                [1, 1]]
    weiler_2 = [[1, 1, 1],
                [1, 1, 0]]
    obsthain = [[1, 1, 1],
                [0, 0, 1]]
    strom_1 = [[1, 1, 1]]
    strom_2 = [[0, 0, 1],
               [0, 1, 1],
               [1, 1, 0]]
    wald_1 = [[1, 0],
              [0, 1]]
    wald_2 = [[0, 1, 1],
              [1, 1, 0]]

    sumpf = [[1, 1, 1],
             [0, 1, 0],
             [0, 1, 0]]
    fischerdorf = [[1, 1, 1, 1]]

    gnollangriff = [[1, 1, 1],
                    [1, 0, 1]]
    goblinattacke = [[1, 0, 0],
                     [0, 1, 0],
                     [0, 0, 1]]
    koboldansturm = [[1, 1, 1],
                     [0, 1, 0]]
    grottenschratueberfall = [[1, 0, 1],
                              [1, 0, 1]]


class DrawableElement(pg.sprite.Sprite):

    def __init__(self, elmnt_type: ElmntType, shape, gives_gold=False, *groups: AbstractGroup):
        super().__init__(*groups)
        self.elmnt_type = elmnt_type.value
        self.shape = shape.value

        self.gives_gold = gives_gold

        self.setup()

    def update(self):
        """move the fist based on the mouse position"""

        self.setup()
        self.drawElements()
        pos = pg.mouse.get_pos()
        self.rect.topleft = pos

    def setup(self):
        self.width = len(self.shape[0]) * 64
        self.height = len(self.shape) * 64
        self.image = Surface((self.width, self.height), pg.SRCALPHA, 32)
        self.rect = self.image.get_rect()

    def drawElements(self, offset_x=0, offset_y=0):
        for row in range(len(self.shape)):
            for column in range(len(self.shape[row])):
                if self.shape[row][column] == 1:
                    self.image.blit(self.elmnt_type.draw(),
                                    (column * 64 + offset_x, row * 64 + offset_y))

        return self.image


class Card:

    def __init__(self, name, types, shapes, value, is_monster=False):
        self.name = name
        self.types = types
        self.shapes = shapes

        self.area1 = None
        self.area2 = None

        self.ele1 = None
        self.ele2 = None
        self.value = value
        self.needs_ruins = False

        self.is_monster = is_monster

        self.surface = Surface((CARD_WIDTH, CARD_HEIGHT))

        self.draw_text()

        if not self.is_monster:

            # one elmnt_type, 2 shapes
            if len(self.types) == 1:

                self.ele1 = DrawableElement(self.types[0], self.shapes[0], True)
                self.ele2 = DrawableElement(self.types[0], self.shapes[1])
                self.ele1_gives_gold = True


            # two types, 1 shape
            else:

                self.ele1 = DrawableElement(self.types[0], self.shapes[0])
                self.ele2 = DrawableElement(self.types[1], self.shapes[0])
                self.ele1_gives_gold = False

            self.area1 = (28, 76, self.ele1.width + 8, self.ele1.height + 8)
            self.area2 = (28, 76 + 64 + self.ele1.height, self.ele2.width + 8, self.ele2.height + 8)

            pg.draw.rect(self.surface, (0, 0, 0), self.area1, 2)
            pg.draw.rect(self.surface, (0, 0, 0), self.area2, 2)

            self.surface.blit(self.ele1.drawElements(), (32, 80))
            self.surface.blit(self.ele2.drawElements(), (32, 80 + 64 + self.ele1.height))

            if self.ele1_gives_gold:
                self.surface.blit(coin, (self.ele1.width, 76 + 8))

        if self.is_monster:  # TODO needs a lot of refactoring/ separate monster class
            self.ele1 = DrawableElement(self.types[0], self.shapes[0])
            self.area1 = (28, 76, self.ele1.width + 8, self.ele1.height + 8)
            pg.draw.rect(self.surface, (0, 0, 0), self.area1, 2)
            self.surface.blit(self.ele1.drawElements(), (32, 80))

    def draw(self):
        return self.surface

    def draw_text(self):
        self.surface.fill((96, 50, 40))
        GAME_FONT.render_to(self.surface, (32, 32), self.name, (200, 200, 100))
        GAME_FONT.size = 36
        GAME_FONT.render_to(self.surface, (CARD_WIDTH - 48, 32), str(self.value), (200, 200, 100))
        GAME_FONT.size = 24


class Splitterland(Card):

    def draw(self):
        self.draw_text()

        self.ele1 = [DrawableElement(x, self.shapes[0]) for x in self.types]

        marker = 64 + 8

        outline_values = [(32, 80), (128, 80), (32, 176), (128, 176), (32, 272)]
        self.area1 = [(x[0] - 4, x[1] - 4, marker, marker) for x in outline_values]

        for outline in self.area1:
            pg.draw.rect(self.surface, (0, 0, 0), outline, 2)

        self.surface.blit(self.ele1[0].drawElements(), (32, 80))
        self.surface.blit(self.ele1[1].drawElements(), (128, 80))
        self.surface.blit(self.ele1[2].drawElements(), (32, 176))
        self.surface.blit(self.ele1[3].drawElements(), (128, 176))
        self.surface.blit(self.ele1[4].drawElements(), (32, 272))
        return self.surface
