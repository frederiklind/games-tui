<div align="center">
  <img src=".assets/logo.png"/>
</div>
<br/>

A collection of terminal based mini-games, written in python. Built using Python's builtin curses library.

## Contents

- [Games](#games)
  - [Tetris]()
  - [Pingpong]()
  - [Klondike Solitaire](#klondike-solitaire)
  - [Rubik's Cube Puzzle](#rubiks-cube-puzzle)
- [Features](#features)
  - [Achievements]()
  - [Game Statistics]()
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Homebrew](#homebrew)
  - [AUR](#aur)
  - [Windows]()
  - [Manual Installation](#manual-installation)
- [Configuration](#configuration)
  - [Colorschemes](#colorschemes)
  - [Ascii-banners](#ascii-banners)

## Games

#

<br/>
<div align="center">
  <img src=".assets/klondike-logo.png" width="75%">
</div>

### Klondike Solitaire

Play Klondike Solitaire in your terminal. 

<br/>
<div align="center">
  <img src=".assets/solitaire.gif"/>
</div>

#### Controls

<div align="center">

| Action                            | Default    | Vim        | Gamer      |
|:----------------------------------|------------|------------|------------|
| Navigate (Left, Down, Up Right)   | Arrow-keys | H, J, K, L | A, S, W, D |
| Select Card(s)                    | Return     | S          | Return     |
| Drop Selection                    | Esc        | Esc        | Esc        |
| Move  card to foundation pile     | M          | F          | M          |
| Quit Game                         | Q          | Q          | Q          |

</div>

[How to manage keybindings]()

#### [Source Code for Klondike Solitaire](./src/games_tui/games/solitaire/)

<br/>

#

<br/>
<div align="center">
  <img src=".assets/rubiks_logo.png" width="75%"/>
</div>

### Rubik's Cube Puzzle

Become a master of the terminal based Rubik's cube. The game will track the number of performed moves of the cube, as well as the time used for a valid solution.

<br/>
<div align="center">
  <img src=".assets/rubiks.gif"/>
</div>

#### [Source Code for Rubik's](./src/games_tui/games/rubiks/)

<br/>

#

<br/>
<div align="center">
  <img src=".assets/tetris-logo.png" width="75%">
</div>

### Tetris

Super awesome terminal tetris.

<br/>

## Features

### Game statistics

Keeps track of the number of moves used to solve the cube, and the time spent getting a valid solution. The results are saved, encouraging you to beat your fastest time.



## Installation

### Prerequisites

This appllication requires having a nerd font installed on your system and set in the terminal emulator being used to run the application. Nerd fonts can be downloaded from [www.nerdfont.com](https://nerdfont.com). 

### Homebrew


### AUR


```bash
# using paru
paru -S games-tui

# using yay
yay -S games-tui
```

### Build from source (Arch)

```bash
git clone https://github.com/frederiklind/games-tui.git
cd games-tui
makepkg -si
```

### Manual Installation

Clone the repository and install the application using the `setup.py`:

```bash
git clone https://github.com/frederiklind/games-tui.git
cd games-tui
python setup.py install
```

## Configuration

### Color Themes

The application saves your preferences in the `.toml` configuration file that comes with the application. Preferences are saved and takes effect while changing. Comes with a variety of different color schemes, placed in the application configuration folder.

<br/>
<div align="center">
  <img src=".assets/colors.gif" />
</div>
<br/>

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

### ASCII-Banners

The ASCII-banner displayed on the application's main screen, can be changed from the application settings. 

<br/>
<div align="center">
  <img src=".assets/ascii-banners.gif"/>
</div>
