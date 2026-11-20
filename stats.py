# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:       Chase Crampton
#              Winfield Fleming
#              Aaron Yuan
#              Jonathan Jiang
# Section:     218
# Assignment:  L6 - Frodo Adventure
# Date:        19 11 2026

import tkinter as tk
from tkinter import ttk

import classes as cls

class StatsPanel(ttk.Frame):
    def __init__(self, parent, item_callback, delete_spell_callback):
        """AI-assisted. Builds the sidebar sections."""
        super().__init__(parent)
        self.item_callback = item_callback
        self.delete_spell_callback = delete_spell_callback
        self.columnconfigure(0, weight=1)

        self.level = self._section(0, "Level")
        self.health = self._section(1, "Health")

        self.inventory_frame = ttk.LabelFrame(self, text="Inventory", padding=10)
        self.inventory_frame.grid(row=2, column=0, sticky="ew", pady=(0, 8))

        self.weapon = self._section(3, "Equipped weapon")

        self.spells_frame = ttk.LabelFrame(self, text="Available Spells (Max 4)", padding=10)
        self.spells_frame.grid(row=4, column=0, sticky="ew", pady=(0, 8))

        self.rowconfigure(5, weight=1)
        legend = ttk.LabelFrame(self, text="Map Legend", padding=10)
        legend.grid(row=6, column=0, sticky="ew", pady=(0, 8))
        legend.columnconfigure((0, 1, 2), weight=1)
        entries = (
            "@  Frodo", "+  Wall", "?  Loot",
            "!  Exit", "#  Spell effect", "Z  Zombie",
            "F  Fairy", "H  Hound", "B  Bat",
            "T  Trap", "C  Coward", "G  Goblin",
            "S  Spider",
        )
        for index, entry in enumerate(entries):
            row, column = divmod(index, 3)
            ttk.Label(legend, text=entry).grid(row=row, column=column, sticky="w")

        log_frame = ttk.LabelFrame(self, text="Action Log", padding=10)
        log_frame.grid(row=7, column=0, sticky="ew")
        self.action_log = tk.Text(
            log_frame, height=6, width=62, wrap="none",
            state="disabled", takefocus=False,
        )
        self.action_log.pack(fill="x")

    def _section(self, row, title):
        """AI-assisted. Creates a labeled section and returns its value label."""
        section = ttk.LabelFrame(self, text=title, padding=10)
        section.grid(row=row, column=0, sticky="ew", pady=(0, 8))
        value = ttk.Label(section, justify="left")
        value.pack(anchor="w")
        return value

    def refresh(self, player, level_name, level_count):
        """AI-assisted. Displays current values and generates item/spell buttons."""
        self.level.configure(text=f"Floor {level_count} ({level_name})")
        self.health.configure(text=str(player.health))
        self.weapon.configure(text=f"Type: {player.weapon.type}\nDamage: {player.weapon.damage}")
        self.action_log.configure(state="normal")
        self.action_log.delete("1.0", "end")
        self.action_log.insert("1.0", "\n".join(player.action_log[-6:]))
        self.action_log.configure(state="disabled")
        
        # Inventory Buttons
        for widget in self.inventory_frame.winfo_children():
            widget.destroy()

        for item_name, count in player.inventory.items.items():
            if count > 0:
                btn = ttk.Button(
                    self.inventory_frame, 
                    text=f"Use {item_name} ({count})", 
                    command=lambda n=item_name: self.item_callback(n)
                )
                btn.pack(anchor="w", pady=2)

        staffs_label = ttk.Label(self.inventory_frame, text=f"Staffs: {', '.join(player.inventory.staffs)}")
        staffs_label.pack(anchor="w", pady=(5, 0))
        
        # --- NEW: Spell UI with Delete Buttons ---
        for widget in self.spells_frame.winfo_children():
            widget.destroy()
            
        for i, spell in enumerate(player.spell_slots):
            frame = ttk.Frame(self.spells_frame)
            frame.pack(fill="x", pady=2)
            
            stats = cls.Weapon.STAFF_TYPES.get(spell, {})
            area = stats.get('area_type', 'line')
            rng = stats.get('range', 1)
            
            text = f"[{i+1}] {spell.capitalize()}: {area.capitalize()}, Range {rng}"
            ttk.Label(frame, text=text).pack(side="left")
            
            # Delete button for each spell
            ttk.Button(
                frame, 
                text="Delete", 
                width=6, 
                command=lambda s=spell: self.delete_spell_callback(s)
            ).pack(side="right")
