import json
import time

class MessageHandler:

  # state
  CONNECTING = 0
  WAITING_DOOR_OPEN = 1
  WAITING_PLAYER_ARRIVAL = 2
  START_POKER = 3

  def __init__(self, params_builder): # pass lobby handler
    self.pb = params_builder

  # Return next state
  def on_message(self, state, ws, msg):
    return self.switch_action_by_message(json.loads(msg), state, ws)

  # FIXIT doing side effect operation (message, websocket.send)
  def switch_action_by_message(self, msg, state, ws):
    if self.type_ping(msg):
      return self.retry_request_if_needed(ws, state)

    elif state == self.CONNECTING:
      if self.type_confirm_subscription(msg):
        self.message_subscription_is_done()
        self.enter_room(ws)
        return self.forward_state(state)

    elif state == self.WAITING_DOOR_OPEN:
      if self.type_welcome(msg['message']):
        self.message_welcome()
        return self.forward_state(state)

    elif state == self.WAITING_PLAYER_ARRIVAL:
      if self.type_player_arrival(msg['message']):
        self.message_member_arrival(msg['message'])
      elif self.type_ready(msg['message']):
        self.message_notify_ready()
        return self.forward_state(state)

    return state

  def retry_request_if_needed(self, ws, state):
    if state == self.WAITING_DOOR_OPEN:
      print '[onMessage] retry enter_room request'
      self.enter_room(ws)
      time.sleep(1)
    return state

  def enter_room(self, ws):
    ws.send(self.pb.build_enter_room_params())

  def message_subscription_is_done(self):
    print '[onMessage] your subscription request is accepted!!'
    print '[onMessage] So move to OPENING_DOOR state'
    print '[onMessage] now trying to enter poker room...'

  def message_welcome(self):
    print '[onMessage] you are in the room !! please wait for other player\'s arrival.'

  def message_member_arrival(self, msg):
    print '[onMessage] Player arrived!! ' + msg['message']

  def message_notify_ready(self):
    print '[onMessage] Hey!! Everything is ready!! Let\'s poker!!'

  def type_ping(self, msg):
    return msg['identifier'] == '_ping'

  def type_confirm_subscription(self, msg):
    return msg['identifier'] == '{"channel":"RoomChannel"}' and \
        msg['type'] == 'confirm_subscription'

  def type_player_arrival(self, msg):
    return msg['phase'] == 'member_wanted' and msg['type'] == 'arrival'

  def type_welcome(self, msg):
    return msg['phase'] == 'member_wanted' and msg['type'] == 'welcome'

  def type_ready(self, msg):
    return msg['phase'] == 'member_wanted' and msg['type'] == 'ready'

  def forward_state(self, state):
    return state + 1

