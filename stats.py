from tkinter import ttk
import classes as cls

class StatsPanel(ttk.Frame):
    def __init__(self, parent):
        """AI-assisted. Builds the level, health, inventory, and weapon sections."""
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.level = self._section(0, "Level")
        self.health = self._section(1, "Health")
        self.inventory = self._section(2, "Inventory")
        self.weapon = self._section(3, "Equipped weapon")
        self.spells = self._section(4, "Available Spells")

    def _section(self, row, title):
        """AI-assisted. Creates a labeled section and returns its value label."""
        section = ttk.LabelFrame(self, text=title, padding=10)
        section.grid(row=row, column=0, sticky="ew", pady=(0, 8))
        value = ttk.Label(section, justify="left")
        value.pack(anchor="w")
        return value

    def refresh(self, player, level_name, level_count):
        """AI-assisted. Displays the current level and player values, including zero counts."""
        inventory = [f"{name}: {count}" for name, count in player.inventory.items.items()]
        inventory.append(f"Staffs: {', '.join(player.inventory.staffs)}")

        self.level.configure(text=f"Floor {level_count} ({level_name})")
        self.health.configure(text=str(player.health))
        self.inventory.configure(text="\n".join(inventory))
        self.weapon.configure(text=f"Type: {player.weapon.type}\nDamage: {player.weapon.damage}")
        
        spell_info = []
        for i, spell in enumerate(player.spell_slots):
            # Fetch the stats from STAFF_TYPES for the UI
            stats = cls.Weapon.STAFF_TYPES.get(spell, {})
            area = stats.get('area_type', 'line')
            rng = stats.get('range', 1)
            
            # Format: "[1] Fire: Cone, Range 3"
            spell_info.append(f"[{i+1}] {spell.capitalize()}: {area.capitalize()}, Range {rng}")
            
        self.spells.configure(text="\n".join(spell_info))
