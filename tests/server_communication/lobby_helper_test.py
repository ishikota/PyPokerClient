from tests.base_unittest import BaseUnitTest
from mock import Mock

from nose.tools import *
from poker_client.server_communication.lobby_helper import LobbyHelper

class LobbyHelperTest(BaseUnitTest):

  def setUp(self):
    self.domain = "hoge/"
    self.mock_client = self.httpclient_spy()
    self.lh = LobbyHelper(self.domain, self.mock_client)

  def test_show_rooms(self):
    self.lh.show_rooms()
    path = self.mock_client.get.call_args_list[0][0][0]
    expected_path = self.domain + "rooms"
    self.eq(expected_path, path)

  def test_login_success(self):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id":1, "name":"kota"}
    self.mock_client.get.return_value = mock_response

    res = self.lh.login(1)

    self.true(res['status'])
    self.eq(1, res['player']['id'])
    self.eq('kota', res['player']['name'])

  def test_login_fail(self):
    mock_response = Mock()
    mock_response.status_code = 404
    self.mock_client.get.return_value = mock_response

    res = self.lh.login(1)

    self.false(res['status'])

  def test_create_player(self):
    self.lh.create_player("taro")
    path = self.mock_client.post.call_args_list[0][0][0]
    params = self.mock_client.post.call_args_list[0][0][1]
    expected_path = self.domain + "players"

    self.eq(expected_path, path)
    self.eq(params['player']['name'], "taro")

  def test_create_room(self):
    self.lh.create_room("poka", 3, 6)
    path = self.mock_client.post.call_args_list[0][0][0]
    params = self.mock_client.post.call_args_list[0][0][1]
    expected_path = self.domain + "rooms"

    self.eq(expected_path, path)
    self.eq(params['room']['name'], "poka")
    self.eq(params['room']['max_round'], 3)
    self.eq(params['room']['player_num'], 6)

  def test_destroy_player(self):
    self.lh.destroy_player(53)
    path = self.mock_client.delete.call_args_list[0][0][0]
    expected_path = self.domain + "players/53"
    self.eq(expected_path, path)

  def test_destroy_room(self):
    self.lh.destroy_room(53)
    path = self.mock_client.delete.call_args_list[0][0][0]
    expected_path = self.domain + "rooms/53"
    self.eq(expected_path, path)



  def httpclient_spy(self):
    return Mock()

if __name__ == '__main__':
  unittest.main()
