import os
import platform
import toml

from typing import List
from config.colors import ColorScheme


class Settings(object):
    """
    User settings for the application

    Attributes:
        config_dir (str): User config directory path
        color_scheme (ColorScheme): Application colorscheme
    """

    config_dir: str
    show_background: bool
    show_headers: bool
    show_ui_borders: bool
    color_scheme: ColorScheme
    ascii_banner: str

    # keybindings
    nav_left: str
    nav_right: str
    nav_up: str
    nav_down: str
    
    
    def __init__(self) -> None:
        user_os = platform.system()
     
        self.__config_dir = os.path.join(os.path.expanduser('~'), ".config", "rubiks-tui")
    
    
    def set_colors(self, )


settings = Settings()
