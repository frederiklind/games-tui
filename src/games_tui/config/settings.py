import os
import platform
# from typing import List

import toml
from typing import List, Any
from config.colors import ColorScheme


class Settings(object):
    """
    User settings for the application

    Attributes:
        config_dir (str): User config directory path
        color_scheme (ColorScheme): Application colorscheme
    """

    __config_dir: str
    color_scheme: str
    show_background: bool
    show_headers: bool
    show_ui_borders: bool
    ascii_banner: str

    # keybindings
    nav_left: str
    nav_right: str
    nav_up: str
    nav_down: str

    def __init__(self) -> None:
        user_os = platform.system()

        self.__config_dir = os.path.join(
            os.path.expanduser("~"), ".config", "games-tui"
        )
                
        self.load()

    def load(self) -> None:
        # get config from toml file
        with open(os.path.join(self.__config_dir, "config.toml"), "r") as f:
            conf = toml.load(f)
        
        self.color_scheme = conf['ui_display']['color_scheme']
        self.ascii_banner = conf['ui_display']['ascii_banner']
        self.show_background = conf['ui_display']['show_background']
        self.show_ui_borders = conf['ui_display']['show_ui_borders']

    def set_colors(self, scheme: str = None) -> None:
        cs = scheme if scheme is not None else self.color_scheme
        ColorScheme.set(self.__config_dir, cs, self.show_background)
         
    def dir(self) -> str:
        return self.__config_dir

    def get_colorschemes(self) -> List[str]:
        """
        Gets the available colorschemes in the configuration directory.
        """
        colorschemes: List[str] = []
        path = os.path.join(self.__config_dir, "colorschemes")
        
        i = 0
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                colorschemes.append(os.path.splitext(file)[0])  # Strip extension
                i += 1
        return colorschemes

    def get_ascii_banners(self) -> List[str]:
        """
        Gets the available ascii banners in the configuration directory.
        """
        banners: List[str] = []
        path = os.path.join(self.__config_dir, "ascii")
        
        i = 0
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                banners.append(os.path.splitext(file)[0])  # Strip extension
                i += 1
        return banners
    
    def update_toml_value(self, section: str, key: str, value: Any):
        """
        Updates specified value in the toml configuration, based on
        section and key.

        Args:
            section (str): The section name of where the key is located.
            key (str): The key of where the value is to be changed.
            value (Any): The new value to be stored in the configuration. 
        """
        file_path = os.path.join(self.__config_dir, "config.toml")
        try:
            data = toml.load(file_path)  
        except FileNotFoundError:
            data = {} 

        if section not in data:
            data[section] = {}  

        data[section][key] = value  

        with open(file_path, "w") as f:
            toml.dump(data, f)  


settings = Settings()
