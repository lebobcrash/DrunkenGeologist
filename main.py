from data.constants import *
import numpy as np
import random


#########################################################
# Classes
#########################################################


class Game:
    """
    The fundamental game object initializing the font, console and drawing the ui borders.
	"""
    def __init__(self):
        self.state = "playing"

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
        # for y in range(SCREEN_HEIGHT):
        #     libtcod.console_put_char_ex(0, 0, y, ASCII_v_line, color_ui_frames, libtcod.black)
        #     libtcod.console_put_char_ex(0, SCREEN_WIDTH - 1, y, ASCII_v_line, color_ui_frames, libtcod.black)
        #
        # for x in range(SCREEN_WIDTH):
        #     libtcod.console_put_char_ex(0, x, 0, ASCII_h_line, color_ui_frames, libtcod.black)
        #     libtcod.console_put_char_ex(0, x, SCREEN_HEIGHT - 1, ASCII_h_line, color_ui_frames, libtcod.black)
        #     libtcod.console_put_char_ex(0, x, 2, ASCII_h_line, color_ui_frames, libtcod.black)
        #
        #
        # libtcod.console_put_char_ex(0, 0, 0, ASCII_line_top_left, color_ui_frames, libtcod.black)
        # libtcod.console_put_char_ex(0, 0, 2, ASCII_vT_left, color_ui_frames, libtcod.black)
        # libtcod.console_put_char_ex(0, 0, SCREEN_HEIGHT - 1, ASCII_line_bot_left, color_ui_frames, libtcod.black)
        # libtcod.console_put_char_ex(0, SCREEN_WIDTH - 1, 0, ASCII_line_top_right, color_ui_frames, libtcod.black)
        # libtcod.console_put_char_ex(0, SCREEN_WIDTH - 1, 2, ASCII_vT_right, color_ui_frames, libtcod.black)
        # libtcod.console_put_char_ex(0, SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1, ASCII_line_bot_right, color_ui_frames,
        #                             libtcod.black)


class Entity:
    """
    Basic map Entity

    METHOD draw: draws Entity at position
    METHOD clear: overwrites Entity at position with underlying Tile
	"""
    def __init__(self, name, x, y, symbol, color, actor=None, item=None):
        self.name = name
        self.x = x
        self.y = y
        self.symbol = symbol
        self.color = color

        self.actor = actor
        if self.actor:
            self.actor.owner = self

        self.item = item
        if self.item:
            self.item.owner = self

    # Draws Entity at x,y
    def draw(self):
        (x, y) = to_camera_coordinates(self.x, self.y)

        libtcod.console_put_char_ex(CON_GAME, x, y, self.symbol, self.color, libtcod.black)

    # Replaces Entity.symbol at x,y with underlying Tile.symbol
    def clear(self):
        (x, y) = to_camera_coordinates(self.x, self.y)

        libtcod.console_put_char_ex(CON_GAME, x, y, world.map[self.y, self.x].symbol, libtcod.white,
                                    libtcod.black)


class Actor:
    """
    Optional component of an Entity, which defines it as an independent actor with basic
    traits (e.g. hp, mana) and the ability to move.

    METHOD move: moves the Entity if possible.
    """
    def __init__(self, hp, mana):
        self.hp = hp
        self.hp_max = hp
        self.mana = mana
        self.mana_max = mana
        self.inventory = []

    def move(self, dx, dy):
        # Move if Tile is walkable
        if world.map[self.owner.y + dy, self.owner.x + dx].walkable is True:
            self.owner.x += dx
            self.owner.y += dy
        else:
            pass

    def pick_up(self):
        for entry in world.entities:
            if entry.x == self.owner.x and entry.y == self.owner.y:
                if len(self.inventory) <= 26:
                    self.inventory.append(entry)
                else:
                    print "Inventory full."


