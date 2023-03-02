import random
import copy
import math

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def drop_phase(self, state):
        drop_cnt = 0
        for row in range(5):
            for col in range(5):
                if state[row][col] == 'b' or state[row][col] == 'r':
                    drop_cnt += 1
        return True if drop_cnt < 8 else False

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.
        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.
                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).
        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        # detect drop phase
        drop_phase = self.drop_phase(state)
        move = []
        a = -math.inf

        if not drop_phase:
            succs = self.succ(state, self.my_piece)
            for succ in succs:
                newstate = copy.deepcopy(state)
                newstate[succ[0][0]][succ[0][1]] = self.my_piece
                newstate[succ[1][0]][succ[1][1]] = ' '
                if a < self.min_value(newstate, 0):
                    a = self.min_value(newstate, 0)
                    move = succ
            return move

        # drop phase
        succs = self.succ(state)
        for succ in succs:
            newstate = copy.deepcopy(state)
            newstate[succ[0]][succ[1]] = self.my_piece
            if a < self.min_value(newstate, 0):
                a = self.min_value(newstate, 0)
                next_move = [succ[0], succ[1]]
        next_move = tuple(next_move)
        move.insert(0, next_move)
        return move

    def max_value(self, state, depth):
        if self.game_value(state) != 0:
            return self.game_value(state)
        if depth >= 1:
            return self.heuristic_game_value(state)
        if self.drop_phase(state):
            a = -math.inf
            succs = self.succ(state)
            for succ in succs:
                newstate = copy.deepcopy(state)
                newstate[succ[0]][succ[1]] = self.my_piece
                a = max(a, self.min_value(newstate, depth + 1))
        else:
            a = -math.inf # just added
            succs = self.succ(state, self.my_piece)
            for succ in succs:
                newstate = copy.deepcopy(state)
                newstate[succ[0][0]][succ[0][1]] = self.my_piece
                newstate[succ[1][0]][succ[1][1]] = ' '
                a = max(a, self.min_value(newstate, depth + 1))
        return a

    def min_value(self, state, depth):
        if self.game_value(state) != 0:
            return self.game_value(state)
        if depth >= 1:
            return self.heuristic_game_value(state)
        if self.drop_phase(state):
            b = math.inf
            succs = self.succ(state)
            for succ in succs:
                newstate = copy.deepcopy(state)
                newstate[succ[0]][succ[1]] = self.opp
                b = min(b, self.max_value(newstate, depth + 1))
        else:
            b = math.inf
            succs = self.succ(state, self.opp)
            for succ in succs:
                newstate = copy.deepcopy(state)
                newstate[succ[0][0]][succ[0][1]] = self.opp
                newstate[succ[1][0]][succ[1][1]] = ' '
                b = min(b, self.max_value(newstate, depth + 1))
        return b

    def succ(self, state, piece=None):
        succ_list = list()
        if self.drop_phase(state):
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        succ_list.append((row,col))
        else:
            moves = [[0,1], [0,-1], [1,0], [1,1], [1,-1], [-1,0], [-1,1], [-1,-1]]
            for row in range(5):
                for col in range(5):
                    if state[row][col] != ' ' and state[row][col] == piece:
                        for move in moves:
                            newrow = row + move[0]
                            newcol = col + move[1]
                            if 0 <= newrow < 5 and 0 <= newcol < 5 and state[newrow][newcol] == ' ':
                                # new pos, old pos
                                succ_list.append([(newrow, newcol), (row, col)])
        return succ_list

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col+1] == state[row+2][col+2] == \
                        state[row+3][col+3]:
                    return 1 if state[row][col]==self.my_piece else -1
        # TODO: check / diagonal wins
        for row in range(3,5):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row-1][col+1] == state[row-2][col+2] == \
                        state[row-3][col+3]:
                    return 1 if state[row][col]==self.my_piece else -1
        # TODO: check box wins
        for row in range(4):
            for col in range(4):
                if state[row][col] != ' ' and state[row][col] == state[row + 1][col] == state[row][col + 1] == \
                        state[row + 1][col + 1]:
                    return 1 if state[row][col]==self.my_piece else -1
        return 0 # no winner yet


    def heuristic_game_value(self, state):
        max_ = -2
        min_ = 2
        # horizontal
        for row in state:
            for i in range(2):
                curr_row = list()
                for space in range(4):
                    curr_row.append(row[i+space])
                my_piece_count = 0
                opp_count = 0
                for p in curr_row:
                    if p == self.my_piece:
                        my_piece_count += 1
                    elif p == self.opp:
                        opp_count += 1
                max_ = max(max_, my_piece_count * 0.2)
                min_ = min(min_, opp_count * -0.2)
        # vertical
        for col in range(5):
            for i in range(2):
                curr_col = list()
                for space in range(4):
                    curr_col.append(state[i+space][col])
                my_piece_count = 0
                opp_count = 0
                for p in curr_col:
                    if p == self.my_piece:
                        my_piece_count += 1
                    elif p == self.opp:
                        opp_count += 1
                max_ = max(max_, my_piece_count * 0.2)
                min_ = min(min_, opp_count * -0.2)
        # \ diagonal
        for row in range(2):
            for col in range(2):
                curr_diag = list()
                for space in range(4):
                    if col+space < 5 and row+space < 5:
                        curr_diag.append(state[row+space][col+space])
                    curr_diag.append(state[row+space][col+space])
                my_piece_count = 0
                opp_count = 0
                for p in curr_diag:
                    if p == self.my_piece:
                        my_piece_count += 1
                    elif p == self.opp:
                        opp_count += 1
                max_ = max(max_, my_piece_count * 0.2)
                min_ = min(min_, opp_count * -0.2)
        # / diagonal
        for row in range(3,5):
            for col in range(2):
                curr_diag = list()
                for space in range(4):
                    if row-space >= 0 and col+space < 5:
                        curr_diag.append(state[row-space][col+space])
                    curr_diag.append(state[row-space][col+space])
                my_piece_count = 0
                opp_count = 0
                for p in curr_diag:
                    if p == self.my_piece:
                        my_piece_count += 1
                    elif p == self.opp:
                        opp_count += 1
                max_ = max(max_, my_piece_count * 0.2)
                min_ = min(min_, opp_count * -0.2)
        # box
        for row in range(4):
            for col in range(4):
                curr_box = list()
                curr_box.append(state[row][col])
                curr_box.append(state[row+1][col])
                curr_box.append(state[row][col+1])
                curr_box.append(state[row+1][col+1])
                my_piece_count = 0
                opp_count = 0
                for p in curr_box:
                    if p == self.my_piece:
                        my_piece_count += 1
                    elif p == self.opp:
                        opp_count += 1
                max_ = max(max_, my_piece_count * 0.2)
                min_ = min(min_, opp_count * -0.2)
        return max_ + min_

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
