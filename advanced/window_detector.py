"""
Cross-platform active window title detection.
Supports Windows, macOS, and Linux.
"""

import platform
import subprocess
import shutil

def _get_active_window_windows() -> str | None:
    """Windows implementation using win32gui. Requires pywin32 installed."""
    try:
        import win32gui  # type: ignore
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd)
    except Exception:
        return None

def _get_active_window_macos() -> str | None:
    """macOS implementation using AppKit. Requires pyobjc installed."""
    try:
        from AppKit import NSWorkspace  # type: ignore
        active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        return active_app.localizedName()
    except Exception:
        return None

def _get_active_window_linux() -> str | None:
    """Linux implementation using xdotool (command-line). Requires xdotool installed."""
    if shutil.which('xdotool') is None:
        return None
    try:
        proc = subprocess.run(
            ['xdotool', 'getwindowfocus', 'getwindowname'],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=0.2
        )
        title = proc.stdout.decode(errors='ignore').strip()
        return title if title else None
    except Exception:
        return None

def get_active_window_title() -> str | None:
    """
    Cross-platform dispatcher for active window title.
    Returns None if detection fails or is unsupported.
    """
    system = platform.system()
    if system == "Windows":
        return _get_active_window_windows()
    elif system == "Darwin":
        return _get_active_window_macos()
    else:
        # Assume Linux/Unix-like
        return _get_active_window_linux()
