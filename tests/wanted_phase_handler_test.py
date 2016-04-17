from base_unittest import BaseUnitTest
import json
from mock import Mock

from nose.tools import *
from poker_client.wanted_phase_handler import WantedPhaseHandler
from poker_client.params_builder import ParamsBuilder

class WantedPhaseHandlerTest(BaseUnitTest):

  def setUp(self):
    self.pb = self.params_builder_mock()
    self.wh = WantedPhaseHandler(self.pb)

  def test_switch_action_msg_connecting(self):
    ws = self.websocket_spy()
    next_state = self.wh.switch_action_by_message(\
        self.confirm_subscription(), self.wh.CONNECTING, ws)
    args = ws.send.call_args_list[0][0][0]

    self.eq(self.wh.WAITING_DOOR_OPEN, next_state)
    self.eq(self.mock_enter_room_msg(), args)

  def test_switch_action_msg_waiting_door_open(self):
    ws = self.websocket_spy()
    next_state = self.wh.switch_action_by_message(\
        self.welcome(), self.wh.WAITING_DOOR_OPEN, ws)

    self.eq(self.wh.WAITING_PLAYER_ARRIVAL, next_state)

  def test_switch_action_msg_arrival(self):
    ws = self.websocket_spy()
    next_state = self.wh.switch_action_by_message(\
        self.arrival(), self.wh.WAITING_PLAYER_ARRIVAL, ws)

    self.eq(self.wh.WAITING_PLAYER_ARRIVAL, next_state)

  def test_switch_action_msg_ready(self):
    ws = self.websocket_spy()
    next_state = self.wh.switch_action_by_message(\
        self.ready(), self.wh.WAITING_PLAYER_ARRIVAL, ws)

    self.eq(self.wh.START_POKER, next_state)

  def test_retry_request_if_needed(self):

    # do not retry
    ws = self.websocket_spy()
    self.wh.retry_request_if_needed(ws, 0)
    self.eq(ws.send.call_count, 0)

    # resend expected message
    ws = self.websocket_spy()
    next_state = self.wh.retry_request_if_needed(ws, WantedPhaseHandler.WAITING_DOOR_OPEN)
    self.eq(ws.send.call_count, 1)
    args = ws.send.call_args_list[0][0][0]
    self.eq(self.mock_enter_room_msg(), args)

  def test_type_ping(self):
    self.true(self.wh.type_ping(self.ping()))
    self.false(self.wh.type_ping(self.confirm_subscription()))

  def test_type_confirm_subscription(self):
    self.true(self.wh.type_confirm_subscription(self.confirm_subscription()))
    self.false(self.wh.type_confirm_subscription(self.ping()))

  def test_type_welcome(self):
    self.true(self.wh.type_welcome(self.welcome()["message"]))
    self.false(self.wh.type_welcome(self.arrival()["message"]))

  def test_type_arrival(self):
    self.true(self.wh.type_player_arrival(self.arrival()["message"]))
    self.false(self.wh.type_player_arrival(self.welcome()["message"]))

  def test_type_ready(self):
    self.true(self.wh.type_ready(self.ready()["message"]))
    self.false(self.wh.type_ready(self.arrival()["message"]))

  def test_forward_state(self):
    self.eq(2, self.wh.forward_state(1))
    self.eq(3, self.wh.forward_state(self.wh.forward_state(1)))

  def ping(self):
    return json.loads('{"identifier":"_ping","message":1460779289}')

  def confirm_subscription(self):
    return json.loads(r'{"identifier":"{\"channel\":\"RoomChannel\"}","type":"confirm_subscription"}')

  def welcome(self):
    return json.loads(r'{"identifier":"{\"channel\":\"RoomChannel\"}", "message" : { "phase":"member_wanted", "type":"welcome"} }')

  def arrival(self):
    return json.loads(r'{"identifier":"{\"channel\":\"RoomChannel\"}", "message" : { "phase":"member_wanted", "type":"arrival", "message":"TODO"} }')

  def ready(self):
    return json.loads(r'{"identifier":"{\"channel\":\"RoomChannel\"}", "message" : { "phase":"member_wanted", "type":"ready"} }')

  def websocket_spy(self):
    websocket = Mock()
    websocket.send.return_value = None
    return websocket

  def params_builder_mock(self):
    pb = Mock()
    pb.build_enter_room_params.return_value = self.mock_enter_room_msg()
    return pb

  def mock_enter_room_msg(self):
    return "enter_room"

if __name__ == '__main__':
  unittest.main()
