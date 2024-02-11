

class JuryReport:

    def __init__(self):
        self.points = {}
        self.story_of_game = []
        self.status = "OK"


    def error_occured(self):
        self.status = "ERROR"


    def add_points(self, player, player_points):
        self.points[player] = player_points


    def add_story(self, position, move):
        self.story_of_game.append(position)
        self.story_of_game.append(move)