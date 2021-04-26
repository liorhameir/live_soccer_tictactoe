from typing import Tuple, Optional, List, Any


class Board(object):

    __board: List[List[Any]] = [[None for _ in range(3)] for _ in range(3)]

    def __init__(self, player1=True, player2=False) -> None:
        self.player1 = player1
        self.player2 = player2
        self.winning_pattern = None

    def update_board(self, position: Optional[Tuple[int, int]], player: bool) -> None:
        if self.legal_move(position):
            self.__board[position[0]][position[1]] = player

    def legal_move(self, position: Optional[Tuple[int, int]]) -> bool:
        if position is None:
            return False
        return self.__board[position[0]][position[1]] is None

    def game_over(self) -> bool:
        empty_spot = None
        for idx in range(3):
            if empty_spot in self.__board[idx]:
                empty_spot = True
            # rows
            if self.__board[idx][0] == self.__board[idx][1] == self.__board[idx][2] and self.__board[idx][0]:
                self.winning_pattern = ((idx, 0), (idx, 1), (idx, 2))
                return True
            # cols
            if self.__board[0][idx] == self.__board[1][idx] == self.__board[2][idx] and self.__board[0][idx]:
                self.winning_pattern = ((0, idx), (1, idx), (2, idx))
                return True
        if empty_spot is None:
            return True

        # left diagonal \
        if self.__board[0][0] == self.__board[1][1] == self.__board[2][2] and self.__board[0][0] is not None:
            self.winning_pattern = ((0, 0), (1, 1), (2, 2))
            return True
        # right diagonal /
        if self.__board[0][2] == self.__board[1][1] == self.__board[2][0] and self.__board[0][2]:
            self.winning_pattern = ((0, 2), (1, 1), (0, 2))
            return True

        return False

    def reset(self):
        for row in self.__board:
            for idx in range(len(row)):
                row[idx] = None
        self.winning_pattern = None
