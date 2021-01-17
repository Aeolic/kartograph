import pygame as pg

pg.init()


class Tile():

    def __init__(self, name, img_path):
        self.name = name
        self.img = pg.transform.scale(pg.image.load(img_path), (64, 64))

    def draw(self):
        return self.img


empty_tile = Tile("Empty", "img/base_tile.png")
mntn_tile = Tile("Mountain", "img/mnt_tile.png")
ruins_tile = Tile("Ruins", "img/ruins_tile.png")
error_tile = Tile("Error", "img/error_tile.png")

forest_tile = Tile("Forest", "img/forest_tile.png")
water_tile = Tile("Water", "img/water_tile.png")
plains_tile = Tile("Plains", "img/plains_tile.png")
city_tile = Tile("City", "img/house_tile.png")
monster_tile = Tile("Monster", "img/monster_tile.png")