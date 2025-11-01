import chess
import chess.engine
import os
from engines.load_engine import load_engine_by_index, get_max_index, get_engine_info_by_index
from chess.pgn import Game

def debug_print(message, debug):
    if debug:
        print(message)

def run_tournament(user_name, generation, debug=False):
    """Run a tournament where the user plays against increasingly harder engines."""
    score = 0
    index = 0

    # Get the maximum index of engines at startup
    max_index = get_max_index()
    print(f"Maximum engine index: {max_index}")
    debug_print(f"Starting tournament for {user_name} in generation {generation}...", debug)

    while index <= max_index:
        try:
            # Get engine details
            engine_info = get_engine_info_by_index(index, debug=debug)
            engine_name = engine_info["name"]
            debug_print(f"Loading engine at index {index} ({engine_name})...", debug)

            if debug:
                debug_command = input("Enter debug command for engine loading (or press Enter to continue): ")
                if debug_command.lower() == "victory":
                    debug_print("Debug: Forcing a victory during engine loading.", debug)
                    return
                elif debug_command.lower() == "draw":
                    debug_print("Debug: Forcing a draw during engine loading.", debug)
                    return
                elif debug_command.lower() == "lose":
                    debug_print("Debug: Forcing a loss during engine loading.", debug)
                    return

            engine = load_engine_by_index(index, debug=debug)

            for color in [chess.WHITE, chess.BLACK]:
                board = chess.Board()
                debug_print(f"Playing against engine at index {index} ({engine_name}) as {'White' if color == chess.WHITE else 'Black'}...", debug)

                while not board.is_game_over():
                    debug_print(str(board), debug)

                    if board.turn == color:
                        move = input("Enter your move: ")

                        try:
                            board.push_san(move)
                        except ValueError:
                            debug_print("Invalid move. Try again.", debug)
                            continue
                    else:
                        result = engine.play(board, chess.engine.Limit(time=1.0))
                        board.push(result.move)
                        debug_print(f"Engine plays: {result.move}", debug)

                debug_print("Game over!", debug)
                debug_print(board.result(), debug)

                # Create directory structure for PGN storage
                pgn_dir = os.path.join(f"generation{generation}", user_name)
                os.makedirs(pgn_dir, exist_ok=True)

                # Save the full PGN
                game = Game.from_board(board)
                game.headers["Event"] = "Tournament"
                game.headers["White"] = user_name if color == chess.WHITE else engine_name
                game.headers["Black"] = engine_name if color == chess.WHITE else user_name
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
                    debug_print(f"Final score for {user_name}: {score}", debug)
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

    debug_print(f"Final score for {user_name}: {score}", debug)

if __name__ == "__main__":
    user_name = input("Enter your name: ")
    generation = input("Enter the generation number: ")
    debug_mode = input("Enable debug mode? (yes/no): ").strip().lower() == "yes"
    run_tournament(user_name, generation, debug=debug_mode)