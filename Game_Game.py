"""
Game Game by Isaya
"""
import arcade
import random
import pyglet
import pyglet.media as media

#Constats
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Game Game"


CHARACTER_SCALING = 0.48
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING
PLAYER_MOVEMENT_SPEED = 10

GRAVITY = 0.8
PLAYER_JUMP_SPEED = 20

PLAYER_START_X = 64
PLAYER_START_Y = 225

LAYER_NAME_MOVING_PLATFORMS = "Moving Platforms"
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
#LAYER_NAME_FOREGROUND = "Foreground"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_DONT_TOUCH = "Don't Touch"
LAYER_NAME_AXOLOTL = "Axolotl"
LAYER_NAME_LADDERS = "Ladders"



class MyGame(arcade.Window):
    """
    Main application class.
    """
    def my_playlist(self):
        while not self.playingRickroll:
            yield self.otherside
        while self.playingRickroll:
            yield self.rickroll

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.tile_map = None
        self.scene = None
        self.rickrollimg = "Rickrollimg/frame"
        self.rick_sprite = None

        self.CURRENT_RICK_VALUE = 5

        self.player_sprite = None

        self.physics_engine = None

        self.camera = None

        self.gui_camera = None

        self.score = 0

        self.axolotl = 0

        self.end_of_map = 0

        self.level = 1

        self.collect_coin_sound = arcade.load_sound("Coin Sound Effect.mp3")
        self.axolotl_sound1 = arcade.load_sound("idle_air1.mp3")
        self.axolotl_sound2 = arcade.load_sound("idle_air2.mp3")
        self.axolotl_sound3 = arcade.load_sound("idle_air3.mp3")
        self.axolotl_sound4 = arcade.load_sound("idle_air4.mp3")
        self.axolotl_sound5 = arcade.load_sound("idle_air5.mp3")
        self.jump_sound = arcade.load_sound("no.wav")

        self.yes_sound = arcade.load_sound("yes.mp3")
        self.game_over = arcade.load_sound("Gameover.mp3")
        self.rickroll = media.load("Rickroll.mp3")
        self.otherside = media.load("otherside.mp3")

        self.playingRickroll = False
        arcade.set_background_color(arcade.csscolor.AQUAMARINE)
        self.background_music = media.Player()
        self.background_music.queue(my_playlist())



    def setup(self):
        print(str(self.playingRickroll))
        self.background_music.next_source()
        self.camera = arcade.Camera(self.width, self.height)

        self.gui_camera = arcade.Camera(self.width, self.height)

        # Name of map file to load


        map_name = f"map{self.level}.json"
        #map_name = f":resources:tiled_maps/map_with_ladders.json"

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_COINS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_AXOLOTL:{
                "use_spatial_hash": True,
            },
            LAYER_NAME_MOVING_PLATFORMS:{
                "use_spatial_hash": True,
            },
            LAYER_NAME_LADDERS: {
                "use_spatial_hash": True,
            },



        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.score = 0
        self.axolotl = 0

 # Add Player Spritelist before "Foreground" layer. This will make the foreground
        # be drawn after the player, making it appear to be in front of the Player.
        # Setting before using scene.add_sprite allows us to define where the SpriteList
        # will be in the draw order. If we just use add_sprite, it will be appended to the
        # end of the order.

        #self.scene.add_sprite_list_before("Player",LAYER_NAME_FOREGROUND)
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Rickroll")
        image_source = "Python_Logo.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)


        self.rick_sprite = arcade.Sprite(f"{self.rickrollimg}{(str(1)).zfill(2)}.gif")
        self.rick_sprite.scale = 2.2
        self.rick_sprite.center_x = SCREEN_WIDTH/2
        self.rick_sprite.center_y = SCREEN_HEIGHT/2
        self.rick_sprite.image_width = 100
        self.rick_sprite.image_height = 50
        self.rick_sprite.alpha = 0
        self.scene.add_sprite("Rickroll", self.rick_sprite)

        self.end_of_map = self.tile_map.tiled_map.map_size.width * GRID_PIXEL_SIZE

        if self.tile_map.tiled_map.background_color:
            arcade.set_background_color(self.tile_map.tiled_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            [
                self.scene.get_sprite_list(LAYER_NAME_PLATFORMS),
                self.scene.get_sprite_list(LAYER_NAME_MOVING_PLATFORMS),
            ],
            gravity_constant=GRAVITY,
            ladders=self.scene.get_sprite_list(LAYER_NAME_LADDERS),
        )



    def on_draw(self):

        arcade.start_render()

        self.camera.use()
        self.scene.draw()

        self.gui_camera.use()

        score_text = f"Score: {self.score}{self.player_sprite.position}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.BLACK,
            18,
        )

        if self.axolotl >= 1:
            axolotl_text = f"Axolotl Count: {self.axolotl}"
            arcade.draw_text(
                axolotl_text,
                820,
                610,
                arcade.csscolor.PINK,
                18,
                )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.DOWN:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.R:
            self.player_sprite.center_x = 64
            self.player_sprite.center_y = 128
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.playingRickroll = False
            self.setup()
            arcade.play_sound(self.yes_sound)
        elif key ==arcade.key.RSHIFT:
            self.playingRickroll = True
            self.setup()
            self.rick_sprite.alpha = 255


    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)
    def on_update(self, delta_time):
        self.physics_engine.update()

        self.scene.update([LAYER_NAME_MOVING_PLATFORMS])

        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene.get_sprite_list("Coins")
        )

        axolotl_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene.get_sprite_list("Axolotl")
        )

        self.CURRENT_RICK_VALUE +=1
        if self.CURRENT_RICK_VALUE >=(53*4):
            self.CURRENT_RICK_VALUE = 5
        self.rick_sprite.texture = arcade.load_texture(f"{self.rickrollimg}{(str(int(self.CURRENT_RICK_VALUE/4))).zfill(2)}.gif")
        #elf.rick_sprite.image_height = SCREEN_HEIGHT
        #self.rick_sprite.image_width = SCREEN_WIDTH

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.score +=1
        self.center_camera_to_player()

        for axolotl in axolotl_hit_list:
            axolotl.remove_from_sprite_lists()
            totally_alive_axolotl = random.randrange(1,5)
            if totally_alive_axolotl == 1:
                arcade.play_sound(self.axolotl_sound1)
            elif totally_alive_axolotl == 2:
                arcade.play_sound(self.axolotl_sound2)
            elif totally_alive_axolotl == 3:
                arcade.play_sound(self.axolotl_sound3)
            elif totally_alive_axolotl == 4:
                arcade.play_sound(self.axolotl_sound4)
            elif totally_alive_axolotl == 5:
                arcade.play_sound(self.axolotl_sound5)
            self.axolotl +=1

        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y
            self.setup()

            arcade.play_sound(self.game_over)

        if arcade.check_for_collision_with_list(
            self.player_sprite, self.scene.get_sprite_list(LAYER_NAME_DONT_TOUCH)

        ):
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y



        if self.player_sprite.center_x >= self.end_of_map:
            self.level += 1

            self.setup()

def main():
        window = MyGame()
        window.setup()
        arcade.run()


if __name__ == "__main__":
    main()
