import json

from server_communication.http_client import CustomHttpClient
from server_communication.lobby_helper import LobbyHelper
from server_communication.websocket_wrapper import WebSocketWrapper

http_host = 'http://localhost:3000/api/v1/'
ws_host = "ws://localhost:3000/cable"

http_client = CustomHttpClient()
lobby = LobbyHelper(http_host, http_client)

def registration():
  name = raw_input("Input your name... >>> ")
  player = lobby.create_player(name)
  print "OK! You are succesfully registered!!"
  print "Player INFO : " + str(player)
  return player

def login():
  pid = int(raw_input("Input your id >>> "))
  res = lobby.login(pid)
  if res['status']:
    return res['player']
  else:
    raise Exception("Login failed")

def create_room():
  name = raw_input("Input the name of new room >>> ")
  max_round = int(raw_input("Input the number of round to play >>> "))
  player_num = int(raw_input("Input the number of player to play with >>> "))
  print "Creating new room..."
  room = lobby.create_room(name, max_round, player_num)
  print "OK! New room is succesfully created!!"
  print "Room INFO : " + str(room)
  return room

def show_rooms():
  print "Fetching available rooms..."
  rooms = lobby.show_rooms().text
  to_s = lambda r : "id : " + str(r["id"]) + ", name : " + r["name"] + ", round : " + str(r["max_round"]) + ", player num : " + str(r["player_num"])
  parse = lambda s : json.loads(s)
  info_list = map(to_s, map(parse, json.loads(rooms)))

  print "[ Available Rooms ]"
  for info in info_list:
    print info
  print ""

def select_room():
  return int(raw_input("Input the room id which you want to enter >>> "))


player = None
flg = raw_input("Input Login(l) or register(r) >> ")
if flg == 'r':
  player = registration()
else:
  player = login()

show_rooms()
flg = raw_input("Create new room? (y/n)")
if flg == 'y':
  create_room()
credential = "a" * 22  # TODO should receive when player is created
room_id = select_room()

websocket = WebSocketWrapper(ws_host, room_id, player["id"], credential)
websocket.run_forever()

