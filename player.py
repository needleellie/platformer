from settings import *
import pygame as pg



class Player(pg.sprite.Sprite):
    def __init__(self, map_width, map_height):
        super(Player, self).__init__()

        self.load_animations()
        self.current_animation = self.idle_animation_right
        self.image = self.current_animation[0]
        self.animation_frame = 0

        self.rect = self.image.get_rect()
        self.rect.center = (200, 100)

        
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.is_jumping = False
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE

        self.animation_timer = pg.time.get_ticks()
        self.animation_interval = 200

        self.hp = 10
        self.damage_timer = pg.time.get_ticks()
        self.damage_interval = 1000

    def get_damage(self):
        if pg.time.get_ticks() - self.damage_timer > self.damage_interval:
            self.hp -= 1
            self.damage_timer = pg.time.get_ticks()


    def update(self, platforms):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

                if self.mode == 'game over':
                    if event.type == pg.KEYDOWN:
                        self.setup()
        keys = pg.key.get_pressed()

        if keys[pg.K_SPACE] and not self.is_jumping:
            self.jump()
        if keys[pg.K_a]:
            if self.current_animation != self.running_animation_left:
                self.current_animation = self.running_animation_left
                self.animation_frame = 0
            
            self.velocity_x = -10
        elif keys[pg.K_d]:
            if self.current_animation != self.running_animation_right:
                self.current_animation = self.running_animation_right
                self.animation_frame = 0

            self.velocity_x = 10
        else:
            if self.current_animation == self.running_animation_right:
                self.current_animation = self.idle_animation_right
            elif self.current_animation == self.running_animation_left:
                self.current_animation = self.idle_animation_left

            self.velocity_x = 0

        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        for platform in platforms:

            if platform.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False

            if platform.rect.collidepoint(self.rect.midtop):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0

        if pg.time.get_ticks() - self.animation_timer > self.animation_interval:
            self.animation_frame += 1
            if self.animation_frame >= len(self.current_animation):
                self.animation_frame = 0
            self.image = self.current_animation[self.animation_frame]
            self.animation_timer = pg.time.get_ticks()

    def jump(self):
        self.velocity_y = -45
        self.is_jumping = True

    def load_animations(self):
        tile_size = 16
        tile_scale = 4

        self.idle_animation_right = []

        num_images = 2
        spritesheet = pg.image.load('sprite/Sprite Pack 2/1 - Onion Lad/Idle (16 x 16).png')

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            self.idle_animation_right.append(image)

        self.idle_animation_left = [pg.transform.flip(image, True, False) for image in self.idle_animation_right]

        self.running_animation_right = []

        spritesheet = pg.image.load('sprite/Sprite Pack 2/1 - Onion Lad/Run_&_Jump (16 x 16).png')

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            self.running_animation_right.append(image)
        
        self.running_animation_left = [pg.transform.flip(image, True, False) for image in self.running_animation_right]






class Ball(pg.sprite.Sprite):
    def __init__(self, player_rect, direction):
        super(Ball, self).__init__()

        self.direction = direction
        self.speed = 10

        self.image = pg.image.load('sprite/шар.png')
        self.image = pg.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect()
        if self.direction == 'right':
            self.rect.x = player_rect.right
        if self.direction == 'left':
            self.rect.x = player_rect.left
        self.rect.y = player_rect.centery

    def update(self):
        if self.direction == 'right':
            self.rect.x += self.speed
        if self.direction == 'left':
            self.rect.x -= self.speed

        if self.rect.x < 0:
            self.kill()
        if self.rect.x > SCREEN_WIDTH:
            self.kill()