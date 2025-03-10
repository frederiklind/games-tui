<div align="center">
  <img src=".assets/logo.png"/>
</div>
<br/>

A collection of terminal based mini-games, written in python.


## Contents

- [Games](#games)
  - [Klondike Solitaire](#klondike-solitaire)
  - [Rubik's Cube Puzzle](#rubiks-cube-puzzle)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Manual Installation](#manual-installation)
- [Configuration](#configuration)
  - [Colorschemes](#colorschemes)
  - [Ascii-banners](#ascii-banners)

## Games

<!-- <div align="center">
  <img src=".assets/klondike-logo.png" width="75%"/>
</div> -->

### Klondike Solitaire


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



#### [Source Code for Klondike Solitaire](./src/games_tui/games/solitaire/)

<br/>

#

<!-- <br/>
<div align="center">
  <img src=".assets/rubiks_logo.png" width="75%"/>
</div> -->

### Rubik's Cube Puzzle


<br/>
<div align="center">
  <img src=".assets/rubiks.gif"/>
</div>

#### [Source Code for Rubik's](./src/games_tui/games/rubiks/)

<br/>


## Installation

### Prerequisites

This appllication requires having a nerd font installed on your system and set in the terminal emulator being used to run the application. Nerd fonts can be downloaded from [www.nerdfont.com](https://nerdfont.com). 


### Build from source

```bash
git clone https://github.com/frederiklind/games-tui.git
cd games-tui
make install
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
