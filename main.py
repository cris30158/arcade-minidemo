"""
Sprite Collect Coins

Simple program to show basic sprite usage.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_collect_coins
"""

import random
import arcade

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = .25
SPRITE_SCALING_ENEMY = .025
COIN_COUNT = 50
ENEMY_COUNT = random.randrange(5) + 5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Collect Coins Example"

BG_COL_FLOOR = 128
BG_COL_CEIL = 255


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None
        self.enemy_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.winState = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        self.Rbg = BG_COL_CEIL
        self.Gbg = BG_COL_FLOOR
        self.Bbg = BG_COL_FLOOR
        self.bgState = 0

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        # Character image from kenney.nl
        img = ":resources:images/animated_characters/female_person/femalePerson_idle.png"
        self.player_sprite = arcade.Sprite(img, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Create the coins
        for i in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite(":resources:images/items/coinGold.png",
                                 SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)

        for i in range(ENEMY_COUNT):
            enemy = arcade.Sprite("circle.png",
                                 SPRITE_SCALING_ENEMY)

            enemy.center_x = random.randrange(SCREEN_WIDTH)
            enemy.center_y = random.randrange(SCREEN_HEIGHT)

            self.enemy_list.append(enemy)

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.coin_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"

        end_text = ""

        if self.winState != 0:
            output = ""
            self.player_sprite.remove_from_sprite_lists()
            for coin in self.coin_list:
                coin.remove_from_sprite_lists()
            for enemy in self.enemy_list:
                enemy.remove_from_sprite_lists()

            if self.winState == 1:
                end_text = "You won!"
            elif self.winState == 2:
                end_text = "You lost"


        arcade.draw_text(text=end_text, start_x=SCREEN_WIDTH / 2 - 100, start_y=SCREEN_HEIGHT / 2 - 20,
                         color=arcade.color.WHITE, font_size=40)

        arcade.draw_text(text=output, start_x=10, start_y=20,
                         color=arcade.color.WHITE, font_size=14)


    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Generate a list of all sprites that collided with the player.
        coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.coin_list)
        enemies_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.enemy_list)


        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        if len(enemies_hit_list) > 0:
            self.winState = 2

        if self.score == COIN_COUNT:
            self.winState = 1

        if self.bgState == 0:
            self.Gbg += 1
            if self.Gbg == BG_COL_CEIL:
                self.bgState += 1

        elif self.bgState == 1:
            self.Rbg -= 1
            if self.Rbg == BG_COL_FLOOR:
                self.bgState += 1

        elif self.bgState == 2:
            self.Bbg += 1
            if self.Gbg == BG_COL_CEIL:
                self.bgState += 1

        elif self.bgState == 3:
            self.Gbg -= 1
            if self.Gbg == BG_COL_FLOOR:
                self.bgState += 1

        elif self.bgState == 4:
            self.Rbg += 1
            if self.Rbg == BG_COL_CEIL:
                self.bgState += 1

        elif self.bgState == 5:
            self.Bbg -= 1
            if self.Bbg == BG_COL_FLOOR:
                self.bgState = 0


        arcade.set_background_color((self.Rbg, self.Gbg, self.Bbg))


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
