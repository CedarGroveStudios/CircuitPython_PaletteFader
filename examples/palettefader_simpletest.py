# SPDX-FileCopyrightText: 2022-09-06 JG for Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT
#
# palettefader_simpletest.py

"""
This is a PaletteFader class example for an Adafruit MatrixPortal with a
32x64 RGB LED display panel. Two text labels, a displayio shape, a vectorio
shape, and an icon spritesheet tile are placed on the display in a layer over a
background image. The Matrix Portal's analog voltage input on pin A0 controls
the foreground layer brightness over the fixed-brightness background image.
"""

import time
import random
import board
from analogio import AnalogIn
import displayio
import vectorio
import terminalio
from simpleio import map_range
from adafruit_matrixportal.matrix import Matrix
from adafruit_display_text.label import Label
from adafruit_display_shapes.rect import Rect
import adafruit_imageload
from cedargrove_palettefader.palettefader import PaletteFader

# fmt: off
# Define a few colors
YELLOW  = 0xFFFF00  # temperature
AQUA    = 0x00FFFF  # humidity
FUCHSIA = 0xFF00FF  # watchdog

# Define icon graphic object parameters
ICON_SPRITESHEET_FILE = "weather-icons.bmp"
ICON_SPRITE_WIDTH     = 16
ICON_SPRITE_HEIGHT    = 16
ICON_SPRITE           =  0  # Select a tile from the spritesheet

# Define background graphic object parameters
BKG_BRIGHTNESS = 0.2   # Initial brightness level
BKG_GAMMA      = 0.65  # Works nicely for brightness = 0.2
BKG_IMAGE_FILE = "background.bmp"

# Instantiate fader potentiometer
ANALOG_FADER  = True  # True to enable; False to disable
fader = AnalogIn(board.A0)

# Instantiate RGB LED matrix display panel
DISPLAY_BRIGHTNESS = 0.3  # Initial brightness level
DISPLAY_BIT_DEPTH  = 6    # Default is 2-bits; maximum of 6-bits
display = Matrix(bit_depth=DISPLAY_BIT_DEPTH).display
display.rotation = 270  # Portrait orientation; MatrixPortal board on bottom
DISPLAY_CENTER   = (display.width // 2, display.height // 2)
# fmt: on

# Define the primary and foreground display groups
primary_group = displayio.Group()
fg_group = displayio.Group()

# Load the background image and source color palette
bkg_bitmap, bkg_palette_source = adafruit_imageload.load(
    BKG_IMAGE_FILE, bitmap=displayio.Bitmap, palette=displayio.Palette
)
# Instantiate background PaletteFader object and display on-screen
bkg_faded = PaletteFader(bkg_palette_source, BKG_BRIGHTNESS, BKG_GAMMA, normalize=True)
bkg_tile = displayio.TileGrid(bkg_bitmap, pixel_shader=bkg_faded.palette)
primary_group.append(bkg_tile)

display.show(primary_group)

# Load the icon spritesheet and source palette
icon_spritesheet, icon_palette_source = adafruit_imageload.load(
    ICON_SPRITESHEET_FILE, bitmap=displayio.Bitmap, palette=displayio.Palette
)
# Set transparency for icon source palette index 0
icon_palette_source.make_transparent(0)

# Instantiate the icon TileGrid and place it on the display
icon_tile = displayio.TileGrid(
    icon_spritesheet,
    pixel_shader=icon_palette_source,
    tile_width=ICON_SPRITE_WIDTH,
    tile_height=ICON_SPRITE_HEIGHT,
)
icon_tile.x = DISPLAY_CENTER[0] - 8
icon_tile.y = 22
fg_group.append(icon_tile)

# Place a displayio display_shapes rectangle in the upper left corner
watchdog = Rect(0, 0, 5, 5, fill=FUCHSIA, outline=AQUA, stroke=1)
fg_group.append(watchdog)

# Define the text labels. Add an attribute for the group items palette.
temperature = Label(terminalio.FONT)
temperature.anchor_point = (0.5, 0.5)
temperature.anchored_position = (DISPLAY_CENTER[0], 14)
temperature.color = YELLOW
fg_group.append(temperature)

humidity = Label(terminalio.FONT)
humidity.anchor_point = (0.5, 0.5)
humidity.anchored_position = (DISPLAY_CENTER[0], 45)
humidity.color = AQUA
fg_group.append(humidity)

# Place a vectorio circle in the upper right corner
sun_palette = displayio.Palette(1)
sun_palette[0] = YELLOW
sun = vectorio.Circle(pixel_shader=sun_palette, radius=8, x=30, y=0)
fg_group.append(sun)

# pylint: disable=protected-access
# Create foreground group color list from ._palette and .pixel_shader contents
fg_colors_source = []
for i, group_object in enumerate(fg_group):
    if hasattr(group_object, "_palette"):
        # It's a displayio display_shapes or label object
        for j, color in enumerate(group_object._palette):
            fg_colors_source.append(color)
    elif hasattr(group_object, "pixel_shader"):
        # It's a bitmap or vectorio object
        for j, color in enumerate(group_object.pixel_shader):
            fg_colors_source.append(color)

primary_group.append(fg_group)

# Instantiate foreground color list PaletteFader object
fg_colors = PaletteFader(fg_colors_source, DISPLAY_BRIGHTNESS, normalize=False)

# ### Primary code loop starts here ###

# Reset the information and fader refresh timers; None for initial run
info_refresh_timer = None
fader_refresh_timer = None

while True:
    # Update the on-screen information every 10 seconds and on initial run
    if (not info_refresh_timer) or (time.monotonic() - info_refresh_timer) > 10:
        # Get a random temperature and humidity value
        current_temperature = random.randrange(500, 1000) / 10
        temperature.text = f"{current_temperature:.0f}°"
        current_humidity = random.randrange(200, 900) / 10
        humidity.text = f"{current_humidity:.0f}%"
        icon_tile[0] = random.randrange(0, 17)

        info_refresh_timer = time.monotonic()

    # Update brightness fader values every 0.1 second and on initial run
    if (not fader_refresh_timer) or (time.monotonic() - fader_refresh_timer) > 0.1:

        if ANALOG_FADER:
            # Read the potentiometer and calculate a new brightness value
            DISPLAY_BRIGHTNESS = int(map_range(fader.value, 300, 54000, 5, 100)) / 100

        # Update foreground group ._palette and .pixel_shader contents
        fg_colors.brightness = DISPLAY_BRIGHTNESS
        fg_colors_index = 0
        for i, _ in enumerate(fg_group):
            if hasattr(fg_group[i], "_palette"):
                # For a displayio display_shapes or label object
                for j, _ in enumerate(fg_group[i]._palette):
                    fg_group[i]._palette[j] = fg_colors.palette[fg_colors_index]
                    fg_colors_index += 1
            elif hasattr(fg_group[i], "pixel_shader"):
                # For a bitmap or vectorio object
                for j, _ in enumerate(fg_group[i].pixel_shader):
                    fg_group[i].pixel_shader[j] = fg_colors.palette[fg_colors_index]
                    fg_colors_index += 1

        fader_refresh_timer = time.monotonic()
