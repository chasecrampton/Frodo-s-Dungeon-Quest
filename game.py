from pathlib import Path
import tkinter as tk
from tkinter import ttk
import random

from level import Level
import classes as cls
from stats import StatsPanel

frodo = cls.Player()

def log_stats(filename: str, stats: dict):
    """
    Team-written.

    Writes stats to a log file at the end of each game
    """

    with open(filename, "w") as file:
        file.write(str(stats))
        file.close()

def next_level(curr_level: str):
    """Team-written. Randomly returns the next level's path based on the previous level's difficulty"""

    possible_levels = []
    directory = Path(__file__).resolve().parent / "levels"
    next_level = ""

    match curr_level:
        case "easy": next_level = "medium"
        case "medium": next_level = "hard"
        case "hard": next_level = "boss"
        case "boss": next_level = "win"

    directory = directory / next_level
    
    possible_levels = [f.name for f in directory.glob("*.txt") if f.is_file()]

    level_file = directory / random.choice(possible_levels)
    return level_file, next_level


def main():
    """AI-assisted. Opens the character map and player stats in one window."""
    level_file = Path(__file__).resolve().parent / "levels" / "easy" / "easy1.txt"
    level = Level(level_file, frodo)
    curr_level = "easy"

    root = tk.Tk()
    root.title("Frodo's Dungeon Quest")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    dungeon = ttk.Frame(root, padding=16)
    dungeon.grid(row=0, column=0, sticky="nsew")
    dungeon.columnconfigure(0, weight=1)
    dungeon.rowconfigure(0, weight=1)

    map_view = tk.Text(
        dungeon,
        font=("Courier", 20, "bold"),
        wrap="none",
        background="#182520",
        foreground="#e4f0de",
        padx=22,
        pady=18,
        borderwidth=0,
        highlightthickness=0,
        takefocus=False,
    )
    map_view.tag_configure("map", justify="center")
    health_tags = {
        cls.Colors.green: "healthy",
        cls.Colors.yellow: "wounded",
        cls.Colors.red: "critical",
    }
    map_view.tag_configure("healthy", foreground="#91dc8a")
    map_view.tag_configure("wounded", foreground="#f5cf67")
    map_view.tag_configure("critical", foreground="#ff8989")
    map_view.grid(row=0, column=0, sticky="nsew")
    ttk.Label(dungeon, text="@ Frodo   M Monster   + Wall   ! Exit").grid(
        row=1, column=0, sticky="w", pady=(10, 2)
    )
    ttk.Label(dungeon, text="WASD to move  •  Esc to quit").grid(
        row=2, column=0, sticky="w"
    )

    stats = StatsPanel(root)
    stats.grid(row=0, column=1, sticky="new", padx=(0, 16), pady=16)

    def refresh():
        """AI-assisted. Redraws the map and player details for the current turn."""
        map_text = level.map_text()
        map_view.configure(
            state="normal",
            width=max(len(row) for row in map_text.splitlines()),
            height=len(level.map),
        )
        map_view.delete("1.0", "end")
        map_view.insert("1.0", map_text, "map")
        for (row, col), entity in level.visible_entities().items():
            # Map text separates each grid cell with one space.
            start = f"{row + 1}.{col * 2}"
            map_view.tag_add(health_tags[entity.color], start, f"{start}+1c")
        map_view.configure(state="disabled")
        stats.refresh(frodo, level_file.stem)

    def move(event):
        """AI-assisted. Moves Frodo and refreshes the window after a keypress."""
        nonlocal level, level_file, curr_level

        level.update(event.keysym.lower())

        row, col = frodo.position
        if isinstance(level.map[row][col], cls.End):
            next_file, next_difficulty = next_level(curr_level)
            level = Level(next_file, frodo)
            level_file, curr_level = next_file, next_difficulty

        refresh()

    for key in "wasdWASD":
        root.bind(f"<KeyPress-{key}>", move)
    root.bind("<Escape>", lambda event: root.destroy())
    refresh()
    root.mainloop()


if __name__ == "__main__":
    main()
