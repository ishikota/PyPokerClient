import json

class PokerPhaseHandler:

  # state
  PLAY_POKER = 4
  FINISH_POKER = 5

  def __init__(self, params_builder, poker_player):
    self.pb = params_builder
    self.pp = poker_player

  # Return next state
  def on_message(self, state, ws, msg):
    return self.switch_action_by_message(json.loads(msg), state, ws)

  # FIXIT doing side effect operation (message, websocket.send)
  def switch_action_by_message(self, data, state, ws):
    if self.type_ping(data):
      return self.retry_request_if_needed(ws, state)

    msg = data["message"]
    if self.type_ask(msg):
      action, amount = self.pp.respond_to_ask(msg["message"])
      self.declare_action(ws, action, amount)
    elif self.type_notification(msg):
      self.pp.receive_notification(msg["message"])
      if msg["message"]["message_type"] == 'game_result_message':
        state = self.FINISH_POKER

    return state

  def retry_request_if_needed(self, ws, state):
    # TODO Implment
    return state

  def declare_action(self, ws, action, amount):
    ws.send(self.pb.build_declare_action_params(action, amount))

  def type_ping(self, msg):
    return msg['identifier'] == '_ping'

  def type_ask(self, msg):
    return msg['phase'] == 'play_poker' and msg['type'] == 'ask'

  def type_notification(self, msg):
    return msg['phase'] == 'play_poker' and msg['type'] == 'notification'

  def forward_state(self, state):
    return state + 1

