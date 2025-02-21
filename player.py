class Player:
    def __init__(self, id: int, nameP: str):
        self.id = id
        self.nameP = nameP
    def showPlayer(self):
        return (f"{self.nameP} - {self.id}\n")