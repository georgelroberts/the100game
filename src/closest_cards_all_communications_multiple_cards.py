"""About: The simulates a game with communication about '10' jumps (i.e. a player can advise other players not to
place their card on a certain pile) and if they have a card that is 'close' to any pile. A player can also play extra
cards if they are close by. """
from typing import List, Tuple, Optional

from base_game import TheGame, GameCondition
from base_game import test_gameplay


def main():
    test_gameplay(ClosestCardsBasicWithJumps, [2, 3, 4], 10000)


class ClosestCardsBasicWithJumps(TheGame):
    def __init__(self, no_players=4):
        super().__init__(no_players)
        self.add_to_best_piles = [0, 0, 0, 0]
        #  Ensure that a player only ignores another players 'jump' if they
        #  would have to do something much worse on a different pile. Do
        #  this by adding to the differences for each pile.

    def best_pile_for_card(self, card_no: int) -> Optional[Tuple[int, int]]:
        # Given a card, find the best difference and index in centre pile
        min_difference = 98  # difference must be lower than this
        best_index = -1
        for index, centre_card_no in enumerate(self.centre_pile):
            if (
                    index < 2 and
                    (
                            card_no <= centre_card_no and
                            (card_no != centre_card_no - 10)
                    )
            ):  # i.e. ascending
                continue
            elif (
                    index >= 2 and
                    (
                            card_no >= centre_card_no and
                            (card_no != centre_card_no + 10)
                    )
            ):  # i.e. descending
                continue
            if index < 2:
                difference = card_no - centre_card_no
            else:
                difference = centre_card_no - card_no
            difference += self.add_to_best_piles[index]
            if difference < min_difference:
                min_difference = difference
                best_index = index
        if best_index == -1:  # Can't play a card
            return
        else:
            return min_difference, best_index

    def choose_starting_player(self) -> int:
        # Chose the pile with the best cards
        best_difference = 200
        best_player_index = -1
        for player_index, player in enumerate(self.players):
            all_differences = []
            self.calculate_best_pile_other_players(player_index)
            for card in player.hand:
                this_difference, _ = self.best_pile_for_card(card)
                all_differences.append(this_difference)
            player_difference = sum(sorted(all_differences)[:2])
            if player_difference < best_difference:
                best_difference = player_difference
                best_player_index = player_index
        return best_player_index

    def calculate_best_pile_other_players(self, this_turn_player_index: int):
        self.add_to_best_piles = [0, 0, 0, 0]
        for player_index, player in enumerate(self.players):
            if player_index == this_turn_player_index:
                continue
            self.add_10_jumps(self.players[player_index].hand)
            self.add_close_cards(self.players[player_index].hand)

    def add_10_jumps(self, hand: List[int]):
        #  At the start is the only time where two piles can have the same
        #  value, and 10 jumps can't be played then anyway+
        for centre_index, centre_card_value in enumerate(self.centre_pile):
            if centre_index < 2:
                if centre_card_value <= 10:
                    continue
                for card in hand:
                    if card == centre_card_value - 10:
                        self.add_to_best_piles[centre_index] = 10

            if centre_index >= 2:
                if centre_card_value >= 90:
                    continue
                for card in hand:
                    if card == centre_card_value + 10:
                        self.add_to_best_piles[centre_index] = 10

    def add_close_cards(self, hand: List[int]):
        #  At the start is the only time where two piles can have the same
        #  value, and 10 jumps can't be played then anyway+
        for centre_index, centre_card_value in enumerate(self.centre_pile):
            if centre_index < 2:
                for card in hand:
                    if (
                            card == centre_card_value + 1 and
                            self.add_to_best_piles[centre_index] != 10
                    ):
                        self.add_to_best_piles[centre_index] = 1

            if centre_index >= 2:
                for card in hand:
                    if (
                            card == centre_card_value - 1 and
                            self.add_to_best_piles[centre_index] != 10
                    ):
                        self.add_to_best_piles[centre_index] = 1

    def play_best_card_in_hand(self, player_index: int) -> GameCondition:
        best_difference = 100
        best_card = -1
        best_pile_index = -1
        self.calculate_best_pile_other_players(player_index)
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

    def play_turn(self, player_index: int) -> GameCondition:
        # Override default behaviour
        for _ in range(self.no_cards_per_turn):
            game_condition = self.play_best_card_in_hand(player_index)
            if game_condition == GameCondition.LOST:
                return GameCondition.LOST
        while True:
            played = self.play_good_cards(player_index)
            if not played:
                break
        self.fill_hand(player_index)
        game_condition = self.check_game_win()
        return game_condition

    def play_good_cards(self, player_index: int) -> bool:
        card_played = False
        best_difference = 100
        best_card = -1
        best_pile_index = -1
        self.calculate_best_pile_other_players(player_index)
        for card in self.players[player_index].hand:
            result = self.best_pile_for_card(card)
            if result:
                this_difference, pile_index = result
                if this_difference < best_difference:
                    best_difference = this_difference
                    best_card = card
                    best_pile_index = pile_index
        if best_difference in {-10}:
            self.centre_pile[best_pile_index] = best_card
            self.players[player_index].hand.remove(best_card)
            card_played = True
        return card_played


if __name__ == '__main__':
    main()
