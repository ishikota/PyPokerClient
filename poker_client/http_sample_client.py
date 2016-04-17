from http_client import CustomHttpClient
from lobby_helper import LobbyHelper

host = 'http://localhost:3000/'
domain = host + 'api/v1/'

if __name__ == '__main__':
  http_client = CustomHttpClient()
  lobby = LobbyHelper(domain, http_client)
  player = lobby.create_player('kota')
  room = lobby.create_room('pokapoka', 5, 3)
  lobby.show_rooms()
  lobby.destroy_room(room['id'])
  lobby.destroy_player(player['id'])