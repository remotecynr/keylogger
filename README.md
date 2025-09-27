# 🔑 Advanced Keylogger (Cross-Platform)

A modular, cross-platform keylogger written in Python using `pynput`.

---

## 📌 Features

- Cross-platform: **Windows**, **macOS**, **Linux**
- Logs readable key events: e.g. `[CTRL + V]`, `[ENTER(4)]`
- Detects **active window/app** and logs it
- Inserts **timestamps after idle periods** (default: 5s)
- Collapses **repeated keys** (ENTER, BACKSPACE, etc.)
- Handles **modifier combos** (CTRL, ALT, SHIFT, CMD)
- **Thread-safe buffer** management
- Graceful shutdown: `ESC`, `SIGINT`, `SIGTERM`

---

## ⚙️ Setup

```bash
git clone https://github.com/remotecynr/keylogger.git
cd keylogger
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

----------

## ▶️ Run

```bash
python -m advanced.keylogger
```

-   Logs will be written to: `advanced/keylog.txt`
    
-   Press `ESC` to stop, or `Ctrl+C` in terminal
    

----------

## 🗂 Project Structure

```
keylogger/
├── advanced/
│   ├── buffer_manager.py
│   ├── constants.py
│   ├── key_handler.py
│   ├── keylogger.py
│   ├── keylog.txt
│   └── window_detector.py
├── basic/
│   └── basic_keylogger.py
└── README.md
```

----------

## 🧩 Dependencies

Install with:

```bash
pip install -r requirements.txt
```

**Python dependencies**:

-   `pynput`
    

**Platform-specific**:

-   **Windows**: `pywin32`
    
-   **macOS**: `pyobjc`
    
-   **Linux**: `xdotool` (install manually)
    

```bash
# Linux only
sudo apt install xdotool
```

----------

## ⚠️ Ethical Notice

> This software is provided **for educational and personal use only**.

Do **not** use this to monitor others without clear, informed **consent**. Unauthorized surveillance is likely **illegal** and definitely **unethical**.

The developer is **not responsible** for any misuse.

----------

## 👤 Author

**remotecynr**  
GitHub: [https://github.com/remotecynr](https://github.com/remotecynr)


