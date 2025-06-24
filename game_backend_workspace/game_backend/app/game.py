"""Tic Tac Toe game logic and state management."""

import uuid


class InvalidMoveException(Exception):
    pass


class GameNotFoundException(Exception):
    pass


class TicTacToeGame:
    """Class managing a single Tic Tac Toe game."""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.status = "waiting"  # waiting, in_progress, finished
        self.winner = None
        self.move_count = 0

    # PUBLIC_INTERFACE
    def to_dict(self):
        """Return the serializable representation of game state."""
        return {
            "id": self.id,
            "board": self.board,
            "current_player": self.current_player,
            "status": self.status,
            "winner": self.winner,
            "move_count": self.move_count,
        }

    # PUBLIC_INTERFACE
    def start(self):
        """Start game; transition from waiting to in_progress."""
        if self.status != "waiting":
            raise Exception("Game already started or finished.")
        self.status = "in_progress"

    # PUBLIC_INTERFACE
    def make_move(self, row, col):
        """
        Attempt to make a move at the given position.
        Raises InvalidMoveException for illegal moves.
        """
        if self.status != "in_progress":
            raise InvalidMoveException("The game is not in progress.")
        if not (0 <= row < 3 and 0 <= col < 3):
            raise InvalidMoveException("Move is out of bounds.")
        if self.board[row][col] is not None:
            raise InvalidMoveException("Cell is already occupied.")

        self.board[row][col] = self.current_player
        self.move_count += 1

        if self._check_winner(row, col):
            self.status = "finished"
            self.winner = self.current_player
        elif self.move_count == 9:
            self.status = "finished"
            self.winner = "Draw"
        else:
            self.current_player = "O" if self.current_player == "X" else "X"

    def _check_winner(self, row, col):
        """Return True if the current player has won after a move at (row, col)."""
        p = self.current_player
        # Check the row and column
        if all(self.board[row][c] == p for c in range(3)):
            return True
        if all(self.board[r][col] == p for r in range(3)):
            return True
        # Diagonals
        if row == col and all(self.board[i][i] == p for i in range(3)):
            return True
        if row + col == 2 and all(self.board[i][2 - i] == p for i in range(3)):
            return True
        return False


class TicTacToeGameManager:
    """
    Singleton managing all games in memory.
    In real deployment, use persistent store!
    """

    def __init__(self):
        # Key: game_id, Value: TicTacToeGame
        self._games = {}

    # PUBLIC_INTERFACE
    def create_game(self):
        """Create and register a new game. Return it."""
        game = TicTacToeGame()
        self._games[game.id] = game
        return game

    # PUBLIC_INTERFACE
    def get_game(self, game_id):
        """Retrieve a game by ID, raises GameNotFoundException if not found."""
        if game_id not in self._games:
            raise GameNotFoundException("Game not found.")
        return self._games[game_id]

    # PUBLIC_INTERFACE
    def list_games(self):
        """List all running games."""
        return [game.to_dict() for game in self._games.values()]

    # PUBLIC_INTERFACE
    def remove_game(self, game_id):
        """Remove a finished or abandoned game."""
        if game_id in self._games:
            del self._games[game_id]


# Singleton instance for game management
game_manager = TicTacToeGameManager()
