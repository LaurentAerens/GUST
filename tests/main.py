import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import chess
import chess.engine
from engines.load_engine import (
    load_engine, 
    sort_engines_by_elo, 
    load_engine_by_index, 
    get_max_index, 
    get_engine_elo, 
    get_engine_info_by_index
)
import tournaments.tournament as tournament

def play_game_with_engine_name(engine_name, debug=True):
    """Play a game against a chess engine loaded by its name."""
    board = chess.Board()
    engine = load_engine(engine_name, debug=debug)

    print("Starting a game against the engine...")
    while not board.is_game_over():
        print(board)
        if board.turn == chess.WHITE:
            move = input("Enter your move: ")
            try:
                board.push_san(move)
            except ValueError:
                print("Invalid move. Try again.")
                continue
        else:
            result = engine.play(board, chess.engine.Limit(time=1.0))
            board.push(result.move)
            print(f"Engine plays: {result.move}")

    print("Game over!")
    print(board.result())
    engine.quit()

def play_game_with_engine_index(index, debug=True):
    """Play a game against a chess engine loaded by its index."""
    board = chess.Board()
    engine = load_engine_by_index(index, debug=debug)

    print("Starting a game against the engine...")
    while not board.is_game_over():
        print(board)
        if board.turn == chess.WHITE:
            move = input("Enter your move: ")
            try:
                board.push_san(move)
            except ValueError:
                print("Invalid move. Try again.")
                continue
        else:
            result = engine.play(board, chess.engine.Limit(time=1.0))
            board.push(result.move)
            print(f"Engine plays: {result.move}")

    print("Game over!")
    print(board.result())
    engine.quit()

def run_tournament(debug=True):
    """Run a tournament where the user plays against increasingly harder engines."""
    try:
        nn_name = input("Enter your name: ")
        generation = int(input("Enter the generation number: "))
        print("Starting a tournament...")
        tournament.run_tournament(nn_name, generation, debug=debug)
        print("Tournament completed successfully!")
    except Exception as e:
        print(f"Error running tournament: {e}")

def menu():
    print("\n--- GUST Function Testing Menu ---")
    print("1. Sort engines by ELO")
    print("2. Get maximum index")
    print("3. Play a game against engine by index")
    print("4. Get engine info by index")
    print("5. Get engine ELO by name")
    print("6. Play a game against engine by name")
    print("7. Run a tournament")
    print("8. Exit")

    choice = input("Enter your choice: ")
    return choice

def main():
    print("""
              .',                      _   
       ,`/ _.' _.-                    | |  
       /  `---'         __ _ _   _ ___| |_ 
       \;/\            / _` | | | / __| __|
          \`.`        | (_| | |_| \__ \ |_ 
           \ `.`       \__, |\__,_|___/\__|
          / /   `.`     __/ |              
         /, / `,'      |___/               
         \\\\ \\
          \\\\ \\
    ejm    -`-'""")
    print("Welcome to GUST - Genetic Universal Stockfish Trainer")

    # Sort engines by ELO at startup
    print("Sorting engines by ELO at startup...")
    sort_engines_by_elo(debug=True)

    while True:
        choice = menu()

        if choice == "1":
            print("Sorting engines by ELO...")
            sort_engines_by_elo(debug=True)
        elif choice == "2":
            max_index = get_max_index(debug=True)
            print(f"Maximum index: {max_index}")
        elif choice == "3":
            try:
                index = int(input("Enter the index of the engine to play against: "))
                play_game_with_engine_index(index, debug=True)
            except Exception as e:
                print(f"Error playing game with engine by index: {e}")
        elif choice == "4":
            try:
                index = int(input("Enter the index of the engine to get info: "))
                engine_info = get_engine_info_by_index(index, debug=True)
                print(f"Engine info at index {index}: {engine_info}")
            except Exception as e:
                print(f"Error retrieving engine info by index: {e}")
        elif choice == "5":
            try:
                name = input("Enter the name of the engine: ")
                elo = get_engine_elo(name, debug=True)
                print(f"ELO of '{name}': {elo}")
            except Exception as e:
                print(f"Error retrieving engine ELO by name: {e}")
        elif choice == "6":
            try:
                name = input("Enter the name of the engine to play against: ")
                play_game_with_engine_name(name, debug=True)
            except Exception as e:
                print(f"Error playing game with engine: {e}")
        elif choice == "7":
            try:
                run_tournament(debug=True)
            except Exception as e:
                print(f"Error running tournament: {e}")
        elif choice == "8":
            print("Exiting the menu. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()