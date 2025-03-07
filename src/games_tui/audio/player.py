import os
import subprocess
import platformdirs

from enum import Enum
from config.settings import settings


class Sound(Enum):
    CARD_DEAL = "card_deal"
    CARD_FLIP = "card_flip"
    CARD_PLACE = "card_place"
    SOLITAIRE_WIN = "solitaire_win"
    RUBIKS = "rubiks"
    RUBIKS_SHUFFLE = "rubiks_shuffle"
    RUBIKS_WIN = "rubiks_win"
    INVALID_1 = "invalid_1"


class Player:

    data_dir = platformdirs.user_data_dir("games-tui") 
    player = None

    @classmethod
    def initialize(cls) -> None:
        """
        Initializes player for playing stuff.
        """
        # windows:

        if os.name == "nt":
            cls.player = "wmplayer"

        # macos / linux:

        elif os.name == "posix":
            if os.system("command -v mpg123 > /dev/null") == 0:
                cls.player = "mpg123"
            elif os.system("command -v ffplay > /dev/null") == 0:
                cls.player = "ffplay -nodisp -autoexit"
            else:
                raise Exception("No player found.")
        else:
            raise Exception("Unsupported OS.")
                
        
    @staticmethod
    def play(sound: Sound) -> None:
        """
        Plays sound effect.
        """
        if Player.player is None:
            Player.initialize()
        
        if not settings.sound_effects_enabled:
            return

        sound_path = os.path.join(Player.data_dir, "sounds", f"{sound.value}.mp3") 
        
        subprocess.Popen(
            [Player.player, sound_path], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
