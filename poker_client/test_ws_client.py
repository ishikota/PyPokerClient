from websocket_wrapper import WebSocketWrapper

# const
host = "ws://localhost:3000/cable"
room_id = 1
player_id = 1
credential = "fugafuga"

if __name__ == "__main__":
  websocket = WebSocketWrapper(host, room_id, player_id, credential)
  websocket.run_forever()
