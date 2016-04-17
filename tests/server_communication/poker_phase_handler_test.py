from base_unittest import BaseUnitTest
import json
from mock import Mock

from nose.tools import *
from poker_client.server_communication.poker_phase_handler import PokerPhaseHandler

class WantedPhaseHandlerTest(BaseUnitTest):

  def setUp(self):
    self.pb = self.params_builder_mock()
    self.pa = self.algo_mock()
    self.ph = PokerPhaseHandler(self.pb, self.pa)

  def test_switch_action_when_ask(self):
    ws = self.websocket_spy()
    msg = self.ask()
    state = PokerPhaseHandler.PLAY_POKER

    next_state = self.ph.switch_action_by_message(msg, state, ws)

    pa_args = self.pa.receive_data.call_args_list[0][0][0]
    ws_args = ws.send.call_args_list[0][0][0]
    self.eq(PokerPhaseHandler.PLAY_POKER, next_state)
    self.eq(msg["message"]["data"], pa_args)
    self.eq(self.mock_declare_action_msg(), ws_args)

  def test_switch_action_when_notification(self):
    ws = self.websocket_spy()
    msg = self.notification()
    state = PokerPhaseHandler.PLAY_POKER

    next_state = self.ph.switch_action_by_message(msg, state, ws)

    pa_args = self.pa.receive_data.call_args_list[0][0][0]
    self.eq(PokerPhaseHandler.PLAY_POKER, next_state)
    self.eq(msg["message"]["data"], pa_args)
    self.eq(ws.send.call_count, 0)

  def test_retry_request_if_needed(self):
    pass # TODO

  def test_type_ping(self):
    self.true(self.ph.type_ping(self.ping()))
    self.false(self.ph.type_ping(self.ask()))

  def test_type_ask(self):
    self.true(self.ph.type_ask(self.ask()["message"]))
    self.false(self.ph.type_ask(self.notification()["message"]))

  def test_type_notification(self):
    self.true(self.ph.type_notification(self.notification()["message"]))
    self.false(self.ph.type_notification(self.ask()["message"]))

  def test_forward_state(self):
    self.eq(2, self.ph.forward_state(1))
    self.eq(3, self.ph.forward_state(self.ph.forward_state(1)))

  def ping(self):
    return json.loads('{"identifier":"_ping","message":1460779289}')

  def ask(self):
    return json.loads(r'{"identifier":"{\"channel\":\"RoomChannel\"}", "message" : { "phase":"play_poker", "type":"ask", "data":"hoge" } }')

  def notification(self):
    return json.loads(r'{"identifier":"{\"channel\":\"RoomChannel\"}", "message" : { "phase":"play_poker", "type":"notification", "data":"fuga" } }')


  def websocket_spy(self):
    websocket = Mock()
    websocket.send.return_value = None
    return websocket

  def params_builder_mock(self):
    pb = Mock()
    pb.build_declare_action_params.return_value = self.mock_declare_action_msg()
    return pb

  def algo_mock(self):
    algo = Mock()
    algo.receive_data.return_value = self.mock_algo_return()
    return algo

  def mock_declare_action_msg(self):
    return "declare_action"

  def mock_algo_return(self):
    return "some_action"

if __name__ == '__main__':
  unittest.main()

