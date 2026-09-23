#!/usr/bin/env python3
"""DayBuddy — a cheerful desktop companion for planning your day.

Built with Python and Tkinter. No extra packages required.
"""

from __future__ import annotations

import json
import random
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox


APP_DIR = Path.home() / ".daybuddy"
TASKS_FILE = APP_DIR / "tasks.json"

BG = "#FFF6E9"
CARD = "#FFFFFF"
INK = "#264653"
MUTED = "#6B7C80"
ACCENT = "#E76F51"
TEAL = "#2A9D8F"
GOLD = "#F4A261"
SOFT = "#FDEBD0"

QUOTES = [
    "A little kindness goes a long way.",
    "You can do hard things.",
    "Today is a great day to learn something new.",
    "Small steps still move you forward.",
    "Be the reason someone smiles today.",
    "Curiosity is a superpower.",
    "Mistakes help your brain grow.",
    "Helping others makes you stronger too.",
    "Finish one thing. Then celebrate.",
    "Fresh air and a good book fix many days.",
    "Your ideas matter.",
    "Practice turns hard into possible.",
]


def load_tasks() -> list[dict]:
    APP_DIR.mkdir(parents=True, exist_ok=True)
    if not TASKS_FILE.exists():
        return []
    try:
        data = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
    except (OSError, json.JSONDecodeError):
        pass
    return []


def save_tasks(tasks: list[dict]) -> None:
    APP_DIR.mkdir(parents=True, exist_ok=True)
    TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


