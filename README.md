<br/>
<div align="center">
  <img src=".assets/logo.png"/>
</div>
<br/>

A collection of terminal based mini-games, written in python. 

## Contents

- [Features](#features)
  - [Rubik's Cube Puzzle]()
  - [Klondike Solitaire](#klondike-solitaire )
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Homebrew](#homebrew)
  - [AUR](#aur)
  - [Windows]()
  - [Manual Installation](#manual-installation)
- [Configuration](#configuration)
  - [Colorschemes](#colorschemes)
  - [Ascii-banners](#ascii-banners)

## Features

### Klondike Solitaire



### Rubik's Cube Puzzle

Become a master of the terminal based Rubik's cube. The game will track the number of performed moves of the cube, as well as the time used for a valid solution.

<div align="center">
  <img src=".assets/rubiks-ui.png"/>
</div>

### Game statistics

Keeps track of the number of moves used to solve the cube, and the time spent getting a valid solution. The results are saved, encouraging you to beat your fastest time.

### Application Settings

The application saves your preferences in the `.toml` configuration file that comes with the application. Preferences are saved and takes effect while changing. Comes with a variety of different color schemes, placed in the application configuration folder.

<div align="center">
  <img src=".assets/colors.gif" />
</div>

The application gets color themes from the application config directory:

- **Linux** - ~/.config/games-tui/colorschemes/
- **MacOS** - ~/.something/.../games-tui/colorschemes/
- **Windows** - C:\Users\your_username\something\...\games-tui\colorschemes

To add your own color themes, the toml template below can be used as a starting point. The application supports both RGB, and hex color codes.

```toml
[base_colors]
white = ""
yellow = ""
green = ""
blue = ""
red = ""
orange = ""

[ui_colors]
window_background = ""
header_background = ""
header_text = ""
ui_text = ""
ui_text_selected = ""
ascii_title = ""
icons = ""

[game_colors]
card_frames = ""
card_selected_frame = ""
```

## Installation

### Prerequisites

This appllication requires having a nerd font installed on your system and set in the terminal emulator being used to run the application. Nerd fonts can be downloaded from [www.nerdfont.com](https://nerdfont.com). 

### Homebrew


### AUR


```bash
# using paru
paru -S rubiks-tui

# using yay
yay -S rubiks-tui
```

### Build from source (Arch)

```bash
git clone https://github.com/FLIVLA/rubiks-tui.git
cd rubiks-tui
makepkg -si
```

### Manual Installation

Clone the repository and install the application using the `setup.py`:

```bash
git clone https://github.com/FLIVLA/rubiks-tui.git
cd rubiks-tui
python setup.py install
```


## Configuration

Configuration files will be placed in the applications config directory

- **Linux**: ~/.config/rubiks-tui/config.toml
- **MacOS**:

Example configuration can be found [Here]("")

Following is the default configuration file:

```toml
# ------------------------ UI Display --------------------------
# Display options for the UI. Note that for custom ascii banners,
# there is a max y,x of y,x characters of the 
# 

[ui_display]
show_background = "true"  # set to false for transparent window background
show_headers = "true"     # display of sidepane headers
show_ui_borders = "false" # display of borders around windows
color_scheme = "default"  # name of the colorscheme (filename wo. extension)
ascii_banner = "default"  # ascii banner displayed on the start screen

# ----------------------- KEYBINDINGS --------------------------
# Navigation:
#   Default navigation: arrow keys 
#   Default alt navigation: are set to vim keybindings (h,j,k,l)
#
# Cube rotation:
#   Clockwise rotation: arrow key (right)
#   Counter clockwise rotation: arrow key (left)
#   Alt clockwise rotation: vim key (l)
#   Alt counter clockwise rotation: vim key (h)

[keybindings]
nav_left = "arw"                    # navigate left
nav_right = "arw"                   # navigate right
nav_up = "arw"                      # navigate up
nav_down = "arw"                    # navigate down 
rotate_clockwise = "arw"            # clockwise cube rotation
rotate_counter_clockwise = "arw"    # counter clockwise cube rotation
alt_nav_left = "h"                  # alt navigate left
alt_nav_right = "l"                 # alt navigate right
alt_nav_up = "k"                    # alt navgate down
alt_nav_down = "j"                  # alt navgate up
alt_rotate_clockwise = "h"          # alt clockwise cube rotation
alt_rotate_counter_clockwise = "l"  # alt counter clockwise cube rotation

# TODO:
# maybe implement custom shortcut bindings for the different moves.
```




