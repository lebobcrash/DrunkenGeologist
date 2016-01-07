# global constants and variables
import libtcodpy as libtcod

# font options
FONT1 = "fonts/qbicfeet_10x10.png"
FONT2 = "fonts/Alloy_curses_12x12.png"
FONT3 = "fonts/grimfortress_cube.png"

# map screen size
CAMERA_WIDTH = 92
CAMERA_HEIGHT = 52

# overall screen size
SCREEN_WIDTH = CAMERA_WIDTH + 2
SCREEN_HEIGHT = CAMERA_HEIGHT + 4

# initialize game consoles
CON_GAME = libtcod.console_new(CAMERA_WIDTH, CAMERA_HEIGHT)	# con for displaying the map only
CON_GUI = libtcod.console_new(CAMERA_WIDTH, 1)						# con for the one-liner GUI

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