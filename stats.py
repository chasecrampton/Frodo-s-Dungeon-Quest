from tkinter import ttk
import classes as cls

class StatsPanel(ttk.Frame):
    def __init__(self, parent, item_callback, delete_spell_callback):
        """AI-assisted. Builds the level, health, inventory, and weapon sections."""
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