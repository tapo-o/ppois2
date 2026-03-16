class Athlete:
    def __init__(self, full_name, squad, position, titles, sport, rank):
        self.full_name = str(full_name)
        self.squad = str(squad)
        self.position = str(position)
        try:
            self.titles = int(titles)
        except:
            self.titles = 0
        self.sport = str(sport)
        self.rank = str(rank)