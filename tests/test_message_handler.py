import unittest
import json
from mock import Mock

from nose.tools import *
from poker_client.message_handler import MessageHandler
from poker_client.params_builder import ParamsBuilder

class MessageHandlerTest(unittest.TestCase):

  def setUp(self):
    self.pb = self.params_builder_mock()
    self.mh = MessageHandler(self.pb)

  def test_switch_action_ping(self):
    for state in range(3):
      ws = self.websocket_spy()
      next_state = self.mh.switch_action_by_message(self.ping(), state, ws)
      self.assertEqual(state, next_state)

  def test_retry_request_if_needed(self):

    # do not retry
    ws = self.websocket_spy()
    self.mh.retry_request_if_needed(ws, 0)
    self.assertEqual(ws.send.call_count, 0)

    # resend expected message
    ws = self.websocket_spy()
    next_state = self.mh.retry_request_if_needed(ws, MessageHandler.WAITING_DOOR_OPEN)
    self.assertEqual(ws.send.call_count, 1)
    args = ws.send.call_args_list[0][0][0]
    self.assertEqual(self.mock_enter_room_msg(), args)

  def test_type_ping(self):
    self.assertTrue(self.mh.type_ping(self.ping()))
    self.assertFalse(self.mh.type_ping(self.confirm_subscription()))

  def test_type_confirm_subscription(self):
    self.assertTrue(self.mh.type_confirm_subscription(self.confirm_subscription()))
    self.assertFalse(self.mh.type_confirm_subscription(self.ping()))

  def test_type_welcome(self):
    self.assertTrue(self.mh.type_welcome(self.welcome()))
    self.assertFalse(self.mh.type_welcome(self.arrival()))

  def test_type_arrival(self):
    self.assertTrue(self.mh.type_player_arrival(self.arrival()))
    self.assertFalse(self.mh.type_player_arrival(self.welcome()))

  def test_forward_state(self):
    self.assertEqual(2, self.mh.forward_state(1))
    self.assertEqual(3, self.mh.forward_state(self.mh.forward_state(1)))

  def ping(self):
    return json.loads('{"identifier":"_ping","message":1460779289}')

  def confirm_subscription(self):
    return json.loads(r'{"identifier":"{\"channel\":\"RoomChannel\"}","type":"confirm_subscription"}')

  def welcome(self):
    return json.loads(r'{"phase":"member_wanted", "type":"welcome"}')

  def arrival(self):
    return json.loads(r'{"phase":"member_wanted", "type":"arrival", "message":"TODO"}')

  def websocket_spy(self):
    websocket = Mock()
    websocket.send.return_value = None
    return websocket

  def params_builder_mock(self):
    pb = Mock()
    pb.build_message_params.return_value = self.mock_enter_room_msg()
    return pb

  def mock_enter_room_msg(self):
    return "enter_room"

if __name__ == '__main__':
  unittest.main()