class DayBuddy(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("DayBuddy")
        self.geometry("720x620")
        self.minsize(620, 540)
        self.configure(bg=BG)

        self.tasks: list[dict] = load_tasks()
        self.quote = random.choice(QUOTES)
        self.remaining = 0
        self.running = False
        self.after_id: str | None = None

        self._build()
        self._tick_clock()
        self._refresh_tasks()

    def _card(self, parent: tk.Widget) -> tk.Frame:
        frame = tk.Frame(parent, bg=CARD, highlightthickness=0)
        frame.pack(fill="x", padx=24, pady=(0, 14))
        inner = tk.Frame(frame, bg=CARD)
        inner.pack(fill="x", padx=18, pady=16)
        return inner

    def _build(self) -> None:
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=24, pady=(22, 8))

        tk.Label(
            header,
            text="DayBuddy",
            font=("Segoe UI", 26, "bold"),
            fg=INK,
            bg=BG,
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Plan your day. Grow your focus. Be kind.",
            font=("Segoe UI", 11),
            fg=MUTED,
            bg=BG,
        ).pack(anchor="w", pady=(2, 0))

        clock_card = self._card(self)
        self.clock_label = tk.Label(
            clock_card,
            text="",
            font=("Segoe UI", 22, "bold"),
            fg=INK,
            bg=CARD,
        )
        self.clock_label.pack(anchor="w")
        self.date_label = tk.Label(
            clock_card,
            text="",
            font=("Segoe UI", 11),
            fg=MUTED,
            bg=CARD,
        )
        self.date_label.pack(anchor="w", pady=(4, 8))

        quote_row = tk.Frame(clock_card, bg=SOFT)
        quote_row.pack(fill="x")
        self.quote_label = tk.Label(
            quote_row,
            text=f"\u201c{self.quote}\u201d",
            font=("Segoe UI", 11, "italic"),
            fg=INK,
            bg=SOFT,
            wraplength=620,
            justify="left",
        )
        self.quote_label.pack(side="left", padx=12, pady=10, fill="x", expand=True)
        tk.Button(
            quote_row,
            text="New quote",
            command=self._new_quote,
            bg=GOLD,
            fg=INK,
            relief="flat",
            padx=10,
            pady=6,
            cursor="hand2",
        ).pack(side="right", padx=10, pady=8)

        task_card = self._card(self)
        tk.Label(
            task_card,
            text="Today's tasks",
            font=("Segoe UI", 14, "bold"),
            fg=INK,
            bg=CARD,
        ).pack(anchor="w")

        entry_row = tk.Frame(task_card, bg=CARD)
        entry_row.pack(fill="x", pady=(10, 8))
        self.task_var = tk.StringVar()
        entry = tk.Entry(
            entry_row,
            textvariable=self.task_var,
            font=("Segoe UI", 12),
            bg="#FFFDF8",
            fg=INK,
            relief="solid",
            bd=1,
        )
        entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))
        entry.bind("<Return>", lambda _e: self._add_task())
        tk.Button(
            entry_row,
            text="Add",
            command=self._add_task,
            bg=TEAL,
            fg="white",
            relief="flat",
            padx=16,
            pady=6,
            cursor="hand2",
        ).pack(side="right")

        self.task_box = tk.Frame(task_card, bg=CARD)
        self.task_box.pack(fill="both", expand=True)

        timer_card = self._card(self)
        tk.Label(
            timer_card,
            text="Focus timer",
            font=("Segoe UI", 14, "bold"),
            fg=INK,
            bg=CARD,
        ).pack(anchor="w")

        self.timer_label = tk.Label(
            timer_card,
            text="25:00",
            font=("Segoe UI", 28, "bold"),
            fg=ACCENT,
            bg=CARD,
        )
        self.timer_label.pack(anchor="w", pady=(6, 8))

        buttons = tk.Frame(timer_card, bg=CARD)
        buttons.pack(anchor="w")
        for minutes in (10, 15, 25):
            tk.Button(
                buttons,
                text=f"{minutes} min",
                command=lambda m=minutes: self._set_timer(m),
                bg=SOFT,
                fg=INK,
                relief="flat",
                padx=12,
                pady=6,
                cursor="hand2",
            ).pack(side="left", padx=(0, 8))
        self.start_btn = tk.Button(
            buttons,
            text="Start",
            command=self._toggle_timer,
            bg=ACCENT,
            fg="white",
            relief="flat",
            padx=16,
            pady=6,
            cursor="hand2",
        )
        self.start_btn.pack(side="left", padx=(8, 0))

        tk.Label(
            self,
            text="Tasks are saved on this computer. Close the window anytime.",
            font=("Segoe UI", 9),
            fg=MUTED,
            bg=BG,
        ).pack(pady=(0, 16))

        self._set_timer(25)

    def _tick_clock(self) -> None:
        now = datetime.now()
        self.clock_label.config(text=now.strftime("%I:%M:%S %p").lstrip("0"))
        self.date_label.config(text=now.strftime("%A, %B %d, %Y"))
        self.after(1000, self._tick_clock)

    def _new_quote(self) -> None:
        choices = [q for q in QUOTES if q != self.quote] or QUOTES
        self.quote = random.choice(choices)
        self.quote_label.config(text=f"\u201c{self.quote}\u201d")

    def _add_task(self) -> None:
        text = self.task_var.get().strip()
        if not text:
            return
        self.tasks.append({"text": text, "done": False})
        self.task_var.set("")
        save_tasks(self.tasks)
        self._refresh_tasks()

    def _toggle_done(self, index: int) -> None:
        self.tasks[index]["done"] = not self.tasks[index]["done"]
        save_tasks(self.tasks)
        self._refresh_tasks()

    def _delete_task(self, index: int) -> None:
        del self.tasks[index]
        save_tasks(self.tasks)
        self._refresh_tasks()

    def _refresh_tasks(self) -> None:
        for child in self.task_box.winfo_children():
            child.destroy()
        if not self.tasks:
            tk.Label(
                self.task_box,
                text="No tasks yet. Add one above.",
                font=("Segoe UI", 10),
                fg=MUTED,
                bg=CARD,
            ).pack(anchor="w", pady=4)
            return
        for index, task in enumerate(self.tasks):
            row = tk.Frame(self.task_box, bg=CARD)
            row.pack(fill="x", pady=3)
            mark = "\u2713" if task["done"] else "\u25cb"
            color = TEAL if task["done"] else INK
            style = "overstrike" if task["done"] else "normal"
            tk.Button(
                row,
                text=mark,
                command=lambda i=index: self._toggle_done(i),
                bg=CARD,
                fg=color,
                relief="flat",
                font=("Segoe UI", 12, "bold"),
                cursor="hand2",
                width=2,
            ).pack(side="left")
            tk.Label(
                row,
                text=task["text"],
                font=("Segoe UI", 11, style),
                fg=color,
                bg=CARD,
                anchor="w",
            ).pack(side="left", fill="x", expand=True)
            tk.Button(
                row,
                text="Remove",
                command=lambda i=index: self._delete_task(i),
                bg=CARD,
                fg=MUTED,
                relief="flat",
                cursor="hand2",
            ).pack(side="right")

    def _set_timer(self, minutes: int) -> None:
        self.running = False
        self.remaining = minutes * 60
        self.start_btn.config(text="Start")
        self._draw_timer()

    def _toggle_timer(self) -> None:
        if self.running:
            self.running = False
            self.start_btn.config(text="Start")
            if self.after_id:
                self.after_cancel(self.after_id)
                self.after_id = None
            return
        if self.remaining <= 0:
            self.remaining = 25 * 60
        self.running = True
        self.start_btn.config(text="Pause")
        self._countdown()

    def _countdown(self) -> None:
        if not self.running:
            return
        if self.remaining <= 0:
            self.running = False
            self.start_btn.config(text="Start")
            self.timer_label.config(text="00:00")
            messagebox.showinfo("DayBuddy", "Focus time is done. Nice work!")
            return
        self._draw_timer()
        self.remaining -= 1
        self.after_id = self.after(1000, self._countdown)

    def _draw_timer(self) -> None:
        minutes, seconds = divmod(max(self.remaining, 0), 60)
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")


def main() -> None:
    app = DayBuddy()
    app.mainloop()


if __name__ == "__main__":
    main()
