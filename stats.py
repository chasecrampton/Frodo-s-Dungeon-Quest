from tkinter import ttk

class StatsPanel(ttk.Frame):
    def __init__(self, parent):
        """AI-assisted. Builds the level, health, inventory, and weapon sections."""
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.level = self._section(0, "Level")
        self.health = self._section(1, "Health")
        self.inventory = self._section(2, "Inventory")
        self.weapon = self._section(3, "Equipped weapon")

    def _section(self, row, title):
        """AI-assisted. Creates a labeled section and returns its value label."""
        section = ttk.LabelFrame(self, text=title, padding=10)
        section.grid(row=row, column=0, sticky="ew", pady=(0, 8))
        value = ttk.Label(section, justify="left")
        value.pack(anchor="w")
        return value

    def refresh(self, player, level_name):
        """AI-assisted. Displays the current level and player values, including zero counts."""
        inventory = [f"{name}: {count}" for name, count in player.inventory.items.items()]
        inventory.append(f"Staffs: {', '.join(player.inventory.staffs)}")

        self.level.configure(text=level_name)
        self.health.configure(text=str(player.health))
        self.inventory.configure(text="\n".join(inventory))
        self.weapon.configure(text=f"Type: {player.weapon.type}\nDamage: {player.weapon.damage}")
