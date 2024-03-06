import itertools

import libgame
import random


class Board:    # Board code from https://gitlab.com/ritwikgopi/connect-4/-/blob/master/connect_4/board.py
    def __init__(self, size=7):
        self.size = size
        self.blank = '-'
        self.board = [
            [self.blank for _ in range(self.size)] for _ in range(self.size)
        ]
        self.filled_columns = set()
        self.border = '_' * (self.size * 8 - 7)

    def __str__(self):
        board = '\n\n'.join(
            '\t'.join(row) for row in self.board
        )
        row_numbers = '\t'.join([str(i + 1) for i in range(self.size)])
        return f"{board}\n{self.border}\n{row_numbers}\n"

    def is_filled(self):
        return len(self.filled_columns) == self.size

    def has_won(self, row, column):
        win_pattern = self.board[row][column] * 4
        valid_pos = lambda cell, offset: cell + offset >= 0 and cell + offset < self.size

        # This variable will represent vertical direction
        vertical = ''

        # This variable will represent horizontal direction
        horizontal = ''

        # These variables will represent diagonal directions
        diagonal_left = ''
        diagonal_right = ''

        for offset in range(-3, 4):
            if valid_pos(row, offset):
                vertical += self.board[row + offset][column]
            if valid_pos(column, offset):
                horizontal += self.board[row][column + offset]
            if valid_pos(row, offset) and valid_pos(column, offset):
                diagonal_left += self.board[row + offset][column + offset]
            if valid_pos(row, -offset) and valid_pos(column, offset):
                diagonal_right += self.board[row - offset][column + offset]
        # print(vertical, horizontal, diagonal_left, diagonal_right, sep="\n")
        for patterns in (vertical, horizontal, diagonal_left, diagonal_right):
            if win_pattern in patterns:
                return True
        return False

    def insert_coin(self, column, player):
        column -= 1
        for row in range(self.size - 1, -1, -1):
            if row == 0:
                self.filled_columns.add(column)
            if self.board[row][column] == self.blank:
                for r in range(row + 1):
                    if r > 0:
                        self.board[r - 1][column] = self.blank
                    self.board[r][column] = player

                return self.has_won(row, column)

        raise BoardFullError("Can't insert any more coins in this row")


class BoardFullError(Exception):
    pass


def validate(player_move: libgame.PlayerMove):
    return 1 <= int(player_move.data) < 8


def main():
    battle = libgame.get_battle()
    if battle.num_players != 2:
        raise ValueError("Only two user can play!")

    players = {1: 2, 2: 1}
    order = [1, 2]
    random.shuffle(order)

    battle.send_to(order[0], "your move!")

    board = Board()

    for player in itertools.cycle(order):
        player_move = battle.wait_for(player)
        if not validate(player_move):
            battle.set_points(players[player], 1)
            battle.end_due(f"Player {player} made invalid move!")
            return

        column = int(player_move.data)
        try:
            won = board.insert_coin(column, str(player))
            if won:
                battle.set_points(player, 1)
                battle.end()
                return
            battle.send_to(players[player], str(column))
        except BoardFullError:
            battle.set_points(players[player], 1)
            battle.end_due(f"Player {player} made invalid move!")
            return


if __name__ == "__main__":
    main()
