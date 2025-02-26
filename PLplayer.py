from player import Player
class PLPlayer(Player):
    def __init__(self, id: int, nameP: str,ga: int,team:str,avg: float):
        Player.__init__(self, id, nameP)
        self.ga = ga
        self.team = team
        self.avg = avg
    def show(self):
        return (f"{self.id}. {self.nameP} - {self.team} - G/A: {self.ga} - average score: {self.avg}\n")