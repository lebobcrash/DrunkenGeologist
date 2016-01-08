from data.constants import *
import numpy as np
import random

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
        libtcod.console_put_char_ex(CON_GAME, self.x, self.y, world.map[self.y, self.x].symbol, libtcod.white, libtcod.black)


class Actor:
    def __init__(self, hp, mana):
        self.hp = hp
        self.hp_max = hp
        self.mana = mana
        self.mana_max = mana

    def move(self, dx, dy):
        # Move if Tile is walkable
        if world.map[self.owner.y + dy, self.owner.x + dx].walkable is True:
            self.owner.x += dx
            self.owner.y += dy
        else:
            pass


class Tile:
    """
    The general Tile class, carrying the x,y coordinates of the respective tile, it's symbol, name,
    in-fov- and out-of-fov-color, explored bool, walkable bool and transparent bool.
	"""
    def __init__(self, y, x):
        self.x = x
        self.y = y

        self.rel_x = None
        self.rel_y = None

        self.symbol = "."
        self.name = None
        self.color = color_light_ground
        self.color_dark = color_dark_ground

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

        # Create 2d numpy-array with objects as data type: map[y][x]
        self.map = np.ndarray((self.height, self.width), dtype=np.object)
        self.fov_map = []
        self.fov_map_np = np.ndarray((self.height, self.width), dtype=np.object)

    def generate_borders(self):
        for y in range(self.height):
            self.map[y, 0].walkable = False
            self.map[y, 0].transparent = False
            self.map[y, 0].symbol = "#"
            self.map[y, 0].name = "Wall"
            self.map[y, self.width - 1].walkable = False
            self.map[y, self.width - 1].transparent = False
            self.map[y, self.width - 1].symbol = "#"
            self.map[y, self.width - 1].name = "Wall"
            for x in range(self.width):
                self.map[0, x].walkable = False
                self.map[0, x].transparent = False
                self.map[0, x].symbol = "#"
                self.map[0, x].name = "Wall"
                self.map[self.height - 1, x].walkable = False
                self.map[self.height - 1, x].transparent = False
                self.map[self.height - 1, x].symbol = "#"
                self.map[self.height - 1, x].name = "Wall"

    def generate(self, map_type):
        ############################################################################
        if map_type == "plain":

            for y in range(world.height):
                for x in range(world.width):
                    self.map[y, x] = Tile(y, x)

            # Generate the FOV map
            self.fov_map = libtcod.map_new(self.width, self.height)  # init fov_map

            # Generate walls enclosing the map
            self.generate_borders()

            for y in range(self.height):
                for x in range(self.width):
                    if self.map[y, x].walkable is True:
                        libtcod.map_set_properties(self.fov_map, x, y, True, True)
                    else:
                        libtcod.map_set_properties(self.fov_map, x, y, False, False)
        ############################################################################
        if map_type == "noise":

            for y in range(world.height):
                for x in range(world.width):
                    self.map[y, x] = Tile(x, y)

                    noise = random.randint(0,16)
                    if noise > 0:
                        self.map[y, x].walkable = True
                        self.map[y, x].transparent = True
                        self.map[y, x].symbol = "."
                        self.map[y, x].name = "Ground"
                    else:
                        self.map[y, x].walkable = False
                        self.map[y, x].transparent = False
                        self.map[y, x].symbol = "#"
                        self.map[y, x].name = "Wall"

            # Generate the FOV map
            self.fov_map = libtcod.map_new(self.width, self.height)  # init fov_map

            # Generate walls enclosing the map
            self.generate_borders()

            for y in range(self.height):
                for x in range(self.width):
                    if self.map[y, x].walkable is True:
                        libtcod.map_set_properties(self.fov_map, x, y, True, True)
                    else:
                        libtcod.map_set_properties(self.fov_map, x, y, False, False)
        ############################################################################
        else:
            print("Invalid gen_type for method World.generate")




class Renderer:
    """

    """
    def __init__(self):
        self.fov_recompute = None

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
                    world.map[y, x].explored = True  # set visible Tile as explored

                    libtcod.console_put_char_ex(CON_GAME, x, y, world.map[y, x].symbol, world.map[y, x].color,
                                             libtcod.black)
                else:
                    if world.map[y, x].explored:  # == True
                        libtcod.console_put_char_ex(CON_GAME, x, y, world.map[y, x].symbol, world.map[y, x].color_dark,
                                                 libtcod.black)
                    else:
                        libtcod.console_put_char_ex(CON_GAME, x, y, " ", libtcod.black, libtcod.black)

        # Draw all things
        for entry in world.entities:
            entry.draw()


def update_ui():
    # Clear the UI console before refresh
    libtcod.console_clear(CON_GUI)

    # Display player.name in the top left
    libtcod.console_print_ex(CON_GUI, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, player.name)

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

    libtcod.console_set_default_foreground(CON_GUI, libtcod.white)
    libtcod.console_print_ex(CON_GUI, SCREEN_WIDTH / 2, 0, libtcod.BKGND_NONE, libtcod.CENTER,
                         get_names_under_mouse(mouse))

    # Update level number and name
    libtcod.console_print_ex(CON_GUI, CAMERA_WIDTH - 1, 0, libtcod.BKGND_NONE, libtcod.RIGHT,
                             "Level " + str(world.number) + ": " + world.name)



def check_for_input(key):
    #key = libtcod.console_wait_for_keypress(True)   # wait for player keypress

    if key.vk in MOVE_KEYS:
        dx, dy = MOVE_DIRECTIONS[MOVE_KEYS[key.vk]]
        player.actor.move(dx, dy)                   # move the player
        renderer.fov_recompute = True               # player moves -> recompute FOV
        return "player acted"

    elif key.vk is libtcod.KEY_ESCAPE:
        return "exit"


def get_names_under_mouse(mouse):

    mx, my = (mouse.cx - 1, mouse.cy - 3)

    if libtcod.map_is_in_fov(world.fov_map, mx, my):
        tile_name = world.map[my, mx].name  # + ", ".join(names)    # join the names with comma seperation
        entity_names = [entry.name for entry in world.entities
                        if entry.x == mx and entry.y == my]
        entity_names.append(tile_name)
        entity_names = ", ".join(entity_names)

        return entity_names
    else:
        return ""


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
world.generate("noise")         # Generate the map using a map_type string

renderer = Renderer()           # Initialize the renderer
renderer.fov_recompute = True   # Initialize FOV computation

#########################################################

mouse = libtcod.Mouse()
key = libtcod.Key()
libtcod.sys_set_fps(FPS_LIMIT)

while not libtcod.console_is_window_closed():
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

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
    input = check_for_input(key)
    if input == "exit":
        break