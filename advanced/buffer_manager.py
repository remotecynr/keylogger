"""
BufferManager module:
Handles thread-safe in-memory buffer for keystrokes,
tracks repeated keys for collapsing sequences,
and manages flushing to disk.
"""

import threading
from advanced.constants import KEY_LABELS

class BufferManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.buffer = ""
        self.repeat_key = None
        self.repeat_count = 0

    def write_to_file(self, data: str, log_file: str) -> None:
        """
        Append string data to the log file.
        Thread-safe with respect to buffer usage since it only writes passed data.
        """
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(data)

    def flush_buffer(self, log_file: str) -> None:
        """
        Write the in-memory buffer to disk and clear it.
        Uses a lock to prevent concurrent flushes.
        """
        with self.lock:
            if self.buffer:
                self.write_to_file(self.buffer, log_file)
                self.buffer = ""

    def flush_repeat(self) -> str:
        """
        Return formatted repeated key sequence and reset repeat state.
        Caller decides when/how to append the text to the buffer.
        """
        if self.repeat_key is None:
            return ""

        label = KEY_LABELS.get(
            self.repeat_key,
            getattr(self.repeat_key, "name", str(self.repeat_key)).upper()
        )
        if self.repeat_count == 1:
            text = f"[{label}]"
        else:
            text = f"[{label}({self.repeat_count})]"

        self.repeat_key = None
        self.repeat_count = 0
        return text

    def buffer_append(self, text: str) -> None:
        """
        Append text to the in-memory buffer.
        Does not trigger a flush.
        """
        self.buffer += text

    def handle_repeatable_key(self, key) -> None:
        """
        Track repeatable keys like ENTER, BACKSPACE so they collapse into [ENTER(4)].
        """
        if key == self.repeat_key:
            self.repeat_count += 1
        else:
            # Flush previous repeated keys if any before switching to new key
            # (Handled by caller before calling this method)
            self.repeat_key = key
            self.repeat_count = 1

# Single shared instance for consistent state across modules
buffer_manager = BufferManager()
