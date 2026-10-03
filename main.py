import pygame as pg
import pytmx
import json
from settings import *
from player import Player, Ball
from enemy import Enemy
from world import Coin, Platform, Portal


pg.init()

font = pg.font.Font(None, 36)


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Платформер")
        self.level = 1


        self.setup()

    def setup(self):
        self.mode = 'game'
        self.clock = pg.time.Clock()
        self.is_running = False

        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.balls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.portals = pg.sprite.Group()

        self.tmx_map = pytmx.load_pygame(f"maps/tileset/level{self.level}.tmx")
        
        self.map_pixel_width = self.tmx_map.width * self.tmx_map.tilewidth * TILE_SCALE
        self.map_pixel_height = self.tmx_map.height * self.tmx_map.tileheight * TILE_SCALE

        self.player = Player(self.map_pixel_width, self.map_pixel_height)
        self.all_sprites.add(self.player)

        


        for layer in self.tmx_map:
            if layer.name == 'platforms':
                for x, y, gid in layer:
                    tile = self.tmx_map.get_tile_image_by_gid(gid)

                    if tile:
                        platform = Platform(tile, x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight,
                                            self.tmx_map.tilewidth,
                                            self.tmx_map.tileheight)
                        self.all_sprites.add(platform)
                        self.platforms.add(platform)
            elif layer.name == 'coins':
                for x, y, gid in layer:
                    tile = self.tmx_map.get_tile_image_by_gid(gid)

                    if tile:
                        coin = Coin(x * self.tmx_map.tilewidth * TILE_SCALE, y * self.tmx_map.tileheight * TILE_SCALE)
                        self.all_sprites.add(coin)
                        self.coins.add(coin)
            elif layer.name == 'portals':
                for x, y, gid in layer:
                    tile = self.tmx_map.get_tile_image_by_gid(gid)

                    if tile:
                        portal = Portal(x * self.tmx_map.tilewidth * TILE_SCALE, y * self.tmx_map.tileheight * TILE_SCALE)
                        self.all_sprites.add(portal)
                        self.portals.add(portal)

        self.load_enemies()



        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 4

        self.bg_image = pg.image.load("maps/tileset/res/f;sldf4.jpg")

        self.run()

    def load_enemies(self):
        enemy_settings = {
            "crab": {
                "sprite_sheet": (
                    "sprite/Sprite Pack 2/9 - Snip Snap Crab/"
                    "Movement_(Flip_image_back_and_forth) (32 x 32).png"
                ),
                "frame_size": 32,
                "frame_count": 1,
            },
            "kopatych": {
                "sprite_sheet": (
                    "sprite/Sprite Pack 2/6 - Robo Totem/"
                    "Walking (16 x 16).png"
                ),
                "frame_size": 16,
                "frame_count": 2,
            },
        }

        with open(
            f"maps/tileset/level{self.level}_enemies.json",
            "r",
            encoding="utf-8",
        ) as json_file:
            data = json.load(json_file)

        for enemy_data in data["enemies"]:
            settings = enemy_settings.get(enemy_data["name"])
            if settings is None:
                continue

            start_position = [
                enemy_data["start_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth,
                enemy_data["start_pos"][1] * TILE_SCALE * self.tmx_map.tilewidth,
            ]
            end_position = [
                enemy_data["final_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth,
                enemy_data["final_pos"][1] * TILE_SCALE * self.tmx_map.tilewidth,
            ]

            enemy = Enemy(
                self.map_pixel_width,
                self.map_pixel_height,
                start_position,
                end_position,
                settings["sprite_sheet"],
                settings["frame_size"],
                TILE_SCALE,
                settings["frame_count"],
            )
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

    def run(self):
        self.is_running = True
        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pg.quit()
        quit()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if self.player.current_animation in (self.player.idle_animation_right, self.player.running_animatoin_right):
                        direction = 'right'
                    else:
                        direction = 'left'
                    ball = Ball(self.player.rect, direction)
                    self.balls.add(ball)
                    self.all_sprites.add(ball)
            if event.type == pg.MOUSEBUTTONDOWN:
                print(event.pos)

        if self.mode == "game over":
            if event.type == pg.KEYDOWN:
                self.setup()

    

    def update(self):
        if self.player.hp <= 0:
            self.mode = 'game over'
            return

        for enemy in self.enemies.sprites():
            if pg.sprite.collide_mask(self.player, enemy):
                self.player.get_damage()

        self.player.update(self.platforms)
        self.balls.update()
        self.coins.update()
        self.portals.update()

        pg.sprite.groupcollide(self.balls, self.enemies, True, True)
        pg.sprite.groupcollide(self.balls, self.platforms, True, False)
        if pg.sprite.spritecollide(self.player, self.coins, True):
            self.score += 1
        hits = pg.sprite.spritecollide(self.player, self.portals, False, pg.sprite.collide_mask)
        for hit in hits:
            self.level += 1
            if self.level == 3:
                quit()
            self.setup()


        for enemy in self.enemies.sprites():
            enemy.update(self.platforms)


        self.camera_x = self.player.rect.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.rect.y - SCREEN_HEIGHT // 2

        self.camera_x = max(0, min(self.camera_x, self.map_pixel_width - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.map_pixel_height - SCREEN_HEIGHT))

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.move(-self.camera_x, -self.camera_y))

        pg.draw.rect(self.screen, pg.Color("red"), (10, 10, 10*self.player.hp, 10))
        pg.draw.rect(self.screen,pg.Color("black"), (10, 10, 100, 10), 1)

        if self.mode == 'game over':
            text = font.render('Вы проиграли', True, pg.Color('red'))
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(text, text_rect)


        # pg.draw.rect(self.screen, pg.Color('red'), (544, 352, 50, 50))
        pg.display.flip()


if __name__ == "__main__":
    game = Game()
