from tests.base_unittest import BaseUnitTest
import json
from nose.tools import *

from poker_client.server_communication.params_builder import ParamsBuilder

class ParamsBuilderTest(BaseUnitTest):

  def setUp(self):
    self.player_id = 53
    self.room_id = 7
    self.credential = 'a' * 22
    self.pb = ParamsBuilder(self.player_id, self.room_id, self.credential)

  def test_build_subscribe_param(self):
    p = json.loads(self.pb.build_subscribe_params())
    self.eq(p["command"], "subscribe")

  def test_build_enter_room_params(self):
    p = json.loads(self.pb.build_enter_room_params())
    d = json.loads(p["data"])
    self.eq(p["command"], "message")
    self.eq(d["action"], "enter_room")

  def test_build_exit_room_params(self):
    p = json.loads(self.pb.build_exit_room_params())
    d = json.loads(p["data"])
    self.eq(p["command"], "message")
    self.eq(d["action"], "exit_room")

  def test_build_my_params(self):
    p = json.loads(self.pb.build_my_params("c"))
    d = json.loads(p["data"])
    self.eq(p["command"], "c")
    self.eq(p["identifier"], self.room_identifier())
    self.eq(d["player_id"], self.player_id)
    self.eq(d["room_id"], self.room_id)
    self.eq(d["credential"], self.credential)

  def room_identifier(self):
    return r'{"channel":"RoomChannel"}'

if __name__ == '__main__':
  unittest.main()

