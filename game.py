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

def next_level(curr_file: Path, curr_level: str, is_dev_mode: bool):
    """Partially Team-written. Randomly returns the next level's path based on the previous level's difficulty"""
    difficulties = ["easy", "medium", "hard", "boss", "win"]
    curr_dir = curr_file.parent
    if is_dev_mode: # Dev testing is AI-written
        # Developer Mode: Sequential Progression
        curr_levels = sorted([f for f in curr_dir.glob("*.txt") if f.is_file()])
        try:
            curr_index = curr_levels.index(curr_file)
        except ValueError:
            curr_index = -1
            
        if curr_index + 1 < len(curr_levels):
            return curr_levels[curr_index + 1], curr_level
            
        diff_index = difficulties.index(curr_level)
        if diff_index + 1 < len(difficulties):
            next_difficulty = difficulties[diff_index + 1]
            next_dir = curr_dir.parent / next_difficulty
            next_levels = sorted([f for f in next_dir.glob("*.txt") if f.is_file()])
            if next_levels:
                return next_levels[0], next_difficulty
                
        return curr_file, curr_level
    else: # Standard game mode is team-written
        possible_levels = []
        directory = Path(__file__).resolve().parent / "levels"
        next_level = random.choice(["easy", "medium", "hard", "boss"])

        match curr_level:
            case "easy": next_level = random.choice(["easy", "medium"])
            case "medium": next_level = random.choice(["easy", "medium", "hard"])
            case "hard": next_level = random.choice(["medium", "hard", "boss"])
            case "boss": next_level = "win"
            case _: next_level = "win"

        directory = directory / next_level
        
        possible_levels = [f.name for f in directory.glob("*.txt") if f.is_file()]
        if possible_levels: # checks if has at least one file
            return directory / random.choice(possible_levels), next_level
        return curr_file, curr_level


def main():
    """AI-assisted. Opens the character map and player stats in one window."""
    level_file = Path(__file__).resolve().parent / "levels" / "easy" / "easy.txt"
    level = Level(level_file, frodo)
    curr_level = "easy"
    level_count = 1

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
    status_label = ttk.Label(dungeon, text="Ready.", foreground="#f5cf67")
    status_label.grid(row=3, column=0, sticky="w", pady=(5, 0))

    pending_spell = None
    dev_mode_var = tk.BooleanVar(value=False)

    def skip_level():
        """Team-written. Instantly skips to the next level (Dev mode only)."""
        nonlocal level, level_file, curr_level, level_count
        if not dev_mode_var.get():
            return
            
        next_file, next_difficulty = next_level(level_file, curr_level, dev_mode_var.get())
        level = Level(next_file, frodo)
        level_file, curr_level = next_file, next_difficulty
        level_count += 1
        
        # Reset any pending spells and redraw
        nonlocal pending_spell
        pending_spell = None
        status_label.configure(text="Ready.")
        refresh()

    def toggle_dev_mode():
        """Team-written. Enables or disables the dev mode based on the checkbox.
        Adds a skip button and infinite health"""
        if dev_mode_var.get():
            skip_button.configure(state="normal")
            frodo.health = 999999
        else:
            skip_button.configure(state="disabled")
            frodo.health = 100  # Reset to default starting health
            
        refresh()
    
    dev_mode_cb = ttk.Checkbutton(
        dungeon, 
        text="Dev Mode (Play All Levels)", 
        variable=dev_mode_var,
        command=toggle_dev_mode
    )
    dev_mode_cb.grid(row=4, column=0, sticky="w", pady=(5, 0))

    skip_button = ttk.Button(
        dungeon, 
        text="Skip to Next Level", 
        command=skip_level, 
        state="disabled"  # Starts disabled until Dev Mode is checked
    )
    skip_button.grid(row=5, column=0, sticky="w", pady=(5, 0))

    def delete_spell_ui(spell_name):
        """Team-written. Deletes a spell to make room for new ones."""
        if len(frodo.spell_slots) <= 1:
            status_label.configure(text="Cannot delete your only spell!")
            return
            
        if spell_name in frodo.spell_slots:
            frodo.spell_slots.remove(spell_name)
            
            # Force equip the first available spell to prevent holding a deleted weapon
            frodo.equip_weapon(cls.Weapon(frodo.spell_slots[0]))
                
            status_label.configure(text=f"Deleted {spell_name} spell.")
            refresh()

    # Define what happens when an inventory button is clicked
    def use_item_ui(item_name):
        """Team-written. Uses clicked item and refreshes UI."""
        if frodo.inventory.get_count(item_name) > 0: # if number of item exists
            result = frodo.use_item(item_name) # use the item, returns False or a string describing what the item did
            
            if result is False:
                status_label.configure(text=f"Cannot use {item_name}! (Spells full?)")
            else:
                # 'result' is a string describing the result
                status_label.configure(text=result)
                
            refresh() # Instantly update health/inventory amounts

    # Pass the function to the StatsPanel
    stats = StatsPanel(root, item_callback=use_item_ui, delete_spell_callback=delete_spell_ui)
    stats.grid(row=0, column=1, sticky="new", padx=(0, 16), pady=16)
    stats.grid(row=0, column=1, sticky="new", padx=(0, 16), pady=16)

    def queue_spell(event):
        """Team-written. Stages a spell slot (1-4)."""
        nonlocal pending_spell
        slot_number = int(event.char) - 1
        
        if slot_number < len(frodo.spell_slots):
            pending_spell = slot_number
            spell_name = frodo.spell_slots[slot_number].capitalize()
            # Update the UI immediately so the user knows to press WASD next
            status_label.configure(text=f"Primed {spell_name}! Press W/A/S/D to cast.")
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
        stats.refresh(frodo, level_file.stem, level_count)

    def move(event):
        """AI-assisted. Moves Frodo and refreshes the window after a keypress."""
        nonlocal level, level_file, curr_level, pending_spell, level_count
        level.clear_spell_effects()
        direction_key = event.keysym.lower()
        if pending_spell is not None:
            # Fire the spell instead of moving
            frodo.cast_spell(pending_spell, direction_key, level.map, level.monsters)
            
            # Allow monsters to move/attack after you cast
            for monster in level.monsters:
                monster.move(frodo, level.map, level.monsters)
                
            pending_spell = None # Reset the spell queue
        else:
            # Standard movement step
            level.update(direction_key)
            status_label.configure(text="Ready.")
        # check death
        if frodo.health <= 0:
            map_view.configure(state="normal")
            map_view.delete("1.0", "end")
            map_view.insert("1.0", "YOU DIED.\nPress Esc to exit.", "map")
            map_view.configure(state="disabled")
            return
        # check exit
        row, col = frodo.position
        if isinstance(level.map[row][col], cls.End):
            next_file, next_difficulty = next_level(level_file, curr_level, dev_mode_var.get())
            level = Level(next_file, frodo)
            level_file, curr_level = next_file, next_difficulty
            level_count += 1

        refresh()
    for key in "1234":
        root.bind(f"<KeyPress-{key}>", queue_spell)
    for key in "wasdWASD":
        root.bind(f"<KeyPress-{key}>", move)
    root.bind("<Escape>", lambda event: root.destroy())
    refresh()
    root.mainloop()


if __name__ == "__main__":
    main()
