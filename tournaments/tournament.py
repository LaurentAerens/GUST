import chess
import chess.engine
import os
import random
from engines.load_engine import load_engine_by_index, get_max_index, get_engine_info_by_index
from chess.pgn import Game

def debug_print(message, debug):
    if debug:
        print(message)

def score_position(board):
    """Score a given board position. For now, return a random value between 0 and 1000."""
    return random.randint(0, 1000)

def run_tournament(nn_name, generation, debug=False):
    """Run a tournament where the user plays against increasingly harder engines."""
    score = 0
    index = 0

    # Get the maximum index of engines at startup
    max_index = get_max_index()
    print(f"Maximum engine index: {max_index}")
    debug_print(f"Starting tournament for {nn_name} in generation {generation}...", debug)

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
                            score = score_position(board)
                            scored_moves.append((score, move))
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
                pgn_dir = os.path.join(f"generation{generation}", nn_name)
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
                    debug_print("You won as White! Now play as Black.", debug)
                    score += 10
                elif board.result() == "1-0" and color == chess.BLACK:
                    debug_print("You won as Black! Moving to the next engine.", debug)
                    score += 10
                elif board.result() == "1/2-1/2":
                    debug_print("It's a draw! You earn 1 point.", debug)
                    score += 1
                else:
                    debug_print("You lost. Tournament over.", debug)
                    engine.quit()
                    debug_print(f"Final score for {nn_name}: {score}", debug)
                    return

            debug_print(f"Current score: {score}", debug)
            index += 1
            engine.quit()

        except IndexError:
            debug_print("No more engines to play against. Tournament complete!", debug)
            break
        except Exception as e:
            debug_print(f"An error occurred: {e}", debug)
            break

    debug_print(f"Final score for {nn_name}: {score}", debug)

if __name__ == "__main__":
    nn_name = input("Enter your name: ")
    generation = input("Enter the generation number: ")
    debug_mode = input("Enable debug mode? (yes/no): ").strip().lower() == "yes"
    run_tournament(nn_name, generation, debug=debug_mode)