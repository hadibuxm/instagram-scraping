# Instagram Post Downloader GUI

This repository now ships with a Tkinter-based interface (`instagram_gui.py`) that wraps the existing Instaloader workflow. It lets non-technical users paste a post link, kick off the download, and observe real-time progress updates without touching the command line.

## Requirements

- Python 3.9+
- [instaloader](https://instaloader.github.io/) – `pip install instaloader`
- Tk / tkinter libraries (ship with most desktop Python builds). On some Linux distros install `python3-tk`.

Optional: set `INSTAGRAM_USERNAME`/`INSTAGRAM_PASSWORD` (or `INSTA_USERNAME`/`INSTA_PASSWORD`) environment variables if you want the GUI to prefill credentials for private or rate-limited downloads.

## Usage

```bash
pip install instaloader
python instagram_gui.py
```

Steps inside the GUI:

1. Paste a valid Instagram post/reel/tv link (or shortcode).
2. Optionally supply login credentials if the post is private.
3. Click **Download Post**.
4. Watch the log panel for live progress and completion/errors.

Posts are saved under the predefined `downloads/` directory in folders named `<owner>_<shortcode>`. Use the **Clear Log** button to reset the progress view between runs.

If `instaloader` or `tkinter` is unavailable, the application shows a clear error explaining how to install the missing dependency.
