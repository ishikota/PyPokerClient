import json

class PokerPhaseHandler:

  # state
  PLAY_POKER = 4

  def __init__(self, params_builder, poker_algorithm):
    self.pb = params_builder
    self.pa = poker_algorithm

  # Return next state
  def on_message(self, state, ws, msg):
    return self.switch_action_by_message(json.loads(msg), state, ws)

  # FIXIT doing side effect operation (message, websocket.send)
  def switch_action_by_message(self, msg, state, ws):
    if self.type_ping(msg):
      return self.retry_request_if_needed(ws, state)

    if self.type_ask(msg['message']):
      act_data = self.pa.receive_data(msg["message"])
      self.declare_action(ws, act_data)
    elif self.type_notification(msg['message']):
      self.pa.receive_data(msg["message"])

    return state

  def retry_request_if_needed(self, ws, state):
    # TODO Implment
    return state

  def declare_action(self, ws, act_data):
    ws.send(self.pb.build_declare_action_params(act_data))

  def type_ping(self, msg):
    return msg['identifier'] == '_ping'

  def type_ask(self, msg):
    return msg['phase'] == 'play_poker' and msg['type'] == 'ask'

  def type_notification(self, msg):
    return msg['phase'] == 'play_poker' and msg['type'] == 'notification'

  def forward_state(self, state):
    return state + 1

