import random
import levels
import matplotlib.pyplot as plt

def log_stats(filename: str, stats: dict):
    """
    Team-written.

    Writes stats to a log file at the end of each game
    """

    with open(filename, "w") as file:
        file.write(str(stats))
        file.close()