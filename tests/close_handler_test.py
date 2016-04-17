from base_unittest import BaseUnitTest
from mock import Mock

from poker_client.close_handler import CloseHandler

class MessageHandlerTest(BaseUnitTest):

  def setUp(self):
    self.pb = self.params_builder_mock()
    self.ch = CloseHandler(self.pb)

  def test_exit_room(self):
    ws = self.websocket_spy()
    self.ch.exit_room(ws)
    args = ws.send.call_args_list[0][0][0]

    self.eq(self.mock_exit_room_msg(), args)

  def params_builder_mock(self):
    pb = Mock()
    pb.build_exit_room_params.return_value = self.mock_exit_room_msg()
    return pb

  def mock_exit_room_msg(self):
    return "exit_room"

  def websocket_spy(self):
    websocket = Mock()
    websocket.send.return_value = None
    return websocket

