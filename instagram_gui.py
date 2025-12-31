#!/usr/bin/env python3
"""Instagram Post Downloader GUI powered by Instaloader."""

from __future__ import annotations

import os
import queue
import re
import threading
import types
from pathlib import Path
from typing import Callable, Optional

try:
    import tkinter as tk
    from tkinter import messagebox, ttk
except ModuleNotFoundError as exc:  # pragma: no cover - platform dependent
    tk = None  # type: ignore[assignment]
    ttk = None  # type: ignore[assignment]
    messagebox = None  # type: ignore[assignment]
    _TK_IMPORT_ERROR = exc
else:
    _TK_IMPORT_ERROR = None

try:
    import instaloader
except ModuleNotFoundError as exc:  # pragma: no cover - dependency availability varies
    instaloader = None  # type: ignore[assignment]
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None


DOWNLOAD_ROOT = Path(__file__).resolve().parent / "downloads"
DOWNLOAD_ROOT.mkdir(parents=True, exist_ok=True)

SHORTCODE_PATTERN = re.compile(
    r"(?:https?://)?(?:www\.)?instagram\.com/(?:p|reel|tv)/([A-Za-z0-9_-]+)"
)


def extract_shortcode(post_link: str) -> str:
    """Return the shortcode for a given Instagram post URL or raise ValueError."""
    candidate = post_link.strip()
    match = SHORTCODE_PATTERN.search(candidate)
    if match:
        return match.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{5,}", candidate):
        return candidate
    raise ValueError("Provide a valid Instagram post link or shortcode.")


def _format_log_message(args: tuple, kwargs: dict) -> str:
    sep = kwargs.get("sep", " ")
    message = sep.join(str(arg) for arg in args)
    return message.strip()


def _wire_instaloader_logging(
    loader: "instaloader.Instaloader", emitter: Callable[[str], None]
) -> None:
    """Route Instaloader context logs into the GUI emitter."""
    ctx = loader.context

    def log_override(self, *args, **kwargs):
        message = _format_log_message(args, kwargs)
        if message:
            emitter(message)

    def error_override(self, *args, **kwargs):
        message = _format_log_message(args, kwargs)
        if message:
            emitter(f"Error: {message}")

    ctx.log = types.MethodType(log_override, ctx)
    ctx.error = types.MethodType(error_override, ctx)


def download_post(
    post_link: str,
    username: Optional[str],
    password: Optional[str],
    emitter: Callable[[str], None],
) -> Path:
    """Download a single Instagram post based on its link."""
    if instaloader is None:
        raise RuntimeError(
            "instaloader is not installed. Install it via `pip install instaloader`."
        ) from _IMPORT_ERROR

    shortcode = extract_shortcode(post_link)
    emitter(f"Detected shortcode: {shortcode}")

    loader = instaloader.Instaloader(
        dirname_pattern=str(DOWNLOAD_ROOT / "{target}"),
        download_comments=False,
        save_metadata=False,
    )
    loader.quiet = True
    _wire_instaloader_logging(loader, emitter)

    try:
        if username and password:
            emitter(f"Logging in as {username}...")
            loader.login(username, password)
        else:
            emitter("Downloading without login. Only public posts are accessible.")

        emitter("Fetching post metadata...")
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        target_name = f"{post.owner_username}_{shortcode}"
        emitter(f"Saving post to {DOWNLOAD_ROOT / target_name}")
        loader.download_post(post, target=target_name)
        emitter("Download complete.")
        return DOWNLOAD_ROOT / target_name
    finally:
        loader.close()


