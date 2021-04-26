from GUI import MainScreen
from board import Board
from engine import get_move, shot_camera_down, move_counter
import threading
from time import sleep

PLAYER1 = True
PLAYER2 = False

if __name__ == "__main__":

    board = Board()

    class SharedContent:
        games_are_played = True
        main_thread = None

    game_screen = MainScreen(SharedContent)

    def play_game():
        while SharedContent.games_are_played:
            current_player = PLAYER1
            # TODO - a condition when nobody wins
            while not board.game_over() and SharedContent.games_are_played:
                move = get_move()
                while not board.legal_move(move):
                    if not SharedContent.games_are_played:
                        return
                    move = get_move()
                board.update_board(move, current_player)
                game_screen.update_board(move, current_player)
                current_player = not current_player
            game_screen.the_winner_is(current_player, board.winning_pattern)
            sleep(2)
            board.reset()
            game_screen.reset()
            move_counter[0] = 0

    SharedContent.main_thread = threading.Thread(target=play_game, daemon=True)
    SharedContent.main_thread.start()
    # TODO - a condition to let the thread finish before kill
    game_screen.mainloop()
    shot_camera_down()