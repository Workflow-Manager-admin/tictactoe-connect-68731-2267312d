from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields

from app.game import (
    game_manager,
    InvalidMoveException,
    GameNotFoundException,
)


# --- SCHEMAS ---


class GameCreateResponseSchema(Schema):
    id = fields.Str(required=True, description="Game ID")
    board = fields.List(
        fields.List(fields.Str(allow_none=True)),
        required=True,
        description="Game board state",
    )
    current_player = fields.Str(required=True, description="Player to move next: 'X' or 'O'")
    status = fields.Str(required=True, description="Game status")
    winner = fields.Str(allow_none=True, description="Winner, or None")
    move_count = fields.Int(required=True, description="Number of moves made")


class GameMoveSchema(Schema):
    row = fields.Int(required=True, description="Row for move, 0-2")
    col = fields.Int(required=True, description="Column for move, 0-2")


class GameStatusSchema(GameCreateResponseSchema):
    pass


class ErrorResponseSchema(Schema):
    message = fields.Str(required=True)


class ListGamesResponseSchema(Schema):
    games = fields.List(
        fields.Nested(GameCreateResponseSchema),
        required=True,
        description="List of games",
    )


# --- API DEFINITION ---


blp = Blueprint(
    "Game",
    __name__,
    url_prefix="/api/game",
    description=(
        "Endpoints for managing Tic Tac Toe games"
    ),
    tags=["TicTacToe"],
)


@blp.route("/", methods=["POST"])
class GameCreate(MethodView):
    """
    Create a new Tic Tac Toe game.
    """

    @blp.response(201, GameCreateResponseSchema)
    @blp.alt_response(500, ErrorResponseSchema, description="Internal server error")
    def post(self):
        """
        summary: Create a new game
        description: Returns the new game's info and ID.
        """
        game = game_manager.create_game()
        return game.to_dict()


@blp.route("/<game_id>/start", methods=["POST"])
class GameStart(MethodView):
    """
    Start a game (set status to 'in_progress').
    """

    @blp.response(200, GameCreateResponseSchema)
    @blp.alt_response(404, ErrorResponseSchema, description="Game not found")
    def post(self, game_id):
        """
        summary: Start a game
        description: Mark the game as started (in_progress).
        """
        try:
            game = game_manager.get_game(game_id)
            game.start()
            return game.to_dict()
        except GameNotFoundException as e:
            abort(404, message=str(e))


@blp.route("/<game_id>/move", methods=["POST"])
class GameMove(MethodView):
    """
    Apply a move in the game.
    """

    @blp.arguments(GameMoveSchema)
    @blp.response(200, GameStatusSchema)
    @blp.alt_response(404, ErrorResponseSchema, description="Game not found")
    @blp.alt_response(400, ErrorResponseSchema, description="Invalid move or game not active")
    def post(self, move_data, game_id):
        """
        summary: Make a move
        description: Apply a move for the current player.
        """
        try:
            game = game_manager.get_game(game_id)
            row = move_data.get("row")
            col = move_data.get("col")
            game.make_move(row, col)
            return game.to_dict()
        except GameNotFoundException as e:
            abort(404, message=str(e))
        except InvalidMoveException as e:
            abort(400, message=str(e))


@blp.route("/<game_id>/status", methods=["GET"])
class GameStatus(MethodView):
    """
    Get the status and board of a game.
    """

    @blp.response(200, GameStatusSchema)
    @blp.alt_response(404, ErrorResponseSchema, description="Game not found")
    def get(self, game_id):
        """
        summary: Fetch game status
        description: Get the board, current player, winner, etc.
        """
        try:
            game = game_manager.get_game(game_id)
            return game.to_dict()
        except GameNotFoundException as e:
            abort(404, message=str(e))


@blp.route("/", methods=["GET"])
class GameList(MethodView):
    """
    List all active games (for development/demo).
    """

    @blp.response(200, ListGamesResponseSchema)
    def get(self):
        """
        summary: List all games
        description: Returns a list of all known games (dev mode).
        """
        return {"games": game_manager.list_games()}
