"""
ZULU Desktop GUI — JARVIS-inspired interface via CustomTkinter
"""

import queue
import threading
import tkinter as tk

import customtkinter as ctk

from zulu.chat import ask_llm
from zulu.computer import open_app, search_web
from zulu.core import COMMANDS, WAKE_WORD
from zulu.news import get_news
from zulu.voice import listen, speak

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Palette ───────────────────────────────────────────────────────────────────
BG         = "#080810"
BG_CHAT    = "#0c0c18"
BG_BUBBLE  = "#111128"
BG_INPUT   = "#0f0f1e"
CYAN       = "#00c8f0"
CYAN_DIM   = "#0077aa"
CYAN_DARK  = "#003355"
WHITE      = "#dde8f5"
GRAY       = "#444466"
GRAY_LIGHT = "#7777aa"
RED        = "#ff3355"

FONT_TITLE  = ("Courier New", 24, "bold")
FONT_STATUS = ("Courier New", 10)
FONT_CHAT   = ("Courier New", 12)
FONT_NAME   = ("Courier New", 10, "bold")
FONT_BTN    = ("Courier New", 11, "bold")


class ZuluGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self._busy = False
        self._listening = False
        self._tts_queue: queue.Queue = queue.Queue()
        threading.Thread(target=self._tts_worker, daemon=True).start()

        self._build()
        self._post_zulu("ZULU online. How can I assist you?")
        self._tts_queue.put("ZULU online. How can I assist you?")

    # ── TTS ───────────────────────────────────────────────────────────────────

    def _tts_worker(self):
        while True:
            text = self._tts_queue.get()
            try:
                speak(text)
            except Exception:
                pass
            self._tts_queue.task_done()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build(self):
        self.root.title("ZULU")
        self.root.geometry("820x680")
        self.root.minsize(560, 440)
        self.root.configure(fg_color=BG)

        self._build_header()
        self._build_chat()
        self._build_input()

    def _build_header(self):
        header = ctk.CTkFrame(self.root, fg_color=BG, corner_radius=0, height=70)
        header.pack(fill=tk.X, padx=28, pady=(20, 0))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="◈  Z U L U",
            font=FONT_TITLE,
            text_color=CYAN,
        ).pack(side=tk.LEFT, pady=10)

        right = ctk.CTkFrame(header, fg_color=BG, corner_radius=0)
        right.pack(side=tk.RIGHT, pady=10)

        self._dot_lbl = ctk.CTkLabel(right, text="●", font=("Courier New", 14), text_color=CYAN)
        self._dot_lbl.pack(side=tk.LEFT)

        self._status_lbl = ctk.CTkLabel(right, text="  online", font=FONT_STATUS, text_color=CYAN)
        self._status_lbl.pack(side=tk.LEFT)

        # cyan rule
        ctk.CTkFrame(self.root, fg_color=CYAN_DIM, corner_radius=0, height=1).pack(
            fill=tk.X, padx=28, pady=(10, 0)
        )

    def _build_chat(self):
        self._chat = ctk.CTkTextbox(
            self.root,
            fg_color=BG_CHAT,
            text_color=WHITE,
            font=FONT_CHAT,
            wrap="word",
            state="disabled",
            corner_radius=0,
            border_width=0,
            scrollbar_button_color=CYAN_DARK,
            scrollbar_button_hover_color=CYAN_DIM,
            activate_scrollbars=True,
        )
        self._chat.pack(fill=tk.BOTH, expand=True, padx=28, pady=0)

        # colour tags
        self._chat._textbox.tag_configure("zulu_name", foreground=CYAN,       font=FONT_NAME)
        self._chat._textbox.tag_configure("zulu_msg",  foreground=WHITE,      font=FONT_CHAT,
                                           lmargin1=60, lmargin2=60)
        self._chat._textbox.tag_configure("user_name", foreground=GRAY_LIGHT, font=FONT_NAME)
        self._chat._textbox.tag_configure("user_msg",  foreground="#9090b8",  font=FONT_CHAT,
                                           lmargin1=60, lmargin2=60)

        # cyan rule
        ctk.CTkFrame(self.root, fg_color=CYAN_DIM, corner_radius=0, height=1).pack(
            fill=tk.X, padx=28, pady=(0, 0)
        )

    def _build_input(self):
        bar = ctk.CTkFrame(self.root, fg_color=BG, corner_radius=0, height=72)
        bar.pack(fill=tk.X, padx=28, pady=(0, 20))
        bar.pack_propagate(False)

        # mic button
        self._mic_btn = ctk.CTkButton(
            bar,
            text="🎤",
            width=48, height=42,
            fg_color=BG_INPUT,
            hover_color=CYAN_DARK,
            text_color=CYAN,
            font=("Courier New", 16),
            corner_radius=8,
            border_width=1,
            border_color=GRAY,
            command=self._on_mic,
        )
        self._mic_btn.pack(side=tk.LEFT, padx=(0, 10), pady=15)

        # text entry
        self._entry = ctk.CTkEntry(
            bar,
            fg_color=BG_INPUT,
            text_color=WHITE,
            border_color=CYAN_DIM,
            border_width=1,
            placeholder_text="speak or type a command...",
            placeholder_text_color=GRAY,
            font=FONT_CHAT,
            corner_radius=8,
            height=42,
        )
        self._entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=15)
        self._entry.bind("<Return>", self._on_send)

        # send button
        self._send_btn = ctk.CTkButton(
            bar,
            text="SEND",
            width=90, height=42,
            fg_color=CYAN_DIM,
            hover_color=CYAN,
            text_color=WHITE,
            font=FONT_BTN,
            corner_radius=8,
            command=self._on_send,
        )
        self._send_btn.pack(side=tk.LEFT, pady=15)

    # ── Chat helpers ──────────────────────────────────────────────────────────

    def _post_zulu(self, text: str):
        self._chat.configure(state="normal")
        self._chat._textbox.insert(tk.END, "ZULU  ", "zulu_name")
        self._chat._textbox.insert(tk.END, text + "\n\n", "zulu_msg")
        self._chat.configure(state="disabled")
        self._chat._textbox.see(tk.END)

    def _post_user(self, text: str):
        self._chat.configure(state="normal")
        self._chat._textbox.insert(tk.END, "YOU   ", "user_name")
        self._chat._textbox.insert(tk.END, text + "\n\n", "user_msg")
        self._chat.configure(state="disabled")
        self._chat._textbox.see(tk.END)

    def _set_status(self, label: str, color: str = CYAN):
        self._dot_lbl.configure(text_color=color)
        self._status_lbl.configure(text=f"  {label}", text_color=color)

    def _lock(self):
        self._busy = True
        self._send_btn.configure(state="disabled", fg_color=GRAY)
        self._entry.configure(state="disabled")

    def _unlock(self):
        self._busy = False
        self._send_btn.configure(state="normal", fg_color=CYAN_DIM)
        self._entry.configure(state="normal")
        self._entry.focus()
        self._set_status("online")

    # ── Events ────────────────────────────────────────────────────────────────

    def _on_send(self, _event=None):
        text = self._entry.get().strip()
        if not text or self._busy:
            return
        self._entry.delete(0, tk.END)
        self._dispatch(text)

    def _on_mic(self):
        if self._listening or self._busy:
            return
        self._listening = True
        self._mic_btn.configure(text_color=RED, border_color=RED)
        self._set_status("listening...", RED)
        threading.Thread(target=self._do_listen, daemon=True).start()

    def _do_listen(self):
        text = listen()
        self._listening = False
        self.root.after(0, lambda: self._mic_btn.configure(text_color=CYAN, border_color=GRAY))
        if text:
            self.root.after(0, lambda: self._dispatch(text))
        else:
            self.root.after(0, lambda: self._set_status("online"))

    # ── Core logic ────────────────────────────────────────────────────────────

    def _dispatch(self, raw: str):
        self._lock()
        self._set_status("thinking...", GRAY_LIGHT)
        self._post_user(raw)
        threading.Thread(target=self._handle, args=(raw.lower().strip(),), daemon=True).start()

    def _handle(self, text: str):
        if text.startswith(WAKE_WORD):
            text = text[len(WAKE_WORD):].strip()

        if not text:
            response = "Yes? How can I help?"
        elif any(kw in text for kw in COMMANDS["exit"]):
            self.root.after(0, self._shutdown)
            return
        elif any(kw in text for kw in COMMANDS["news"]):
            articles = get_news()
            response = ("Here are the top headlines: " + ". ".join(articles[:5])
                        if articles else "I couldn't fetch the news right now.")
        elif any(kw in text for kw in COMMANDS["open"]):
            app = self._extract(text, ["open", "launch", "start"])
            if app:
                response = f"Opening {app}."
                open_app(app)
            else:
                response = "What would you like me to open?"
        elif any(kw in text for kw in COMMANDS["search"]):
            query = self._extract(text, ["search", "look up", "google", "find"])
            if query:
                response = f"Searching for {query}."
                search_web(query)
            else:
                response = "What should I search for?"
        else:
            response = ask_llm(text)

        self.root.after(0, lambda: self._post_zulu(response))
        self.root.after(0, self._unlock)
        self._tts_queue.put(response)

    def _extract(self, text: str, verbs: list) -> str:
        for verb in verbs:
            if verb in text:
                return text.split(verb, 1)[-1].strip()
        return text.strip()

    def _shutdown(self):
        msg = "Shutting down. Goodbye."
        self._post_zulu(msg)
        self._tts_queue.put(msg)
        self.root.after(2000, self.root.destroy)

    # ── Run ───────────────────────────────────────────────────────────────────

    def run(self):
        self.root.mainloop()
