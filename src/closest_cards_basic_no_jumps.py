"""
About: The simulates a game with no communication and no '10' jumps.
"""
import numpy as np
from typing import List, Tuple, Optional

from base_game import TheGame, GameCondition
from base_game import test_gameplay


def main():
    test_gameplay(ClosestCardsBasicNoJumps, [2,3,4], 1000)


class ClosestCardsBasicNoJumps(TheGame):
    def __init__(self, no_players=4):
        super().__init__(no_players)

    def best_pile_for_card(self, card_no: int) -> Optional[Tuple[int, int]]:
        # Given a card, find the best difference and index in centre pile
        min_difference = 98 # difference must be lower than this
        best_idx = -1
        for index, centre_card_no in enumerate(self.centre_pile):
            if index < 2 and card_no <= centre_card_no: # i.e. ascending
                    continue
            elif index >= 2 and card_no >= centre_card_no: # i.e. descending
                    continue
            difference = np.abs(card_no - centre_card_no)
            if difference < min_difference:
                min_difference = difference
                best_idx = index
        if best_idx == -1:  # Can't play a card
            return
        else:
            return min_difference, best_idx

    def choose_starting_player(self) -> int:
        # Chose the pile with the best cards
        best_difference = 200
        best_player_idx = -1
        for player_idx, player in enumerate(self.players):
            all_differences = []
            for card in player.hand:
                this_difference, _ = self.best_pile_for_card(card)
                all_differences.append(this_difference)
            player_difference = sum(sorted(all_differences)[:2])
            if player_difference < best_difference:
                best_difference = player_difference
                best_player_idx = player_idx
        return best_player_idx

    def play_best_card_in_hand(self, player_index: int) -> GameCondition:
        card_played = False
        best_difference = 100
        best_card = -1
        best_pile_index = -1
        for card in self.players[player_index].hand:
            result = self.best_pile_for_card(card)
            if result:
                this_difference, pile_index = result
                if this_difference < best_difference:
                    best_difference = this_difference
                    best_card = card
                    best_pile_index = pile_index
        if best_card == -1:
            return GameCondition.LOST
        self.centre_pile[best_pile_index] = best_card
        self.players[player_index].hand.remove(best_card)
        return GameCondition.CONTINUING


if __name__ == '__main__':
    main()
