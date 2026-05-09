# =============================================================================
# utils.py — Shared Display & Input Helpers
# Centralized so every module uses the same formatting.
# No game logic here — only pure display and input functions.
# =============================================================================


# -----------------------------------------------------------------------------
# Display Helpers
# -----------------------------------------------------------------------------

def header(title: str):
    """Print a prominent section header."""
    width = 52
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def subheader(title: str):
    """Print a lighter sub-section divider."""
    width = 52
    print("\n" + "-" * width)
    print(f"  {title}")
    print("-" * width)


def separator():
    """Print a plain divider line."""
    print("-" * 52)


def blank():
    """Print a blank line."""
    print()


def info(msg: str):
    """Print an informational message."""
    print(f"  {msg}")


def warn(msg: str):
    """Print a warning or error message."""
    print(f"  [!] {msg}")


def success(msg: str):
    """Print a success/positive message."""
    print(f"  >> {msg}")


# -----------------------------------------------------------------------------
# Stat Display
# -----------------------------------------------------------------------------

def display_stats(entity: dict):
    """
    Print HP, MP, ATK, and DEF for a player or monster in a consistent format.
    Works for both player dicts and monster dicts because they share key names.
    """
    hp      = entity.get("hp", 0)
    max_hp  = entity.get("max_hp", entity.get("hp", 0))
    mp      = entity.get("mp", 0)
    max_mp  = entity.get("max_mp", entity.get("mp", 0))
    atk     = entity.get("attack", 0)
    defense = entity.get("defense", 0)

    hp_bar  = _make_bar(hp, max_hp, 20, fill="█", empty="░")
    mp_bar  = _make_bar(mp, max_mp, 20, fill="▓", empty="░")

    print(f"  HP  [{hp_bar}] {hp}/{max_hp}")
    print(f"  MP  [{mp_bar}] {mp}/{max_mp}")
    print(f"  ATK: {atk}   DEF: {defense}")


def _make_bar(current: int, maximum: int, length: int, fill: str, empty: str) -> str:
    """Build a text progress bar of a given length."""
    if maximum <= 0:
        return empty * length
    filled = int((current / maximum) * length)
    filled = max(0, min(filled, length))
    return fill * filled + empty * (length - filled)


# -----------------------------------------------------------------------------
# Input Helpers
# -----------------------------------------------------------------------------

def get_valid_input(prompt: str, valid_options: list) -> str:
    """
    Repeatedly prompt until the user enters one of the valid_options.
    Comparison is case-insensitive. Returns the original-case option from the list.

    Why: Centralizing input validation avoids copy-pasting the while-True loop
    in every menu. All menus behave consistently.
    """
    valid_lower = {opt.lower(): opt for opt in valid_options}
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_lower:
            return valid_lower[choice]
        warn(f"Invalid choice. Options: {', '.join(valid_options)}")


def confirm(prompt: str) -> bool:
    """Ask a yes/no question. Returns True for 'y', False for 'n'."""
    while True:
        answer = input(f"  {prompt} [y/n]: ").strip().lower()
        if answer == "y":
            return True
        if answer == "n":
            return False
        warn("Please enter 'y' or 'n'.")
