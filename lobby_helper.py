from http_client import CustomHttpClient

class LobbyHelper:

  def __init__(self, domain):
    self.c = CustomHttpClient()
    self.domain = domain

  def show_rooms(self, status=''):
    params = { 'status' : status }
    return self.c.get(self.domain + 'rooms', params)

  def create_player(self, name):
    params = { 'player' : { 'name' : name } }
    r = self.c.post(self.domain + 'players', params)
    return r.json()

  def create_room(self, name, max_round, player_num):
    params = { 'room' : { 'name' : name, 'max_round' : max_round, 'player_num' : player_num } }
    r = self.c.post(self.domain + 'rooms', params)
    return r.json()

  def destroy_player(self, pid):
    return self.c.delete(self.domain + 'players/' + str(pid))

  def destroy_room(self, rid):
    return self.c.delete(self.domain + 'rooms/' + str(rid))

