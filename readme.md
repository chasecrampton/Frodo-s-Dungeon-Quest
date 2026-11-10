# Frodo's Dungeon Quest

Rooms, treasure, monsters, and choices with consequences. Frodo is the hero. Or the sidekick. Or the one who needs rescuing. Or a god-like figure watching over the player for good and evil.

# Game Requirements Checklist

## Game Structure

- 1\. Turn loop: One `while` loop runs the game turn by turn until the player wins, loses, or quits.
- 2\. Menu: Each turn offers options, including the rules, the current status, and quit. There's wide acceptability in what this can look like.
- 3\. Randomness: The `random` module drives dice, events, or outcomes.

## Data and Logic

- 4\. List: A list that changes during play, with at least one addition (`append` or `insert`) and one removal (`remove` or `pop`).
- 5\. Dictionary: A dictionary that changes during play, such as stats, positions, or rewards.
- 6\. Three decisions: `if` statements with an `elif` or `else` branch.
- 7\. Three loops: Including a `for` loop and a loop with an `else`.

## Functions and Files

- 8\. Five functions: Each with a docstring that starts with its `Team-written` or `AI-assisted` tag.
  - Three functions must take parameters and return a value.
  - Each team member must write at least one `Team-written` function.
- 9\. Exception handling: Use `try` / `except` around something that can actually fail.
- 10\. Write a log file: Record each turn's action and result, plus a calculated summary at the end.
- 11\. Read a file: Read a saved game or game data (rooms, spaces, events) from a file your team made.
  - AI may help fill in the data.
  - The code that reads the file must be `Team-written`.

## Requirement 12: One Visual Element (Pick at Least One)

A text game is fine, but every game must show the player at least one picture.

- 12\. Visual element: Implement at least one of the following options.

* Option 1: Text Grid Map
  - A map stored as a list of lists.
  - Printed row by row, showing where Frodo is.
  - Nothing to install.

- Option 2: Matplotlib Picture
  - A map or a chart of stats over the turns.
  - The game pauses until the plot window closes, then continues.
  - Tell players on the rules screen to close the plot to continue.

* Option 3: Turtle or Pygame
  - A stretch option.
  - Pygame requires `pip install pygame` on every laptop used on presentation day.
  - Don't mix `input()` with a pygame window because the window freezes while Python waits for typing.