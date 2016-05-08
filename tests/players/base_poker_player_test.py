from tests.base_unittest import BaseUnitTest
from mock import Mock
from poker_client.players.base_poker_player import BasePokerPlayer
from tests.players.message_builder import *

class BasePokerPlayerTest(BaseUnitTest):

  def setUp(self):
    self.player = BasePokerPlayer()


  def test_respond_to_ask(self):
    msg = ask_message("h", "v", "r", "a")
    method = self.player.respond_to_ask
    self.__check_err(msg, method, "declare_action")

  def test_receive_game_start(self):
    msg = game_start_message("g")
    method = self.player.receive_notification
    self.__check_err(msg, method, "receive_game_start_message")

  def test_receive_round_start(self):
    msg = round_start_message("s", "h")
    method = self.player.receive_notification
    self.__check_err(msg, method, "receive_round_start_message")

  def test_receive_street_start(self):
    msg = street_start_message("s", "r")
    method = self.player.receive_notification
    self.__check_err(msg, method, "receive_street_start_message")

  def test_receive_game_update(self):
    msg = game_update_message("a", "r", "h")
    method = self.player.receive_notification
    self.__check_err(msg, method, "receive_game_update_message")

  def test_receive_round_result(self):
    msg = round_result_message("w", "r")
    method = self.player.receive_notification
    self.__check_err(msg, method, "receive_round_result_message")

  def test_receive_game_result(self):
    msg = game_result_message("s")
    method = self.player.receive_notification
    self.__check_err(msg, method, "receive_game_result_message")


  def __check_err(self, msg, method, err_word):
    with self.assertRaises(NotImplementedError) as context:
      method(msg)
    self.__check_err_msg(err_word, context.exception)

  def __check_err_msg(self, msg, exception):
    self.eq(
        "Your client does not implement [ {0} ] method".format(msg),
        exception.message)

