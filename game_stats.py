import pyodbc

class GameStats:
    """Track statistics for Alien Invasion."""
    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        # High score should never be reset.
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def save_score(self, player_name):
        """Save the current score to the database."""
        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=HIEU_DATA;'
                'DATABASE=alien_invasion;'
                'Trusted_Connection=yes'
            )
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO PlayerScores (player_name, score) VALUES (?, ?)",
                (player_name, self.score)
            )
            conn.commit()
            conn.close()
            print("Score saved successfully!")
        except pyodbc.Error as e:
            print("Error saving score:", e)