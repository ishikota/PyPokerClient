
class BasePokerPlayer:
  """Base Poker client implementation

  To create poker client, you need to override this class and
  implement following 7 methods.

  - declare_action
  - receive_game_start_message
  - receive_round_start_message
  - receive_street_start_message
  - receive_game_update_message
  - receive_round_result_message
  - receive_game_result_message
  """

  def __init__(self):
    pass

  def declare_action(self, hole_card, valid_actions, round_state, action_histories):
    err_msg = self.__build_err_msg("declare_action")
    raise NotImplementedError(err_msg)

  def receive_game_start_message(self, game_info):
    err_msg = self.__build_err_msg("receive_game_start_message")
    raise NotImplementedError(err_msg)

  def receive_round_start_message(self, hole_card, seats):
    err_msg = self.__build_err_msg("receive_round_start_message")
    raise NotImplementedError(err_msg)

  def receive_street_start_message(self, street, round_state):
    err_msg = self.__build_err_msg("receive_street_start_message")
    raise NotImplementedError(err_msg)

  def receive_game_update_message(self, action, round_state, action_histories):
    err_msg = self.__build_err_msg("receive_game_update_message")
    raise NotImplementedError(err_msg)

  def receive_round_result_message(self, winners, round_state):
    err_msg = self.__build_err_msg("receive_round_result_message")
    raise NotImplementedError(err_msg)

  def receive_game_result_message(self, seats):
    err_msg = self.__build_err_msg("receive_game_result_message")
    raise NotImplementedError(err_msg)


  def respond_to_ask(self, message):
    """Called from PokerPhaseHandler when ask message received from server"""
    data = self.__parse_ask_message(message)
    return self.declare_action(*data)

  def receive_notification(self, message):
    """Called from PokerPhaseHandler when notification received from server"""
    msg_type = message["message_type"]

    if msg_type == "game_start_message":
      data = self.__parse_game_start_message(message)
      self.receive_game_start_message(*data)

    elif msg_type == "round_start_message":
      data = self.__parse_round_start_message(message)
      self.receive_round_start_message(*data)

    elif msg_type == "street_start_message":
      data = self.__parse_street_start_message(message)
      self.receive_street_start_message(*data)

    elif msg_type == "game_update_message":
      data = self.__parse_game_update_message(message)
      self.receive_game_update_message(*data)

    elif msg_type == "round_result_message":
      data = self.__parse_round_result_message(message)
      self.receive_round_result_message(*data)

    elif msg_type == "game_result_message":
      data = self.__parse_game_result_message(message)
      self.receive_game_result_message(*data)


  def __build_err_msg(self, msg):
    return "Your client does not implement [ {0} ] method".format(msg)

  def __parse_ask_message(self, message):
    hole_card = message["hole_card"]
    valid_actions = message["valid_actions"]
    round_state = message["round_state"]
    action_histories = message["action_histories"]
    return (hole_card, valid_actions, round_state, action_histories)

  def __parse_game_start_message(self, message):
    game_info = message["game_information"]
    return (game_info)

  def __parse_round_start_message(self, message):
    seats = message["seats"]
    hole_card = message["hole_card"]
    return (hole_card, seats)

  def __parse_street_start_message(self, message):
    street = message["street"]
    round_state = message["round_state"]
    return (street, round_state)

  def __parse_game_update_message(self, message):
    action = message["action"]
    round_state = message["round_state"]
    action_histories = message["action_histories"]
    return (action, round_state, action_histories)

  def __parse_round_result_message(self, message):
    winners = message["winners"]
    round_state = message["round_state"]
    return (winners, round_state)

  def __parse_game_result_message(self, message):
    seats = message["seats"]
    return (seats)


