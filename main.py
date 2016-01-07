from data.constants import *


#########################################################
# Classes
#########################################################


class Game:
    """

	"""
    def __init__(self):

        #######################################################################
        # initialize console
        #######################################################################

        # Set custom font
        libtcod.console_set_custom_font(FONT2, libtcod.FONT_LAYOUT_ASCII_INROW)

        # Initialize console
        libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT,  # window size
                                  "Drunken Geologist",  # window title
                                  False  # fullscreen bool
                                  )

        # Draw UI frames
        for y in range(SCREEN_HEIGHT):
            libtcod.console_put_char_ex(0, 0, y, ASCII_v_line, color_ui_frames, libtcod.black)
            libtcod.console_put_char_ex(0, SCREEN_WIDTH - 1, y, ASCII_v_line, color_ui_frames, libtcod.black)

        for x in range(SCREEN_WIDTH):
            libtcod.console_put_char_ex(0, x, 0, ASCII_h_line, color_ui_frames, libtcod.black)
            libtcod.console_put_char_ex(0, x, SCREEN_HEIGHT - 1, ASCII_h_line, color_ui_frames, libtcod.black)
            libtcod.console_put_char_ex(0, x, 2, ASCII_h_line, color_ui_frames, libtcod.black)

        libtcod.console_put_char_ex(0, 0, 0, ASCII_line_top_left, color_ui_frames, libtcod.black)
        libtcod.console_put_char_ex(0, 0, 2, ASCII_vT_left, color_ui_frames, libtcod.black)
        libtcod.console_put_char_ex(0, 0, SCREEN_HEIGHT - 1, ASCII_line_bot_left, color_ui_frames, libtcod.black)

        libtcod.console_put_char_ex(0, SCREEN_WIDTH - 1, 0, ASCII_line_top_right, color_ui_frames, libtcod.black)
        libtcod.console_put_char_ex(0, SCREEN_WIDTH - 1, 2, ASCII_vT_right, color_ui_frames, libtcod.black)
        libtcod.console_put_char_ex(0, SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1, ASCII_line_bot_right, color_ui_frames,
                                    libtcod.black)


class Entity:
    """

	"""
    def __init__(self, name, x, y, symbol, color, actor=None):
        self.name = name
        self.x = x
        self.y = y
        self.symbol = symbol
        self.color = color

        self.actor = actor
        if self.actor:
            self.actor.owner = self

    # Draws Entity at x,y
    def draw(self):
        libtcod.console_put_char_ex(CON_GAME, self.x, self.y, self.symbol, self.color, libtcod.black)

    # Replaces Entity at x,y with "."
    def clear(self):
        libtcod.console_put_char_ex(CON_GAME, self.x, self.y, ".", libtcod.white, libtcod.black)


class Actor:
    def __init__(self, hp, mana):
        self.hp = hp
        self.hp_max = hp
        self.mana = mana
        self.mana_max = mana

    def move(self, dx, dy):
        self.owner.x += dx
        self.owner.y += dy


