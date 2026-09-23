# DayBuddy

A cheerful desktop window app built with **Python** and **Tkinter**.

DayBuddy helps you plan a kind, focused day:

- Live clock and date
- A rotating kindness / growth quote
- A simple to-do list (saved on your computer)
- A 10 / 15 / 25 minute focus timer

No extra packages. If Python is installed, it runs.

## Run

```bash
python main.py
```

On Windows you can also double-click `main.py` if `.py` files open with Python.

## Requirements

- Python 3.9 or newer
- Tkinter (included with most official Python installs)

## What it saves

Tasks are stored in:

- Windows: `C:\\Users\\<you>\\.daybuddy\\tasks.json`
- macOS / Linux: `~/.daybuddy/tasks.json`

Nothing is sent to the internet.

## Project files

- `main.py` — the full app window
- `requirements.txt` — no third-party packages
- `LICENSE` — MIT

## Why this app

It is a complete beginner-friendly GUI project: widgets, events, a timer loop, and local JSON storage. Good first GitHub publish.

## License

MIT
