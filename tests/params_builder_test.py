import unittest
import json
from nose.tools import *

from poker_client.params_builder import ParamsBuilder

class ParamsBuilderTest(unittest.TestCase):

  def setUp(self):
    self.player_id = 53
    self.room_id = 7
    self.credential = 'a' * 22
    self.pb = ParamsBuilder(self.player_id, self.room_id, self.credential)

  def test_build_subscribe_param(self):
    p = json.loads(self.pb.build_subscribe_params())
    self.assertEqual(p["command"], "subscribe")

  def test_build_enter_room_params(self):
    p = json.loads(self.pb.build_enter_room_params())
    d = json.loads(p["data"])
    self.assertEqual(p["command"], "message")
    self.assertEqual(d["action"], "enter_room")

  def test_build_my_params(self):
    p = json.loads(self.pb.build_my_params("c"))
    d = json.loads(p["data"])
    self.assertEqual(p["command"], "c")
    self.assertEqual(p["identifier"], self.room_identifier())
    self.assertEqual(d["player_id"], self.player_id)
    self.assertEqual(d["room_id"], self.room_id)
    self.assertEqual(d["credential"], self.credential)

  def room_identifier(self):
    return r'{"channel":"RoomChannel"}'

if __name__ == '__main__':
  unittest.main()

