import os
import toml
import re
import curses

from typing import Dict


class RGBColor(object):
    """
    RGB Colors
    
    Attributes:
        r (int): Red.
        g (int): Green.
        b (int): Blue.
    """
    r: int
    g: int
    b: int

    def __init__(self, color: str) -> None:
        """
        Initialize RGBColor from either hex (#RRGGBB) or rgb(r, g, b).
        """
        if color.startswith("#"):
            self.r, self.g, self.b = self.__hex_to_rgb(color)
        else:
            self.r, self.g, self.b = self.__parse_rgb(color)

        # Convert to curses-compatible values
        self.r = self.__to_curses_color(self.r)
        self.g = self.__to_curses_color(self.g)
        self.b = self.__to_curses_color(self.b)

    def __hex_to_rgb(self, hex_color: str):
        """
        Convert hex color (#RRGGBB) to an RGB tuple.

        Args:
            hex_color (str): Hex color string.

        Returns:
            tuple: (r, g, b) values as integers.
        """
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def __parse_rgb(self, rgb_color: str):
        """
        Extract RGB values from an 'rgb(r, g, b)' formatted string.

        Args:
            rgb_color (str): RGB string.

        Returns:
            tuple: (r, g, b) values as integers.
        """
        nums = re.findall(r'\d+', rgb_color)
        return map(int, nums)  # Returns (r, g, b)

    def __to_curses_color(self, x: int) -> int:
        """
        Converts RGB Values to curses compatible values.

        Args:
            x: (int): R, G, or B value for a color.

        Returns:
            int: The curses compatible R, G or B value.
        """
        return int((x / 255) * 1000)
    

class ColorScheme:
    """
    Coloscheme for the UI.

    """
    @staticmethod
    def get_from_file(path: str, scheme: str) -> Dict[int, RGBColor]:
        """

        """
        with open(os.path.join(path, "colorschemes", f"{scheme}.toml"), 'r') as f:
            scheme = toml.load(f)
        return {
            1: RGBColor(scheme['cube']['cube_top']),
            2: RGBColor(scheme['cube']['cube_bottom']),
            3: RGBColor(scheme['cube']['cube_left']),
            4: RGBColor(scheme['cube']['cube_right']),
            5: RGBColor(scheme['cube']['cube_front']),
            6: RGBColor(scheme['cube']['cube_back']),
            7: RGBColor(scheme['window']['window_background']),
            8: RGBColor(scheme['header']['header_background']),
            9: RGBColor(scheme['header']['header_text']),
            10: RGBColor(scheme['text']['ui_text']),
            11: RGBColor(scheme['text']['ui_selected_text']),
            12: RGBColor(scheme['text']['icons']),
            13: RGBColor(scheme['text']['ascii_title'])
        }

    @staticmethod
    def set(path: str, scheme: str, show_bck: bool) -> None:
        """
        Sets the curses colors from configuration file.   
        """
        colors = ColorScheme.get_from_file(path, scheme)
        
        if curses.has_colors() and curses.can_change_color():
            for k, v in colors.items():
                curses.init_color(k + 20, v.r, v.g, v.b)    # create colors

            # setup setup colorpairs
            curses.init_pair(1, 21, ColorScheme.__get_bck(1) if show_bck else -1)
            curses.init_pair(2, 22, ColorScheme.__get_bck(2) if show_bck else -1)
            curses.init_pair(3, 23, ColorScheme.__get_bck(3) if show_bck else -1)
            curses.init_pair(4, 24, ColorScheme.__get_bck(4) if show_bck else -1)
            curses.init_pair(5, 25, ColorScheme.__get_bck(5) if show_bck else -1)
            curses.init_pair(6, 26, ColorScheme.__get_bck(6) if show_bck else -1)

            curses.init_pair(7, -1, ColorScheme.__get_bck(7) if show_bck else -1)    # window background
            curses.init_pair(8, 29, ColorScheme.__get_bck(8) if show_bck else -1)    # headers
            curses.init_pair(9, 30, ColorScheme.__get_bck(9) if show_bck else -1)    # ui text
            curses.init_pair(10, 31, ColorScheme.__get_bck(10) if show_bck else -1)  # ui selected text
            curses.init_pair(11, 32, ColorScheme.__get_bck(11) if show_bck else -1)  # icons
            curses.init_pair(12, 33, ColorScheme.__get_bck(12) if show_bck else -1)  # ascii banner
            curses.init_pair(13, 28, ColorScheme.__get_bck(1) if show_bck else -1)

                    
    @staticmethod
    def __get_bck(pair_idx: int) -> int:
        match pair_idx:
            case 8:
                return 28
            case _:
                return 27
            

