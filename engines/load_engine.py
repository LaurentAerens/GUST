import chess.engine
import csv
import os

# Index-based methods
def get_max_index():
    """Get the maximum index of engines in the enginelist.csv file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    enginelist_path = os.path.join(base_dir, "enginelist.csv")

    with open(enginelist_path, "r") as csvfile:
        reader = list(csv.DictReader(csvfile))
        return len(reader) - 1

def load_engine_by_index(index, debug=False):
    """Load a chess engine by its index in the enginelist.csv file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    enginelist_path = os.path.join(base_dir, "enginelist.csv")
    executables_dir = os.path.join(base_dir, "executables")

    with open(enginelist_path, "r") as csvfile:
        reader = list(csv.DictReader(csvfile))
        if index < 0 or index >= len(reader):
            raise IndexError("Index out of range.")

        engine_row = reader[index]
        engine_path = os.path.join(executables_dir, os.path.basename(engine_row["path"]))
        engine_path = os.path.normpath(engine_path)

        if debug:
            print(f"Loading engine at index {index}: {engine_row}")
            print(f"Engine path: {engine_path}")

        return chess.engine.SimpleEngine.popen_uci(engine_path)

def get_engine_info_by_index(index, debug=False):
    """Get the ELO and name of an engine by its index."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    enginelist_path = os.path.join(base_dir, "enginelist.csv")

    with open(enginelist_path, "r") as csvfile:
        reader = list(csv.DictReader(csvfile))
        if index < 0 or index >= len(reader):
            raise IndexError("Index out of range.")

        engine = reader[index]

        if debug:
            print(f"Engine info retrieved by index {index}: {engine}")

        return {"name": engine["name"], "elo": int(engine["elo"])}

# Name-based methods
def load_engine(engine_name, debug=False):
    """Load a chess engine by name from the enginelist.csv file."""
    if debug:
        print(f"Loading engine: {engine_name}")
        print("Reading enginelist.csv...")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    enginelist_path = os.path.join(base_dir, "enginelist.csv")
    executables_dir = os.path.join(base_dir, "executables")

    with open(enginelist_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if debug:
                print(f"Checking row: {row}")
            if row["name"] == engine_name:
                engine_path = os.path.join(executables_dir, os.path.basename(row["path"]))
                engine_path = os.path.normpath(engine_path)  # Normalize path for cross-platform compatibility
                if debug:
                    print(f"Engine found. Relative Path: {engine_path}")
                return chess.engine.SimpleEngine.popen_uci(engine_path)
    raise ValueError(f"Engine '{engine_name}' not found in enginelist.csv")

def get_engine_elo(name, debug=False):
    """Get the ELO of an engine by its name."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    enginelist_path = os.path.join(base_dir, "enginelist.csv")

    with open(enginelist_path, "r") as csvfile:
        reader = list(csv.DictReader(csvfile))
        engine = next((row for row in reader if row["name"] == name), None)
        if engine is None:
            raise ValueError(f"Engine with name '{name}' not found.")

        if debug:
            print(f"Engine ELO retrieved: {engine['elo']} for name: {name}")

        return int(engine["elo"])

# Utility methods
def sort_engines_by_elo(debug=False):
    """Sort the enginelist.csv file by ELO in ascending order."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    enginelist_path = os.path.join(base_dir, "enginelist.csv")

    with open(enginelist_path, "r") as csvfile:
        reader = list(csv.DictReader(csvfile))
        sorted_engines = sorted(reader, key=lambda x: int(x["elo"]))

    with open(enginelist_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["name", "elo", "path"])
        writer.writeheader()
        writer.writerows(sorted_engines)

    if debug:
        print("Engines sorted by ELO:")
        for engine in sorted_engines:
            print(engine)

if __name__ == "__main__":
    engine_name = input("Enter the name of the engine to load: ")
    debug_mode = input("Enable debug mode? (yes/no): ").strip().lower() == "yes"
    try:
        engine = load_engine(engine_name, debug=debug_mode)
        print(f"Successfully loaded engine: {engine_name}")
        engine.quit()
    except Exception as e:
        print(f"Error: {e}")