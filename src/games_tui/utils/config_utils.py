from typing import Tuple


class ConfigUtils:
    """
    Configuration utility class.
    """
    
    @staticmethod
    def get_toml_headers(idx: int) -> Tuple[str, str]:
        """
        Gets the tome section and header strings by the setting index.

        Args:
            idx (int): The index of the selected setting.
        Returns:
            Tuple[str, str]: A tuple consaining the toml section and header string.
        """
        match idx:
            case 0:
                return ("ui_display", "color_scheme")
            case 1:
                return ("ui_display", "ascii_banner")
            case 2:
                return ("ui_display", "show_background")
            case 3:
                return ("ui_display", "show_ui_borders")
            case 4:
                return ("controls", "alt_keys")
