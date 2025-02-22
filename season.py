class Season:
    def __init__(self, id: int, name: str, finished: int):
        self.id = id
        self.name = name
        self.finished = finished

    def showSeason(self):
        if self.finished == 0:
            finish= "finished"
        else:
            finish = "pending"
        return(f"id:{self.id} - name:{self.name} and it is {finish}")