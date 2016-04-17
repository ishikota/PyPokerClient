import unittest
import json

from nose.tools import *
from poker_client.message_handler import MessageHandler
from poker_client.params_builder import ParamsBuilder

class MessageHandlerTest(unittest.TestCase):

  def setUp(self):
    self.player_id = 53
    self.room_id = 7
    self.credencial = 'a' * 22
    self.pb = ParamsBuilder(self.player_id, self.room_id, self.credencial)
    self.mh = MessageHandler(self.pb)

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


if __name__ == '__main__':
  unittest.main()
