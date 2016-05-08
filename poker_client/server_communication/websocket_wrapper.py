import websocket
from params_builder import ParamsBuilder
from wanted_phase_handler import WantedPhaseHandler
from poker_phase_handler import PokerPhaseHandler
from close_handler import CloseHandler

class WebSocketWrapper:

  def __init__(self, host, room_id, player_id, credential, poker_player):
    websocket.enableTrace(True)
    self.host = host
    self.state = WantedPhaseHandler.CONNECTING
    self.pb = ParamsBuilder(player_id, room_id, credential)
    self.wanted_handler = WantedPhaseHandler(self.pb)
    self.poker_handler = PokerPhaseHandler(self.pb, poker_player)
    self.close_handler = CloseHandler(self.pb)

  def run_forever(self):
    ws = websocket.WebSocketApp(self.host,
        on_message = self.on_message,
        on_error = self.on_error,
        on_close = self.on_close)
    ws.on_open = self.on_open
    ws.run_forever()


  def on_message(self, ws, message):
    global state

    if self.state >= WantedPhaseHandler.START_POKER:
      self.poker_handler.on_message(self.state, ws, message)
    else:
      self.state = self.wanted_handler.on_message(self.state, ws, message)

  def on_error(self, ws, error):
      print error

  def on_close(self, ws):
      print "[onClose] close websocket"

  def on_open(self, ws):
    ws.send(self.pb.build_subscribe_params())

