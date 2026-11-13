import random
from level import Level
import classes as cls
import matplotlib.pyplot as plt

frodo = cls.Player()

def log_stats(filename: str, stats: dict):
    """
    Team-written.

    Writes stats to a log file at the end of each game
    """

    with open(filename, "w") as file:
        file.write(str(stats))
        file.close()