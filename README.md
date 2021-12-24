<!-- ABOUT THE PROJECT -->
## About The Project

This repo simulates 'The Game' in various scenarios.
For full game rules, please refer to https://nsv.de/wp-content/uploads/2018/05/the-game-english.pdf, but please find a basic overview below.

### Basic game overview

There are four central piles, starting at 100, 100, 1 and 1. 
Cards must be played on these piles in descending (the first two piles), or ascending (the final 2 piles) order only.

If the card is 10 away from the top card of the central pile in the wrong direction, it may also be played (called a 'jump' in this project). 
This is a strong benefit, because it moves that pile further from the end.

To start the game, each player is dealt a number of cards depending on how many players there are:
- 2 players -> 7 cards each
- Anything else -> 6 cards each.
On a player's turn, they must play two (or more if they wish) cards on any of the central piles. 
To end the player's turn, the then pick up cards until they reach the maximum number of cards.
A player is only allowed limited communication with other players: They may say if they want to go on a pile and if they have a close card, but they must not tell any fellow players what cards they have (i.e. any numbers).

The game is won when the players have played all their cards in the correct order and the deck is empty.


## Prerequisites

Please find the packages in requirements.txt

<!-- ROADMAP -->
## Roadmap

- [X] Allow players to play more than 2 cards if they have suitable cards.
- [X] Allow more advanced playing styles (e.g. if they are playing the 2 and 12 on the ascending pile, play the 12 first then jump back down to the 2).

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

