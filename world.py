from settings import *
import pygame as pg


class Platform(pg.sprite.Sprite):
    def __init__(self,image, x, y, width, height):
        super(Platform, self).__init__()

        self.image = pg.transform.scale(image, (width * TILE_SCALE, height * TILE_SCALE))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE



class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.load_animation()
        self.image = self.images[0]
        self.rect = self.image.get_rect(x=x, y=y)

        self.current_image = 0

        self.timer = pg.time.get_ticks()
        self.interval = 200

    def load_animation(self):
        tile_size = 16
        tile_scale = 4

        num_images = 5
        self.images = []
        spritesheet = pg.image.load('sprite/coins/MonedaD.png')

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            self.images.append(image)
    
    def update(self):
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.images):
                self.current_image = 0
            self.image = self.images[self.current_image]
            self.timer = pg.time.get_ticks()


class Portal(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.load_animation()
        self.image = self.images[0]
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(x=x, y=y)

        self.current_image = 0

        self.timer = pg.time.get_ticks()
        self.interval = 100

    def load_animation(self):
        tile_size = 64
        tile_scale = 4

        num_images = 8
        self.images = []
        spritesheet = pg.image.load('sprite/Purple Portal Sprite Sheet.png').convert_alpha()

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            image = pg.transform.flip(image, False, True)
            self.images.append(image)
    
    def update(self):
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.images):
                self.current_image = 0
            self.image = self.images[self.current_image]
            self.timer = pg.time.get_ticks()

