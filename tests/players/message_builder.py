
def game_start_message(game_info):
  return {
      u'message_type': 'game_start_message',
      u'game_information': game_info
      }

def round_start_message(seats, hole_card):
  return {
      u'message_type': 'round_start_message',
      u'seats': seats,
      u'hole_card': hole_card
      }

def street_start_message(street, round_state):
  return {
      u'message_type': 'street_start_message',
      u'street': street,
      u'round_state': round_state
      }

def game_update_message(action, round_state, action_histories):
  return {
      u'message_type': 'game_update_message',
      u'action': action,
      u'round_state': round_state,
      u'action_histories': action_histories
      }

def round_result_message(winners, round_state):
  return {
      u'message_type': 'round_result_message',
      u'winners': winners,
      u'round_state': round_state
      }

def game_result_message(seats):
  return {
      u'message_type': 'game_result_message',
      u'seats': seats
      }

def ask_message(hole_card, valid_actions, round_state, action_histories):
  return {
      u'message_type': 'ask_message',
      u'hole_card': hole_card,
      u'valid_actions': valid_actions,
      u'round_state': round_state,
      u'action_histories': action_histories
      }

def hsh():
  return { "h":"a", "s":"h" }

def ary():
  return [0] * 5

def s():
  return "hoge"

def i():
  return 53

