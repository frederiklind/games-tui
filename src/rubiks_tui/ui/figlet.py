import os

from typing import List
from config.settings import settings


class Figlet:
    """

    """

    @staticmethod
    def title() -> list[str]:
        return [
            "________       ______ ___________ ___            ____________  _________ ",
            "___  __ \\___  ____  /____(_)__  /__( )_______    ___  __/_  / / /___  _/ ",
            "__  /_/ /  / / /_  __ \\_  /__  //_/|/__  ___/    __  /  _  / / / __  /   ",
            "_  _, _// /_/ /_  /_/ /  / _  ,<     _(__  )     _  /   / /_/ / __/ /    ",
            "/_/ |_| \\__,_/ /_.___//_/  /_/\\|_|    /____/     /_/    \\____/  /___/    ",
            "",
        ]
    
    @staticmethod
    def get_from_file(filename: str) -> List[str]:
        """

        """
        with open(os.path.join(settings.dir(), "ascii", f"{filename}.txt"), "r") as f:
            return [line for line in f]
