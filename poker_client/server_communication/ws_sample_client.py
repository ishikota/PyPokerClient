from players.template_poker_player import TemplatePokerPlayer
from players.human_poker_player import HumanPokerPlayer
from server_communication.websocket_wrapper import WebSocketWrapper

# const
host = "ws://localhost:3000/cable"

if __name__ == "__main__":
  player_id = int(raw_input("player_id >> "))
  room_id = int(raw_input("room_id >> "))
  credential = "fugafuga"
  #poker_player = TemplatePokerPlayer()
  poker_player = HumanPokerPlayer()
  websocket = WebSocketWrapper(host, room_id, player_id, credential, poker_player)
  websocket.run_forever()
