"""
Constant definitions for keys and modifiers.
Used for easy reference and consistent key naming.
"""

from pynput.keyboard import Key

# Modifier keys set for quick checks
MODIFIERS = {
    Key.shift, Key.shift_l, Key.shift_r,
    Key.ctrl, Key.ctrl_l, Key.ctrl_r,
    Key.alt, Key.alt_l, Key.alt_r,
    Key.cmd, Key.cmd_l, Key.cmd_r,
}

# Friendly names for modifiers
MODIFIER_NAMES = {
    Key.shift: "SHIFT",
    Key.shift_l: "SHIFT",
    Key.shift_r: "SHIFT",
    Key.ctrl: "CTRL",
    Key.ctrl_l: "CTRL",
    Key.ctrl_r: "CTRL",
    Key.alt: "ALT",
    Key.alt_l: "ALT",
    Key.alt_r: "ALT",
    Key.cmd: "CMD",
    Key.cmd_l: "CMD",
    Key.cmd_r: "CMD",
}

# Keys that should collapse when repeated (like ENTER, BACKSPACE)
REPEATABLE_KEYS = {
    Key.enter,
    Key.backspace,
    Key.tab,
    Key.delete,
    Key.space,
    Key.left,
    Key.up,
    Key.right,
    Key.down,
}

# Human-readable labels for special keys
KEY_LABELS = {
    Key.enter: "ENTER",
    Key.backspace: "BACKSPACE",
    Key.tab: "TAB",
    Key.delete: "DELETE",
    Key.space: "SPACE",
    Key.esc: "ESC",
    Key.up: "UP",
    Key.down: "DOWN",
    Key.left: "LEFT",
    Key.right: "RIGHT",
}
