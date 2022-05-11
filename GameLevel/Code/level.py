import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size
from tiles import Tile, StaticTile, Crate

class Level:
    def __init__(self,level_data_1,surface):
        #general setup
        self.display_surface = surface
        self.world_shift = -4

        #beach setup
        beach_layout = import_csv_layout(level_data_1['beach'])
        self.beach_sprites = self.create_tile_group(beach_layout,'beach')

        # crates
        crate_layout = import_csv_layout(level_data_1['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

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

                    sprite_group.add(sprite)

        return sprite_group

    def run(self):

        #beach
        self.beach_sprites.draw(self.display_surface)
        self.beach_sprites.update(self.world_shift)

        # crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

