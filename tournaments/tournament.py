import chess
import chess.engine
import os
from engines.load_engine import load_engine_by_index, get_max_index, get_engine_info_by_index
from chess.pgn import Game
from neural_network.model import NNUEModel
import torch
from datetime import datetime

def debug_print(message, debug):
    if debug:
        print(message)

def score_position(board):
    """Score a given board position using the NNUE model."""
    # Convert the board to a feature tensor
    board_features = convert_board_to_features(board)

    # Load the NNUE model (ensure the path to the model is correct)
    nnue_model = NNUEModel.load_stockfish_format("path/to/{nn_name}r/nnue_model.nnue")

    # Evaluate the board using the NNUE model
    score = nnue_model.evaluate_board(torch.tensor(board_features, dtype=torch.float32))

    return score

def convert_board_to_features(board):
    """Convert a chess.Board object to NNUE-compatible features.

    Args:
        board (chess.Board): The chess board object.

    Returns:
        list: A list of features representing the board state.
    """
    # Placeholder for feature extraction logic
    # Replace this with actual feature extraction logic compatible with NNUE
    features = [0] * 512  # Example: Zero-filled features for HalfKP

    # Example: Populate features based on board state
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            # Example: Encode piece type and color into features
            features[square] = piece.piece_type * (1 if piece.color == chess.WHITE else -1)

    return features

def run_tournament(nn_name, generation, model, debug=False, start_level=0):
    """Run a tournament where the user plays against increasingly harder engines.

    Args:
        nn_name (str): Name of the neural network.
        generation (int): Generation number.
        model (NNUEModel): The NNUE model to evaluate board positions.
        debug (bool): Enable debug mode.
        start_level (int): The starting engine index for the tournament.

    Returns:
        tuple: Final score and the index of the last engine played against.
    """
    score = 0
    index = start_level  # Start from the specified level

    # Get the maximum index of engines at startup
    max_index = get_max_index()
    debug_print(f"Maximum engine index: {max_index}", debug)    
    debug_print(f"Starting tournament for {nn_name} in generation {generation} from level {start_level}...", debug)

    while index <= max_index:
        try:
            # Get engine details
            engine_info = get_engine_info_by_index(index, debug=debug)
            engine_name = engine_info["name"]
            debug_print(f"Loading engine at index {index} ({engine_name})...", debug)

            engine = load_engine_by_index(index, debug=debug)

            for color in [chess.WHITE, chess.BLACK]:
                board = chess.Board()
                debug_print(f"Playing against engine at index {index} ({engine_name}) as {'White' if color == chess.WHITE else 'Black'}...", debug)

                while not board.is_game_over():
                    debug_print(str(board), debug)

                    if board.turn == color:
                        # Generate all legal moves
                        legal_moves = list(board.legal_moves)
                        debug_print(f"Legal moves: {legal_moves}", debug)

                        # Evaluate all future positions
                        scored_moves = []
                        for move in legal_moves:
                            board.push(move)
                            board_features = torch.tensor(convert_board_to_features(board), dtype=torch.float32)
                            evaluation_score = model.evaluate_board(board_features)
                            scored_moves.append((evaluation_score, move))
                            board.pop()

                        # Pick the move with the highest score
                        best_move = max(scored_moves, key=lambda x: x[0])[1]
                        debug_print(f"Best move: {best_move}", debug)

                        # Play the best move
                        board.push(best_move)
                    else:
                        result = engine.play(board, chess.engine.Limit(time=1.0))
                        board.push(result.move)
                        debug_print(f"Engine plays: {result.move}", debug)

                debug_print("Game over!", debug)
                debug_print(board.result(), debug)

                # Create directory structure for PGN storage
                pgn_dir = os.path.join("tournament_results", f"generation{generation}", nn_name)
                os.makedirs(pgn_dir, exist_ok=True)

                # Save the full PGN
                game = Game.from_board(board)
                game.headers["Event"] = "Tournament"
                game.headers["White"] = nn_name if color == chess.WHITE else engine_name
                game.headers["Black"] = engine_name if color == chess.WHITE else nn_name
                game.headers["Result"] = board.result()

                pgn_path = os.path.join(pgn_dir, f"{engine_name}_{'white' if color == chess.WHITE else 'black'}.pgn")
                with open(pgn_path, "w") as pgn_file:
                    pgn_file.write(str(game))

                debug_print(f"Game saved to {pgn_path}", debug)

                if board.result() == "1-0" and color == chess.WHITE:
                    debug_print("{nn_name} won as White! Now play as Black.", debug)
                    score += 10
                elif board.result() == "1-0" and color == chess.BLACK:
                    debug_print("{nn_name} won as Black! Moving to the next engine.", debug)
                    score += 10
                elif board.result() == "1/2-1/2":
                    debug_print("It's a draw! {nn_name} earn 1 point.", debug)
                    score += 1
                else:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"[{timestamp}] {nn_name} lost to engine {engine_name}. Final score: {score}. Tournament over.")
                    engine.quit()
                    debug_print(f"Final score for {nn_name}: {score}", debug)
                    return score, index

            debug_print(f"Current score: {score}", debug)
            index += 1
            engine.quit()

        except IndexError:
            debug_print("No more engines to play against. Tournament complete!", debug)
            break
        except Exception as e:
            debug_print(f"An error occurred: {e}", debug)
            break

    print(f"Final score for {nn_name}: {score}")
    return score, index

if __name__ == "__main__":
    nn_name = input("Enter {nn_name}r name: ")
    generation = input("Enter the generation number: ")
    debug_mode = input("Enable debug mode? (yes/no): ").strip().lower() == "yes"
    # Load the NNUE model outside the tournament function
    nnue_model = NNUEModel.load_stockfish_format("path/to/{nn_name}r/nnue_model.nnue")
    run_tournament(nn_name, generation, nnue_model, debug=debug_mode)