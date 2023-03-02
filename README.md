This project is an AI game player for a board game called Teeko.

The AI player determines it's next move using the minimax algorithm (https://en.wikipedia.org/wiki/Minimax)

How to play:
Teeko is a game between two players on a 5x5 board. Each player has four markers of either red or black. Beginning with black, they take turns placing markers (the "drop phase") until all markers are on the board, with the goal of getting four in a row horizontally, vertically, or diagonally, or in a 2x2 box as shown above. If after the drop phase neither player has won, they continue taking turns moving one marker at a time -- to an adjacent space only! (this includes diagonals, not just left, right, up, and down one space.) -- until one player wins. Note, the game has no “wrap-around” similar to other board games, so a player can not move off of the board or win using pieces on the other side of the board.

Win Conditions:
Four same colored markers in a row horizontally, vertically, or diagonally. OR
Four same colored markers that form a 2x2 box.