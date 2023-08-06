"""Match helpers"""

def is_concede(data):
    """Given match data returns True if the match was conceded"""
    if (data['match']['teams'][0]['mvp'] == 2
            or data['match']['teams'][1]['mvp'] == 2):
        return True
    return False

class Match:
    def __init__(self,data):
      self.data = data

    def uuid(self):
      return self.data['uuid']
    
    def competition(self):
      return self.data['match']['competitionname']

    def competition_id(self):
      return self.data['match']['idcompetition']

    def coach1(self):
      return self.data['match']['coaches'][0]

    def coach2(self):
      return self.data['match']['coaches'][1]

    def team1(self):
      return self.data['match']['teams'][0]

    def team2(self):
      return self.data['match']['teams'][1]

    def winner(self):
      if self.team1()['inflictedtouchdowns'] > self.team2()['inflictedtouchdowns']:
        return self.coach1()
      elif self.team1()['inflictedtouchdowns'] < self.team2()['inflictedtouchdowns']:
        return self.coach2()
      else:
        return None

    def is_concede(self):
      return is_concede(self.data)