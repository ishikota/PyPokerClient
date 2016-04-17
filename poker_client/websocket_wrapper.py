import websocket
from params_builder import ParamsBuilder
from message_handler import MessageHandler

class WebSocketWrapper:

  def __init__(self, host, room_id, player_id, credential):
    websocket.enableTrace(True)
    self.host = host
    self.state = MessageHandler.CONNECTING
    self.pb = ParamsBuilder(player_id, room_id, credential)
    self.msg_handler = MessageHandler(self.pb)

  def run_forever(self):
    ws = websocket.WebSocketApp(self.host,
        on_message = self.on_message,
        on_error = self.on_error,
        on_close = self.on_close)
    ws.on_open = self.on_open
    ws.run_forever()


  def on_message(self, ws, message):
    global state
    self.state = self.msg_handler.on_message(self.state, ws, message)

  def on_error(self, ws, error):
      print error

  def on_close(self, ws):
      print "[onClose] close websocket"

  def on_open(self, ws):
    ws.send(self.pb.build_subscribe_params())

