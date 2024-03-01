from poker_game_runner.state import Observation
from poker_game_runner.utils import Range, HandType
import time
import random

class Bot:
  def get_name(self):
        return "Nissemand 2.0"

  def act(self, obs: Observation):
      current_board_hand = obs.get_board_hand_type()
      can_raise = obs.can_raise()
      my_hand = obs.get_my_hand_type()
      board = obs.get_board_hand_type()

      decent_hand = Range(
          "22+, A2s+, K2s+, Q2s+, J2s+, T2s+, 92s+, 84s+, 73s+, 64s+, 53s+, A2o+, K2o+, Q4o+, J6o+, T7o+, 97o+, 87o"
      )

      if obs.current_round == 0:
          if (decent_hand.is_hand_in_range(obs.my_hand)):
              if can_raise:
                  return obs.get_min_raise()
              else:
                return self.call_raise(obs)

      if obs.current_round == 1 or obs.current_round == 2:
          if current_board_hand >= 2:
              if can_raise and my_hand > board:
                  return obs.get_min_raise()
              else:
                return self.call_raise(obs)

          if current_board_hand >= 9 and my_hand > board:
              return obs.get_max_raise()
          else:
              return self.call_raise(obs)

      if obs.current_round == 3:
          if current_board_hand >= 3:
              if can_raise and my_hand > board:
                  return obs.get_min_raise()
              else:
                return self.call_raise(obs)


          if current_board_hand >= 8:
            return obs.get_fraction_pot_raise(.4)
          
          if current_board_hand >= 5 and my_hand > board:
              return obs.get_min_raise() * 2
          else:
              return self.call_raise(obs)
          

      if obs.current_round == 4:
          if current_board_hand >= 4:
              return obs.get_min_raise()
          if current_board_hand >= 7:
              return obs.get_fraction_pot_raise(.4)

      return self.last_call(obs)
      # Returning 0 will fold or check
      # return 1 - Returning 1 will call or check
      # return x > 1 - Returning a number greater than 1 will raise
  
  def call_raise(self, obs: Observation):
    # instead of calling 1 to make sure we done go all in :)
    can_raise = obs.can_raise()
    my_player_info = obs.get_my_player_info()
    my_stack = my_player_info.stack

    stack_sizes = []
    players = obs.get_active_players()

    for player in players:
        if player.stack == 0:  #removes 0 from stack sizes, to avoid folding
            continue

        stack_sizes.append(player.stack + player.spent)

    if can_raise:
        min_stack = min(stack_sizes)
        if obs.legal_actions[0] == 1 and my_stack >= obs.legal_actions[1]:
          return min_stack
        return self.last_call(obs)
    else:
      return self.last_call(obs)
    
  def last_call(self, obs: Observation):
      big_blind = obs.big_blind
      my_player_info = obs.get_my_player_info()
      my_stack = my_player_info.stack

      if my_stack <= big_blind * 4:
          return 1
      else:
          return 0