class Item:
    def __init__(self, use_function=None):
        self.use_function = use_function

    def use(self):
        if self.use_function is None:
            print "This item cannot be used."
        else:
            if self.use_function() is not "cancelled":
                player.actor.inventory.remove(self.owner)
                self.use_function()
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
    Initializes the world, creates a list of all Entities present and most importantly
    the map.

    METHOD generate_borders: creates encapsulating map borders (for test maps) and is
        automatically used in "plain" and "noise".
    METHOD generate: generates map[y, x] (np.ndarray) depending on map_type str
        map_type: "plain", "noise"
	"""
    def __init__(self, name):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT

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
            self.map[y, self.width - 2].walkable = False
            self.map[y, self.width - 2].transparent = False
            self.map[y, self.width - 2].symbol = "#"
            self.map[y, self.width - 2].name = "Wall"
            for x in range(self.width):
                self.map[0, x].walkable = False
                self.map[0, x].transparent = False
                self.map[0, x].symbol = "#"
                self.map[0, x].name = "Wall"
                self.map[self.height - 2, x].walkable = False
                self.map[self.height - 2, x].transparent = False
                self.map[self.height - 2, x].symbol = "#"
                self.map[self.height - 2, x].name = "Wall"

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

                    noise = random.randint(0, 30)
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
    Initializes the fov_recompute and is used to update the world

    METHOD update_world: computes fov if necessary and draws all map Tiles and Entities
    """
    def __init__(self):
        self.fov_recompute = None

    def update_world(self):

        move_camera(player.x, player.y)

        # Compute FOV if necessary
        if self.fov_recompute:  # == True
            self.fov_recompute = False
            libtcod.map_compute_fov(world.fov_map, player.x, player.y,
                                    FOV_TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGORITHM)

        # Draw all map Tiles
        for y in range(CAMERA_HEIGHT):
            for x in range(CAMERA_WIDTH):

                (map_x, map_y) = (camera_x + x, camera_y + y)

                visible = libtcod.map_is_in_fov(world.fov_map, map_x, map_y)  # True if Tile visible for player

                if visible:
                    world.map[map_y, map_x].explored = True  # set visible Tile as explored

                    libtcod.console_put_char_ex(CON_GAME, x, y, world.map[map_y, map_x].symbol, world.map[map_y, map_x].color,
                                                libtcod.black)
                else:
                    if world.map[map_y, map_x].explored:  # == True
                        libtcod.console_put_char_ex(CON_GAME, x, y, world.map[map_y, map_x].symbol, world.map[map_y, map_x].color_dark,
                                                    libtcod.black)
                    else:
                        libtcod.console_put_char_ex(CON_GAME, x, y, " ", libtcod.black, libtcod.black)

        # Draw all Entities
        for entry in world.entities:
            if entry != player:
                entry.draw()
        player.draw()   # draw player last


def update_ui():
    """
    Handles the top-screen ui updating (player name, hp, mana, mouse-hover names and
    level number and name).
    :return: N/A
    """
    # Clear the UI console before refresh
    libtcod.console_clear(CON_GUI)

    # Display player.name in the top left
    # libtcod.console_print_ex(CON_GUI, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, player.name)

    # Update the player.actor.hp
    libtcod.console_set_default_foreground(CON_GUI, libtcod.light_crimson)
    libtcod.console_print_ex(CON_GUI, 0, 0,
                             libtcod.BKGND_NONE, libtcod.LEFT,
                             str(player.actor.hp) + "/" + str(player.actor.hp_max))

    # Update the player.actor.mana
    libtcod.console_set_default_foreground(CON_GUI, libtcod.light_azure)
    libtcod.console_print_ex(CON_GUI, 2 * len(str(player.actor.hp)) + 2, 0,
                             libtcod.BKGND_NONE, libtcod.LEFT,
                             str(player.actor.mana) + "/" + str(player.actor.mana_max))

    libtcod.console_set_default_foreground(CON_GUI, libtcod.white)
    libtcod.console_print_ex(CON_GUI, SCREEN_WIDTH / 2, 0, libtcod.BKGND_NONE, libtcod.CENTER,
                             get_names_under_mouse(mouse))

    # Update level number and name
    libtcod.console_print_ex(CON_GUI, CAMERA_WIDTH - 1, 0, libtcod.BKGND_NONE, libtcod.RIGHT,
                             "Level " + str(world.number) + ": " + world.name)

#########################################################################################################
# Functions
#########################################################################################################


def check_input(key):
    """
    Checks the input and acts accordingly. Does player.actor.move and issues fov recompute
    if applicable.
    :param key: libtcod.Key()
    :return: str: "player acted" if turn taken, "exit" if ESC
    """
    if key.vk is libtcod.KEY_ESCAPE:
        return "exit"

    if game.state is "playing":

        if key.vk in MOVE_KEYS:
            dx, dy = MOVE_DIRECTIONS[MOVE_KEYS[key.vk]]
            player.actor.move(dx, dy)  # move the player
            renderer.fov_recompute = True  # player moves -> recompute FOV
            return "player acted"

        else:
            key_char = chr(key.c)

            if key_char == "i":
                chosen_item = inventory_menu()
                if chosen_item is not None:
                    chosen_item.use()
                # game.state = "in menu"

            return "player did not act"


