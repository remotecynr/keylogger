"""
Key handling module:
Processes keyboard input, including modifiers and repeatable keys,
formats key sequences, and appends to buffer via BufferManager.
"""

from pynput.keyboard import Key
from advanced.constants import MODIFIERS, MODIFIER_NAMES, REPEATABLE_KEYS, KEY_LABELS
from advanced.buffer_manager import buffer_manager

# Track currently held modifier keys
held_modifiers = set()

def is_modifier_key(key) -> bool:
    """Check if the given key is a recognized modifier key."""
    return key in MODIFIERS

def track_modifier(key) -> None:
    """Add a modifier key to the held_modifiers set."""
    held_modifiers.add(key)

def release_modifier(key) -> None:
    """Remove a modifier key from the held_modifiers set."""
    held_modifiers.discard(key)

def format_combo(modifiers, key) -> str:
    """
    Format a modifier+key combo string, e.g., [CTRL + SHIFT + A] or [CMD + V].
    """
    # Sort modifiers for consistent output
    mod_names = [MODIFIER_NAMES.get(mod, str(mod).upper()) for mod in sorted(modifiers, key=lambda x: str(x))]
    
    # Determine key name
    if hasattr(key, 'char') and key.char:
        key_name = key.char.upper()
    elif hasattr(key, 'name'):
        key_name = key.name.upper()
    else:
        key_name = str(key).upper()
    
    return f"[{' + '.join(mod_names + [key_name])}]"

def handle_with_modifiers(key) -> None:
    """
    Handle key presses while modifier(s) are held.
    - If only SHIFT is held and the key is printable, log the character (Shift effect).
    - Otherwise, log a formatted combo [MOD1 + MOD2 + KEY].
    """
    only_shift = held_modifiers.issubset({Key.shift, Key.shift_l, Key.shift_r})

    if only_shift:
        if hasattr(key, 'char') and key.char and key.char.isprintable():
            flush_repeat()
            buffer_manager.buffer_append(key.char)
            return
        flush_repeat()
        buffer_manager.buffer_append(format_combo(held_modifiers, key))
    else:
        flush_repeat()
        buffer_manager.buffer_append(format_combo(held_modifiers, key))

def handle_without_modifiers(key) -> None:
    """
    Handle key presses with no modifiers.
    - Printable characters appended directly.
    - Space handled specially.
    - Repeatable keys tracked for collapsing.
    - Others logged by name.
    """
    if hasattr(key, 'char') and key.char:
        flush_repeat()
        buffer_manager.buffer_append(key.char)
        return

    if key == Key.space:
        flush_repeat()
        buffer_manager.buffer_append(' ')
    elif key in REPEATABLE_KEYS:
        buffer_manager.handle_repeatable_key(key)
    else:
        flush_repeat()
        label = KEY_LABELS.get(key, getattr(key, "name", str(key)).upper())
        buffer_manager.buffer_append(f"[{label}]")

def flush_repeat() -> None:
    """
    Flush repeated keys from BufferManager to the buffer.
    """
    text = buffer_manager.flush_repeat()
    if text:
        buffer_manager.buffer_append(text)
