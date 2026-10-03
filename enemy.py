import pygame as pg

from settings import TILE_SCALE


class Enemy(pg.sprite.Sprite):
    """A simple walking enemy that moves between two points."""

    def __init__(
        self,
        map_width,
        map_height,
        start_position,
        end_position,
        sprite_sheet_path,
        frame_size,
        scale,
        frame_count,
    ):
        super().__init__()

        self.walking_right = self.load_animation(
            sprite_sheet_path,
            frame_size,
            scale,
            frame_count,
        )
        self.walking_left = [
            pg.transform.flip(image, True, False)
            for image in self.walking_right
        ]

        self.animation = self.walking_right
        self.animation_frame = 0
        self.image = self.animation[self.animation_frame]

        self.rect = self.image.get_rect()
        self.rect.bottomleft = start_position

        self.left_edge = start_position[0]
        self.right_edge = end_position[0]

        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE

        self.direction = "right"
        self.move_speed = 5

        self.animation_timer = pg.time.get_ticks()
        self.animation_interval = 300

    @staticmethod
    def load_animation(sprite_sheet_path, frame_size, scale, frame_count):
        sprite_sheet = pg.image.load(sprite_sheet_path).convert_alpha()
        animation = []

        for frame_index in range(frame_count):
            frame_rect = pg.Rect(
                frame_index * frame_size,
                0,
                frame_size,
                frame_size,
            )
            image = sprite_sheet.subsurface(frame_rect)
            image = pg.transform.scale(
                image,
                (frame_size * scale, frame_size * scale),
            )
            animation.append(image)

        return animation

    def update(self, platforms):
        self.update_direction()
        self.move(platforms)
        self.animate()

    def update_direction(self):
        if self.rect.right >= self.right_edge:
            self.direction = "left"
        elif self.rect.left <= self.left_edge:
            self.direction = "right"

        if self.direction == "right":
            self.velocity_x = self.move_speed
            self.animation = self.walking_right
        else:
            self.velocity_x = -self.move_speed
            self.animation = self.walking_left

    def move(self, platforms):
        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        for platform in platforms:
            if platform.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0

            if platform.rect.collidepoint(self.rect.midtop):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0

    def animate(self):
        if pg.time.get_ticks() - self.animation_timer <= self.animation_interval:
            return

        self.animation_frame = (self.animation_frame + 1) % len(self.animation)
        self.image = self.animation[self.animation_frame]
        self.animation_timer = pg.time.get_ticks()
