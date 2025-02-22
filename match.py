class Match:
    def __init__(self, id: int, teams: str, score: str):
        self.id = id
        self.teams = teams
        self.score = score
    def showMatch(self):
        return(f"{self.teams} -> {self.score}")