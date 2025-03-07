import sqlite3

from typing import List


class Database:
    """

    """
    con_str = "connectionstr"

    
    @staticmethod
    def get_achievements(game: str) -> str:
        pass


    @staticmethod
    def get_highscores(game: str) -> List[str]:
        conn = sqlite3.connect(Database.con_str)

    
    @staticmethod
    def create_init() -> None
        """
        Creates the initial database.
        """
        conn = sqlite3.connect(Database.con_str)
        cursor = conn.cursor()
        
        cursor.execute()