class Tile:
    """

	"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.rel_x = None
        self.rel_y = None

        self.symbol = "."
        self.name = "Air"

        self.explored = False  # all tiles start unexplored
        self.walkable = True
        self.transparent = True


class World:
    """

	"""
    def __init__(self, name):
        self.width = CAMERA_WIDTH
        self.height = CAMERA_HEIGHT

        self.number = 1
        self.name = name

        self.entities = [player]  # list of entities in world

        self.map = []
        self.fov_map = []

    def generate(self, map_type):
        if map_type == "plain":

            self.map = [[Tile(x, y) for y in range(self.height)] for x in range(self.width)]

            # Generate the FOV map
            self.fov_map = libtcod.map_new(self.width, self.height)  # init fov_map

            for y in range(self.height):
                for x in range(self.width):
                    if self.map[x][y].walkable is True:
                        libtcod.map_set_properties(self.fov_map, x, y, True, True)
                    else:
                        libtcod.map_set_properties(self.fov_map, x, y, False, False)

        else:
            print("Invalid gen_type for method World.generate")


class Renderer:
    """

    """
    def __init__(self):
        self.fov_recompute = None

        # Display player.name in the top left
        libtcod.console_print_ex(CON_GUI, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, player.name)

    def update_world(self):
        # Compute FOV if necessary
        if self.fov_recompute:  # == True
            self.fov_recompute = False
            libtcod.map_compute_fov(world.fov_map, player.x, player.y,
                                    FOV_TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGORITHM)

        # Draw all map Tiles
        for y in range(world.height):
            for x in range(world.width):

                visible = libtcod.map_is_in_fov(world.fov_map, x, y)  # True if Tile visible for player

                if visible:
                    world.map[x][y].explored = True  # set visible Tile as explored

                    libtcod.console_put_char_ex(CON_GAME, x, y, world.map[x][y].symbol, color_light_ground,
                                             libtcod.black)
                else:
                    if world.map[x][y].explored:  # == True
                        libtcod.console_put_char_ex(CON_GAME, x, y, world.map[x][y].symbol, color_dark_ground,
                                                 libtcod.black)
                    else:
                        libtcod.console_put_char_ex(CON_GAME, x, y, " ", libtcod.black, libtcod.black)

        # Draw all things
        for entry in world.entities:
            entry.draw()


def update_ui():
    # Update the player.actor.hp
    libtcod.console_set_default_foreground(CON_GUI, libtcod.light_crimson)
    libtcod.console_print_ex(CON_GUI, len(player.name) + 1, 0,
                             libtcod.BKGND_NONE, libtcod.LEFT,
                             str(player.actor.hp) + "/" + str(player.actor.hp_max))

    # Update the player.actor.mana
    libtcod.console_set_default_foreground(CON_GUI, libtcod.light_azure)
    libtcod.console_print_ex(CON_GUI, len(player.name) + 2 * len(str(player.actor.hp)) + 3, 0,
                             libtcod.BKGND_NONE, libtcod.LEFT,
                             str(player.actor.mana) + "/" + str(player.actor.mana_max))

    # Update level number and name
    libtcod.console_set_default_foreground(CON_GUI, libtcod.white)
    libtcod.console_print_ex(CON_GUI, CAMERA_WIDTH - 1, 0, libtcod.BKGND_NONE, libtcod.RIGHT,
                             "Level " + str(world.number) + ": " + world.name)


def check_for_input():
    move_directions = {
        "up"        :   (0, -1),
        "up-right"  :   (1, -1),
        "right"     :   (1, 0),
        "down-right":   (1, 1),
        "down"      :   (0, 1),
        "down-left" :   (-1, 1),
        "left"      :   (-1, 0),
        "up-left"   :   (-1, -1)
    }

    move_keys = {
        libtcod.KEY_KP8     :   "up",
        libtcod.KEY_UP      :   "up",

        libtcod.KEY_KP9     :   "up-right",

        libtcod.KEY_KP6     :   "right",
        libtcod.KEY_RIGHT   :   "right",

        libtcod.KEY_KP3     :   "down-right",

        libtcod.KEY_KP2     :   "down",
        libtcod.KEY_DOWN    :   "down",

        libtcod.KEY_KP1     :   "down-left",

        libtcod.KEY_KP4     :   "left",
        libtcod.KEY_LEFT    :   "left",

        libtcod.KEY_KP7     :   "up-left"
    }

    key = libtcod.console_wait_for_keypress(True)   # wait for player keypress

    if key.vk in move_keys:
        dx, dy = move_directions[move_keys[key.vk]]
        player.actor.move(dx, dy)                   # move the player
        renderer.fov_recompute = True               # player moves -> recompute FOV

    elif key.vk is libtcod.KEY_ESCAPE:
        return "exit"


########################################################################################################################
# Main loop
########################################################################################################################

game = Game()   # Initialize the Game

#########################################################
# Player creation

player = Entity("Dude McSnore", CAMERA_WIDTH / 2, CAMERA_HEIGHT / 2, "@",
                libtcod.red, actor=Actor(25, 12))
#########################################################

world = World("Testrealm")    # Initialize the World named Slatsnrealm
world.generate("plain")         # Generate the map using a map_type string

renderer = Renderer()           # Initialize the renderer

#########################################################
while not libtcod.console_is_window_closed():

    renderer.update_world()  # re-render the world
    update_ui()  # re-render the ui

    ##############################################
    # blit off-screen consoles to the root console
    libtcod.console_blit(CON_GAME, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 1, 3)
    libtcod.console_blit(CON_GUI, 0, 0, SCREEN_WIDTH, 1, 0, 1, 1)

    libtcod.console_flush()
    ##############################################

    # Clear all Entities on the map
    for entity in world.entities:
        entity.clear()

    # Check for player input and act accordingly
    input = check_for_input()
    if input == "exit":
        break