def get_names_under_mouse(mouse):
    """
    Provides name of Tile and present Entities at mouse position (if in fov).
    :param mouse: libtcod.Mouse()
    :return: list of str or empty str
    """
    mx, my = (mouse.cx - 1 + camera_x, mouse.cy - 3 + camera_y)  # correct mouse coordinates for top-ui and frame

    if libtcod.map_is_in_fov(world.fov_map, mx, my):  # only for Tiles in fov
        tile_name = world.map[my, mx].name

        # Create list of str of all Entities at mouse position
        entity_names = [entry.name for entry in world.entities
                        if entry.x == mx and entry.y == my]
        entity_names.append(tile_name)
        entity_names = ", ".join(entity_names)

        return entity_names
    else:
        return ""


def menu(title, options):
    """

    :param title: title str
    :param options: list of menu options str
    :return:
    """
    # Create off-screen console for the menu
    menu_window = libtcod.console_new(CAMERA_WIDTH, CAMERA_HEIGHT)
    libtcod.console_set_default_background(menu_window, libtcod.black)

    # Print the title
    libtcod.console_print_ex(menu_window, 2, 2, libtcod.BKGND_NONE, libtcod.LEFT, "- " + title + " -")

    # Loop-print all options
    h = 5
    numerator = ord("a")
    for entry in options:
        text = "[" + chr(numerator) + "] " + entry
        libtcod.console_print_ex(menu_window, 4, h, libtcod.BKGND_NONE, libtcod.LEFT, text)
        h += 1
        numerator += 1

    # Blit to the root console
    libtcod.console_blit(menu_window, 0, 0, CAMERA_WIDTH, CAMERA_HEIGHT, 0, 1, 3)

    # Present root console to the player and wait for key-press
    libtcod.console_flush()
    key = libtcod.console_wait_for_keypress(True)

    # Convert ASCII code to an index, if it corresponds to an option, return it
    index = key.c - ord("a")
    if 0 <= index < len(options):
        return index
    else:
        return None


def inventory_menu():

    if len(player.actor.inventory) == 0:
        options = ["Inventory is empty."]
    else:
        options = [entry.name for entry in player.actor.inventory]

    index = menu("Inventory", options)

    # if an item was chosen, return it:
    if index is None or len(player.actor.inventory) == 0:
        return None
    else:
        return player.actor.inventory[index].item


def move_camera(target_x, target_y):
    global camera_x, camera_y

    # new camera coordinates
    x = target_x - CAMERA_WIDTH / 2
    y = target_y - CAMERA_HEIGHT / 2

    # make sure the camera doesnt see outside of the map
    if x < 0: x = 0
    if y < 0: y = 0
    if x > MAP_WIDTH - CAMERA_WIDTH - 1:
        x = MAP_WIDTH - CAMERA_WIDTH - 1
    if y > MAP_HEIGHT - CAMERA_HEIGHT - 1:
        y = MAP_HEIGHT - CAMERA_HEIGHT - 1

    (camera_x, camera_y) = (x, y)

    if x != camera_x or y != camera_y:
        renderer.fov_recompute = True


def to_camera_coordinates(x, y):
    # convert coordinates on the map to coordinates on the screen
    (x, y) = (x - camera_x, y - camera_y)

    if x < 0 or y < 0 or x >= CAMERA_WIDTH or y >= CAMERA_HEIGHT:
        return None, None # if it's outside the view return nothing

    return x, y






##################################################################################################
# Spell functions
##################################################################################################


def heal(target, amount):
    if target.actor.hp == target.actor.hp_max:
        print "Target already at full health."
        return "cancelled"
    else:
        if target.actor.hp + amount > target.actor.hp_max:
            target.actor.hp = target.actor.hp_max
        else:
            target.actor.hp += amount




########################################################################################################################
# Main loop
########################################################################################################################

game = Game()  # Initialize the Game

#########################################################
# Player creation
player = Entity("Dude McSnore", MAP_WIDTH / 2, MAP_HEIGHT / 2, "@",
                libtcod.red, actor=Actor(25, 12))

test_item = Entity("Pale Red Potion", None, None, "!", libtcod.white,
                   item=Item())
player.actor.inventory.append(test_item)
player.actor.hp -= 11
#########################################################

world = World("Testrealm")  # Initialize the World named Slatsnrealm
world.generate("noise")  # Generate the map using a map_type string

renderer = Renderer()  # Initialize the renderer
renderer.fov_recompute = True  # Initialize FOV computation

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
    input = check_input(key)
    if input == "exit":
        break
