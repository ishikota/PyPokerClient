class CloseHandler:

  def __init__(self, params_builder):
    self.pb = params_builder

  def on_close(self, ws):
    return self.exit_room(ws)

  def exit_room(self, ws):
    ws.send(self.pb.build_exit_room_params())

