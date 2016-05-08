from server_communication.http_client import CustomHttpClient

class LobbyHelper:

  def __init__(self, domain, http_client):
    self.c = http_client
    self.domain = domain

  def show_rooms(self, status=''):
    params = { 'status' : status }
    return self.c.get(self.domain + 'rooms', params)

  def login(self, pid):
    response = self.c.get(self.domain + 'players/' + str(pid))
    if response.status_code == 200:
      return { 'status' : True, 'player' : response.json() }
    else:
      return { 'status' : False }

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

