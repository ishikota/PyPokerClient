from players.base_poker_player import BasePokerPlayer

class TemplatePokerPlayer(BasePokerPlayer):

  def __init__(self):
    pass

  def declare_action(self, hole_card, valid_actions, round_state, action_histories):
    print "[Ask] It's your turn!! declare some action"
    print "  [hoke_card] {0}".format(hole_card)
    print "  [valid_actions] {0}".format(valid_actions)
    print "  [round_state] {0}".format(round_state)
    print "  [action_histories] {0}".format(action_histories)
    return 'fold', 0  # TODO This player always fold the round. So change this behavior as you like.

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