class InstaDownloaderGUI:
    """Tkinter GUI wrapper for the downloader."""

    def __init__(self) -> None:
        if _TK_IMPORT_ERROR is not None:  # pragma: no cover - environment specific
            raise RuntimeError(
                "tkinter is required to run the GUI. Install the Tk libraries for your "
                "platform and try again."
            ) from _TK_IMPORT_ERROR

        self.root = tk.Tk()
        self.root.title("Instagram Post Downloader")
        self.root.resizable(False, False)

        self.url_var = tk.StringVar()
        self.username_var = tk.StringVar(
            value=os.getenv("INSTAGRAM_USERNAME") or os.getenv("INSTA_USERNAME", "")
        )
        self.password_var = tk.StringVar(
            value=os.getenv("INSTAGRAM_PASSWORD") or os.getenv("INSTA_PASSWORD", "")
        )
        self.status_var = tk.StringVar(value="Idle")

        self.log_queue: "queue.Queue[dict]" = queue.Queue()

        self._build_layout()
        self.root.after(100, self._poll_queue)

        if _IMPORT_ERROR is not None:
            messagebox.showwarning(
                "Missing dependency",
                "The `instaloader` package is not installed. Install it with "
                "`pip install instaloader` before downloading posts.",
            )

    def _build_layout(self) -> None:
        padding = {"padx": 10, "pady": 5}

        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(main_frame, text="Instagram Post Link:").grid(
            row=0, column=0, sticky="w", **padding
        )
        ttk.Entry(main_frame, textvariable=self.url_var, width=60).grid(
            row=1, column=0, columnspan=2, sticky="ew", **padding
        )

        ttk.Label(main_frame, text="Username (optional):").grid(
            row=2, column=0, sticky="w", **padding
        )
        ttk.Entry(main_frame, textvariable=self.username_var, width=30).grid(
            row=3, column=0, sticky="ew", **padding
        )

        ttk.Label(main_frame, text="Password (optional):").grid(
            row=2, column=1, sticky="w", **padding
        )
        ttk.Entry(
            main_frame, textvariable=self.password_var, width=30, show="*"
        ).grid(row=3, column=1, sticky="ew", **padding)

        ttk.Label(main_frame, text=f"Download folder: {DOWNLOAD_ROOT}").grid(
            row=4, column=0, columnspan=2, sticky="w", **padding
        )

        self.download_button = ttk.Button(
            main_frame, text="Download Post", command=self._start_download
        )
        self.download_button.grid(row=5, column=0, sticky="ew", **padding)

        ttk.Button(main_frame, text="Clear Log", command=self._clear_log).grid(
            row=5, column=1, sticky="ew", **padding
        )

        ttk.Label(main_frame, textvariable=self.status_var).grid(
            row=6, column=0, sticky="w", **padding
        )
        self.progress = ttk.Progressbar(main_frame, mode="indeterminate")
        self.progress.grid(row=6, column=1, sticky="ew", **padding)

        log_frame = ttk.LabelFrame(main_frame, text="Download Progress")
        log_frame.grid(row=7, column=0, columnspan=2, sticky="nsew", **padding)

        self.log_text = tk.Text(log_frame, height=15, width=70, state=tk.DISABLED)
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)

    def _clear_log(self) -> None:
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def _append_log(self, message: str) -> None:
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def _start_download(self) -> None:
        if _IMPORT_ERROR is not None:
            messagebox.showerror(
                "Dependency missing",
                "instaloader is required. Install it with `pip install instaloader`.",
            )
            return

        url = self.url_var.get().strip()
        username = self.username_var.get().strip() or None
        password = self.password_var.get() or None

        if not url:
            messagebox.showerror("Missing data", "Enter an Instagram post link.")
            return

        if (username and not password) or (password and not username):
            messagebox.showerror(
                "Credentials incomplete",
                "Provide both username and password, or leave both blank.",
            )
            return

        self.download_button.config(state=tk.DISABLED)
        self.progress.start(10)
        self.status_var.set("Downloading...")
        self._clear_log()

        worker = threading.Thread(
            target=self._download_worker, args=(url, username, password), daemon=True
        )
        worker.start()

    def _download_worker(
        self, url: str, username: Optional[str], password: Optional[str]
    ) -> None:
        def emit(message: str) -> None:
            self.log_queue.put({"type": "log", "message": message})

        try:
            target_path = download_post(url, username, password, emit)
        except Exception as exc:  # pragma: no cover - GUI handles errors
            self.log_queue.put({"type": "done", "success": False, "error": str(exc)})
        else:
            self.log_queue.put({"type": "done", "success": True, "path": target_path})

    def _poll_queue(self) -> None:
        try:
            while True:
                message = self.log_queue.get_nowait()
                if message["type"] == "log":
                    self._append_log(message["message"])
                elif message["type"] == "done":
                    self._finish_download(message)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self._poll_queue)

    def _finish_download(self, payload: dict) -> None:
        self.progress.stop()
        self.download_button.config(state=tk.NORMAL)

        if payload.get("success"):
            path = payload["path"]
            self.status_var.set("Download complete.")
            messagebox.showinfo(
                "Download complete", f"Post saved to:\n{Path(path).resolve()}"
            )
        else:
            self.status_var.set("Failed")
            messagebox.showerror("Download failed", payload.get("error", "Unknown error"))

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = InstaDownloaderGUI()
    app.run()


if __name__ == "__main__":
    main()
