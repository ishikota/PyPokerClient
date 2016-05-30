import json

from server_communication.http_client import CustomHttpClient
from server_communication.lobby_helper import LobbyHelper
from server_communication.websocket_wrapper import WebSocketWrapper

class PokerRunner:

  HTTP_HOST = 'http://localhost:3000/api/v1/'
  WS_HOST = 'ws://localhost:3000/cable'

  def run(self, poker_player):
    http_client = CustomHttpClient()
    lobby = LobbyHelper(self.HTTP_HOST, http_client)
    player_info = self.login_or_registration(lobby)
    self.show_rooms(lobby)
    self.create_room_if_needed(lobby)
    room_id = self.ask_room_id()
    credential = "not used now"

    websocket = WebSocketWrapper(
        self.WS_HOST, room_id, player_info["id"], credential, poker_player)
    websocket.run_forever()

  def login_or_registration(self, lobby):
    flg = raw_input("Input Login(l) or register(r) >> ")
    return self.registration() if flg == 'r' else self.login(lobby)

  def registration(self, lobby):
    name = raw_input("Input your name... >>> ")
    player = lobby.create_player(name)
    print "OK! You are succesfully registered!!"
    print "Player INFO : " + str(player)
    return player

  def login(self, lobby):
    pid = int(raw_input("Input your id >>> "))
    res = lobby.login(pid)
    if res['status']:
      return res['player']
    else:
      raise Exception("Login failed")

  def create_room_if_needed(self, lobby):
    flg = raw_input("Create new room? (y/n)")
    if flg == 'y':
      self.create_room(lobby)


  def create_room(self, lobby):
    name = raw_input("Input the name of new room >>> ")
    max_round = int(raw_input("Input the number of round to play >>> "))
    player_num = int(raw_input("Input the number of player to play with >>> "))
    print "Creating new room..."
    room = lobby.create_room(name, max_round, player_num)
    print "OK! New room is succesfully created!!"
    print "Room INFO : " + str(room)
    return room

  def show_rooms(self, lobby):
    print "Fetching available rooms..."
    rooms = lobby.show_rooms().text
    to_s = lambda r : "id : " + str(r["id"]) + ", name : " + r["name"] + ", round : " + str(r["max_round"]) + ", player num : " + str(r["player_num"])
    parse = lambda s : json.loads(s)
    info_list = map(to_s, map(parse, json.loads(rooms)))

    print "[ Available Rooms ]"
    for info in info_list:
      print info
    print ""

  def ask_room_id(self):
    return int(raw_input("Input the room id which you want to enter >>> "))

