import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size
from tiles import Tile, StaticTile, Crate, Coin, Palm
from enemy import Enemy

class Level:
    def __init__(self,level_data_1,surface):
        #general setup
        self.display_surface = surface
        self.world_shift = -6

        #player
        player_layout = import_csv_layout(level_data_1['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        #beach setup
        beach_layout = import_csv_layout(level_data_1['beach'])
        self.beach_sprites = self.create_tile_group(beach_layout,'beach')

        # crates
        crate_layout = import_csv_layout(level_data_1['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

        # coins
        coin_layout = import_csv_layout(level_data_1['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

        # foreground palms
        fg_palm_layout = import_csv_layout(level_data_1['fg.palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg.palms')

        # background palms
        bg_palm_layout = import_csv_layout(level_data_1['bg.palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg.palms')

        # enemy
        enemy_layout = import_csv_layout(level_data_1['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # constraint
        constraint_layout = import_csv_layout(level_data_1['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraint')

    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index , row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'beach':
                        beach_tile_list = import_cut_graphics('Graphics/decoration_1/beach/beach.jpg')
                        tile_surface = beach_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)

                    if type == 'crates':
                        sprite = Crate(tile_size, x, y)

                    if type == 'coins':
                        if val == '0': sprite = Coin(tile_size, x, y, 'Graphics/coins/gold')
                        if val == '1': sprite = Coin(tile_size, x, y, 'Graphics/coins/silver')

                    if type == 'fg.palms':
                        if val == '2': sprite = Palm(tile_size, x, y, 'Graphics/decoration_1/beach/palm_small', 38)

                    if type == 'bg.palms':
                        sprite = Palm(tile_size, x, y, 'Graphics/decoration_1/beach/palm_bg', 64)

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'constraint':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    print('player goes here')
                if val == '1':
                    hat_surface = pygame.image.load('Graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def run(self):
        # background palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        #beach
        self.beach_sprites.draw(self.display_surface)
        self.beach_sprites.update(self.world_shift)

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # foreground palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        # player sprites
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)



