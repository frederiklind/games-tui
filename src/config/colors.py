import toml
import re

class Color(object):
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

    # def __init__(self, r: int, g: int, b: int) -> None:
    #     """
    #
    #     """
    #     self.r = self.__to_curses_color(r)
    #     self.g = self.__to_curses_color(g)
    #     self.b = self.__to_curses_color(b)

    def __init__(self, rgb: str) -> None:
        """

        """
        nums = re.findall(r'\d+', rgb)
        r, g, b = map(int, nums)
        self.r = self.__to_curses_color(r)
        self.g = self.__to_curses_color(g)
        self.b = self.__to_curses_color(b)

    def __to_curses_color(self, x: int) -> int:
        """
        Converts RGB Values to curses compatible values.

        Args:
            x: (int): R, G, or B value for a color.

        Returns:
            
        """
        return x // 255 * 1000
    

class ColorScheme(object):
    """
    Coloscheme for the UI.

    Attributes:
        window_background (Color): Background color for the cube
        side_pane_background (Color): Background color for side panes of game screen.
        header_background (Color): Background color for side pane headers, etc.
        icon_color (Color): Color of UI icons.
        ui_text (Color): UI text color, both passive elements, and selectable elements in non-selected state.
        ui_selected_text (Color): UI text color for selectable elements in selected state.
        header_text (Color): Color of header text.
        ascii_title (Color): Color of the ascii banner on the splash screen.
        cube_top (Color): Color of Rubik's cube top face (default: white).
        cube_bottom (Color): Color of Rubik's cube top face (default: yellow).
        cube_left (Color): Color of Rubik's cube left face (default: green).
        cube_right (Color): Color of Rubik's cube right face (default: blue).
        cube_front (Color): Color of Rubik's cube front face (default: red).
        cube_back (Color): Color of Rubik's cube back face (default: orange).
    """
    window_background: Color
    side_pane_background: Color
    header_background: Color
    ui_text: Color
    ui_selected_text: Color
    header_text: Color
    icon_color: Color
    ascii_title: Color
    cube_top: Color
    cube_bottom: Color
    cube_left: Color
    cube_right: Color
    cube_front: Color
    cube_back: Color

    def __init__(self, scheme: str) -> None:
        """

        """
        self.load_from_file(scheme)
    
    def load_from_file(self, scheme: str) -> None:
        """
        Loads colorscheme from toml file in user's config directory,
        and sets colorscheme state from toml data.

        Args:
            scheme (str): name of the colorscheme to load (filename).
        """
        with open('', 'r') as f:
            scheme = toml.load(f)
        
        self.window_background = Color(scheme['window']['window_background'])
        self.side_pane_background = Color(scheme['window']['side_pane_background'])
        self.header_background = Color(scheme['header']['header_background'])
        self.header_text = Color(scheme['header']['header_text'])
        self.ui_text = Color(scheme['text']['ui_text'])
        self.ui_selected_text = Color(scheme['text']['ui_selected_text'])
        self.icon_color = Color(scheme['text']['icon_color'])
        self.ascii_title = Color(scheme['text']['ascii_title'])
        self.cube_top = Color(scheme['cube']['cube_top'])
        self.cube_bottom = Color(scheme['cube']['cube_bottom'])
        self.cube_left = Color(scheme['cube']['cube_left'])
        self.cube_right = Color(scheme['cube']['cube_right'])
        self.cube_front = Color(scheme['cube']['cube_front'])
        self.cube_back = Color(scheme['cube']['cube_back'])
