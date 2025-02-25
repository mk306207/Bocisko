class Team:
    def __init__(self,team_name: str,team_position: int,team_wins: int, team_draws: int, team_loses: int, team_points: int):
        self.team_name = team_name
        self.team_position = team_position
        self.team_wins = team_wins
        self.team_draws = team_draws
        self.team_loses = team_loses
        self.team_points = team_points
        
    def show(self):
        return(f"{self.team_position}. {self.team_name}   {self.team_wins}-{self.team_draws}-{self.team_loses} --- {self.team_points}pkt")