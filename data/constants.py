# global constants and variables
import libtcodpy as libtcod

FPS_LIMIT = 20

# font options
FONT1 = "fonts/qbicfeet_10x10.png"
FONT2 = "fonts/Alloy_curses_12x12.png"
FONT3 = "fonts/grimfortress_cube.png"

# map screen size
CAMERA_WIDTH = 64
CAMERA_HEIGHT = 32

# overall screen size
SCREEN_WIDTH = CAMERA_WIDTH + 2
SCREEN_HEIGHT = CAMERA_HEIGHT + 4

# map size for now
MAP_WIDTH = 100
MAP_HEIGHT = 100

LOG_HEIGHT = 8

# initialize game consoles
CON_GAME = libtcod.console_new(CAMERA_WIDTH, CAMERA_HEIGHT)	        # con for displaying the map only
CON_GUI = libtcod.console_new(CAMERA_WIDTH, 1)						# con for the one-liner GUI
CON_LOG = libtcod.console_new(CAMERA_WIDTH, LOG_HEIGHT)

#########################################################
# FOV options
#########################################################

FOV_ALGORITHM = libtcod.FOV_PERMISSIVE_1
FOV_LIGHT_WALLS = True
FOV_TORCH_RADIUS = 12

#########################################################
# Colors
#########################################################

color_dark_wall = libtcod.Color(35, 35, 35)
color_light_wall = libtcod.Color(180, 180, 180)
color_dark_ground = libtcod.Color(35, 35, 35)
color_light_ground = libtcod.Color(150, 150, 150)

color_ui_frames = libtcod.Color(220,220,220)

#########################################################
# ASCII characters
#########################################################

MOVE_DIRECTIONS = {
    "up"        :   (0, -1),
    "up-right"  :   (1, -1),
    "right"     :   (1, 0),
    "down-right":   (1, 1),
    "down"      :   (0, 1),
    "down-left" :   (-1, 1),
    "left"      :   (-1, 0),
    "up-left"   :   (-1, -1)
}

MOVE_KEYS = {
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

#########################################################
# ASCII characters
#########################################################

# double bars =
ASCII_h_dbar = 205
ASCII_v_dbar = 186
ASCII_dbar_top_left = 201
ASCII_dbar_top_right = 187
ASCII_dbar_bot_left = 200
ASCII_dbar_bot_right = 188

# single lines
ASCII_h_line = 196
ASCII_v_line = 179
ASCII_line_top_left = 218
ASCII_line_top_right = 191
ASCII_line_bot_left = 192
ASCII_line_bot_right = 217
ASCII_vT_left = 195
ASCII_vT_right = 180