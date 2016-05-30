from players.base_poker_player import BasePokerPlayer

class PokerPlayer(BasePokerPlayer):

  def __init__(self):
    pass

  def declare_action(self, hole_card, valid_actions, round_state, action_histories):
    print "[Ask] It's your turn!! declare some action"
    print "  [hoke_card] {0}".format(hole_card)
    print "  [valid_actions] {0}".format(valid_actions)
    print "  [round_state] {0}".format(round_state)
    print "  [action_histories] {0}".format(action_histories)
    return self.__select_action()

  def receive_game_start_message(self, game_info):
    print "[Notification] Game started"
    print "  [GameInformation] {0}".format(game_info)

  def receive_round_start_message(self, hole_card, seats):
    print "[Notification] New round started"
    print "  [hole_card] {0}".format(hole_card)
    print "  [seats] {0}".format(seats)

  def receive_street_start_message(self, street, round_state):
    print "[Notification] New street started"
    print "  [street] {0}".format(street)
    print "  [round_state] {0}".format(round_state)

  def receive_game_update_message(self, action, round_state, action_histories):
    print "[Notification] Received game update"
    print "  [action] {0}".format(action)
    print "  [round_state] {0}".format(round_state)
    print "  [action_histories] {0}".format(action_histories)

  def receive_round_result_message(self, winners, round_state):
    print "[Notification] Round finished"
    print "  [winners] {0}".format(winners)
    print "  [round_state] {0}".format(round_state)

  def receive_game_result_message(self, seats):
    print "[Notification] Game finished"
    print "  [seats] {0}".format(seats)


  def __select_action(self):
    action_flg, bet_amount = self.__receive_input()
    action = self.__action_flg_to_action(action_flg)
    return action, bet_amount

  def __action_flg_to_action(self, action_flg):
    if action_flg == "f":
      return "fold"
    elif action_flg == "c":
      return "call"
    elif action_flg == "r":
      return "raise"
    else:
      return action_flg  # the case when action flg is already formatted
  def __receive_input(self):
    while True:
      try:
        action_flg = raw_input("Select the action: f(fold), c(call), r(raise) >> ")
        bet_amount = raw_input("Input the bet_amount >> ")
        self.__check_action(action_flg, bet_amount)
        return action_flg, int(bet_amount)
      except Exception as e:
        print e.message

  def __check_action(self, action_flg, bet_amount):
    if action_flg not in ["f", "c", "r", "fold", "call", "raise"]:
      raise ValueError("You input invalid action [{0}]. Try again!!".format(action_flg))
    try:
      int(bet_amount)
    except ValueError:
      raise ValueError("You input invalid bet amount [{0}]. Try again!!".format(bet_amount))


