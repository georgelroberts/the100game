import numpy as np
import random
from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

random.seed(42)


class Deck:
    def __init__(self) -> None:
        self.cards = []
        self.build()
        self.shuffle()

    def build(self) -> None:
        self.cards.extend(list(np.arange(2, 100)))

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def draw_card(self) -> Optional[int]:
        if not self.cards:
            return None
        return self.cards.pop()

    def __repr__(self) -> str:
        return f"{self.cards}"


class Player:
    def __init__(self) -> None:
        self.hand = []

    def __repr__(self) -> str:
        return f"{self.hand}"


class GameCondition(Enum):
    WON = 0
    CONTINUING = 1
    LOST = 2


class TheGame(ABC):
    def __init__(self, no_players: int) -> None:
        self.deck = None
        self.no_players = no_players
        self.max_no_cards_in_hand = self.get_max_no_cards_in_hand()
        self.players = []
        self.setup_board()
        self.centre_pile = [1, 1, 100, 100]  # First two ascending, second descending
        self.start_player_index = -1
        self.turn_no = 0
        self.no_cards_per_turn = 2

    def get_max_no_cards_in_hand(self) -> int:
        if self.no_players == 2:
            return 7
        else:
            return 6

    def setup_board(self) -> None:
        self.deck = Deck()
        for ii in range(self.no_players):
            self.players.append(Player())
            self.fill_hand(ii)

    def play_game(self) -> GameCondition:
        self.start_player_index = self.choose_starting_player()
        while True:
            player_index = self.get_current_player_index()
            game_condition = self.play_turn(player_index)
            if game_condition == GameCondition.WON:
                return game_condition
            elif game_condition == GameCondition.LOST:
                return game_condition
            self.turn_no += 1

    def play_turn(self, player_index: int) -> GameCondition:
        for _ in range(self.no_cards_per_turn):
            game_condition = self.play_best_card_in_hand(player_index)
            if game_condition == GameCondition.LOST:
                return GameCondition.LOST
        self.fill_hand(player_index)
        game_condition = self.check_game_win()
        return game_condition

    def fill_hand(self, player_index: int) -> None:
        while len(self.players[player_index].hand) < self.max_no_cards_in_hand:
            card = self.deck.draw_card()
            if card:
                self.players[player_index].hand.append(card)
            else:
                break

    def get_current_player_index(self) -> int:
        turn_index = self.start_player_index + self.turn_no
        player_index = turn_index % self.no_players
        return player_index

    def check_game_win(self) -> GameCondition:
        for player in self.players:
            if player.hand:
                return GameCondition.CONTINUING
        if self.deck.cards:
            return GameCondition.CONTINUING
        return GameCondition.WON

    def __repr__(self) -> str:
        return f"Centre pile: {self.centre_pile}. Turn number: {self.turn_no}"

    @abstractmethod
    def best_pile_for_card(self, card_no: int) -> Optional[Tuple[int, int]]:
        raise NotImplementedError

    @abstractmethod
    def choose_starting_player(self) -> int:
        # Chose the pile with the best cards
        raise NotImplementedError

    @abstractmethod
    def play_best_card_in_hand(self, player_index: int) -> GameCondition:
        raise NotImplementedError


def test_gameplay(game_type: TheGame, no_players_list: List, no_runs: int) -> None:
    for no_players in no_players_list:
        no_wins = 0
        no_losses = 0
        for ii in range(no_runs):
            closest_cards_basic = game_type(no_players)
            game_condition = closest_cards_basic.play_game()
            if game_condition == GameCondition.LOST:
                no_losses += 1
            elif game_condition == GameCondition.WON:
                no_wins += 1
            else:
                raise ValueError("Game shouldn't be ongoing")
        print(f"Number of players: {no_players} wins:losses -> " +
              f"{no_wins}:{no_losses}")
