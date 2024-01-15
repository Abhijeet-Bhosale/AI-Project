import copy

class ReversiGame:
    def __init__(self, size=8):
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.board[size // 2 - 1][size // 2 - 1] = self.board[size // 2][size // 2] = 1
        self.board[size // 2 - 1][size // 2] = self.board[size // 2][size // 2 - 1] = -1

    def display_board(self):
        for row in self.board:
            print(" ".join(map(str, row)))
        print()

    def is_valid_move(self, row, col, player):
        if not (0 <= row < self.size and 0 <= col < self.size) or self.board[row][col] != 0:
            return False

        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == -player:
                    r, c = r + dr, c + dc
                    if 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                        return True
        return False

    def make_move(self, row, col, player):
        if not self.is_valid_move(row, col, player):
            return False

        self.board[row][col] = player

        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                to_flip = []
                while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == -player:
                    to_flip.append((r, c))
                    r, c = r + dr, c + dc
                    if 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                        for flip_row, flip_col in to_flip:
                            self.board[flip_row][flip_col] = player
                        break
        return True

    def get_valid_moves(self, player):
        valid_moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))
        return valid_moves

    def is_game_over(self):
        return not self.get_valid_moves(1) and not self.get_valid_moves(-1)

    def count_pieces(self):
        count_player1 = sum(row.count(1) for row in self.board)
        count_player2 = sum(row.count(-1) for row in self.board)
        return count_player1, count_player2

    def count_stable_pieces(self, player):
        return sum(row.count(player) for row in self.board)

    def evaluate_board_heuristic(self):
        flexibility_weight = 1.0
        stability_weight = 0.5
        corners_weight = 2.0

        player1_flexibility = len(self.get_valid_moves(1))
        player2_flexibility = len(self.get_valid_moves(-1))
        flexibility_score = flexibility_weight * (player1_flexibility - player2_flexibility)

        stability_score = stability_weight * (self.count_stable_pieces(1) - self.count_stable_pieces(-1))

        corners_score = corners_weight * (
            self.board[0][0] + self.board[0][-1] + self.board[-1][0] + self.board[-1][-1]
        )

        total_score = flexibility_score + stability_score + corners_score
        return total_score


def minimax(board, depth, maximizing_player):
    if depth == 0 or board.is_game_over():
        return board.evaluate_board_heuristic()

    valid_moves = board.get_valid_moves(1 if maximizing_player else -1)

    if maximizing_player:
        max_eval = float('-inf')
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            new_board.make_move(move[0], move[1], 1)
            eval = minimax(new_board, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            new_board.make_move(move[0], move[1], -1)
            eval = minimax(new_board, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

def get_best_move(board, depth):
    valid_moves = board.get_valid_moves(1)
    best_move = None
    best_eval = float('-inf')

    for move in valid_moves:
        new_board = copy.deepcopy(board)
        new_board.make_move(move[0], move[1], 1)
        eval = minimax(new_board, depth - 1, False)

        if eval > best_eval:
            best_eval = eval
            best_move = move

    return best_move

if __name__ == "__main__":
    game = ReversiGame()
    game.display_board()

    while not game.is_game_over():
        player_move = get_best_move(game, depth=3) 
        game.make_move(player_move[0], player_move[1], 1)
        game.display_board()

        if game.is_game_over():
            break

        row, col = map(int, input("Enter your move (row col): ").split())
        while not game.make_move(row, col, -1):
            print("Invalid move. Try again.")
            row, col = map(int, input("Enter your move (row col): ").split())

        game.display_board()

    count_player1, count_player2 = game.count_pieces()
    print("Game Over!")
    print(f"Player 1 (AI) score: {count_player1}")
    print(f"Player 2 (I) score: {count_player2}")

    if count_player1 > count_player2:
        print("Player 1 (AI) wins!")
    elif count_player1 < count_player2:
        print("Player 2 (I) wins!")
    else:
        print("It's a tie!")
