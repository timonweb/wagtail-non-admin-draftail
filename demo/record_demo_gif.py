#!/usr/bin/env python
"""
Record the README's demo GIF: the Draftail editor on the demo's "New note" page.

Starts a throwaway demo server (temporary database and media), drives the editor
with Playwright while recording a video, and converts the video to a GIF with
ffmpeg. Run it from the repo root with `just demo-gif`.
"""

import os
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

from pathlib import Path

from playwright.sync_api import Page, expect, sync_playwright


REPO = Path(__file__).resolve().parent.parent
OUTPUT = REPO / "docs" / "demo.gif"
IMAGE = REPO / "tests" / "seed" / "example.png"
YOUTUBE_URL = "https://www.youtube.com/watch?v=IMNFjrQ5OY4"
VIEWPORT = {"width": 840, "height": 720}
GIF_FPS = 15
USERNAME = "demo"

# Headless browsers don't draw the mouse, so the page gets a fake pointer that
# follows mousemove events. Without it, the viewer can't see what's clicked.
# Transitions are switched off because every faded frame costs a full GIF frame.
PAGE_SCRIPT = """
window.addEventListener("DOMContentLoaded", () => {
  const style = document.createElement("style");
  style.textContent = "*, *::before, *::after { transition: none !important; animation: none !important; }";
  document.head.appendChild(style);
  const cursor = document.createElement("div");
  cursor.innerHTML = '<svg width="22" height="22" viewBox="0 0 24 24"><path d="M4 2l16 9.5-7 1.5-3.5 6.5z" fill="#111" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/></svg>';
  Object.assign(cursor.style, {
    position: "fixed", left: "0", top: "0", zIndex: "2147483647",
    pointerEvents: "none", transform: "translate(-100px, -100px)",
  });
  document.body.appendChild(cursor);
  document.addEventListener("mousemove", (event) => {
    cursor.style.transform = `translate(${event.clientX - 3}px, ${event.clientY - 2}px)`;
  }, true);
});
"""


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def wait_for_server(url, server, timeout=60):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if server.poll() is not None:
            sys.exit(f"The demo server exited with code {server.returncode}.")
        try:
            urllib.request.urlopen(url, timeout=2)  # noqa: S310 - local demo server URL
            return
        except (urllib.error.URLError, ConnectionError):
            time.sleep(0.5)
    sys.exit(f"The demo server didn't answer at {url} within {timeout} s.")


class Director:
    """Moves a visible pointer and types at a human pace."""

    def __init__(self, page: Page):
        self.page = page
        self.x, self.y = VIEWPORT["width"] / 2, VIEWPORT["height"] / 2

    def pause(self, ms=600):
        self.page.wait_for_timeout(ms)

    def move_to(self, locator):
        box = locator.bounding_box()
        x, y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
        self.page.mouse.move(x, y, steps=20)
        self.x, self.y = x, y

    def click(self, locator):
        self.move_to(locator)
        self.pause(250)
        self.page.mouse.click(self.x, self.y)

    def type(self, text, delay=45):
        self.page.keyboard.type(text, delay=delay)

    def select_back(self, text, skip=0):
        """Select `text`, which ends `skip` characters before the caret."""
        for _ in range(skip):
            self.page.keyboard.press("ArrowLeft")
        for _ in range(len(text)):
            self.page.keyboard.press("Shift+ArrowLeft", delay=15)
        self.pause(400)


def wait_for_modal(page, title):
    page.wait_for_selector(".Non-Admin-Draftail__modal", state="visible")
    page.get_by_text(title).first.wait_for()


def wait_for_modal_to_close(page):
    page.wait_for_selector(".Non-Admin-Draftail__modal", state="hidden", timeout=30_000)


def perform(page, workdir):
    d = Director(page)
    modal = page.locator(".Non-Admin-Draftail__modal")
    d.pause(800)

    d.click(page.locator("[name=title]"))
    d.type("Hello, Draftail")
    d.pause()

    d.click(page.locator('[role="textbox"]'))
    line = "It works on any Django form, not just in the Wagtail admin."
    d.type(line)
    d.select_back("any Django form", skip=len(", not just in the Wagtail admin."))
    d.click(page.locator("button[name=BOLD]"))
    d.page.keyboard.press("End")
    d.pause()

    d.page.keyboard.press("Enter")
    d.type("Links work too, see the docs.")
    d.select_back("docs", skip=1)
    d.click(page.locator("button[name=LINK]"))
    wait_for_modal(page, "Add a link")
    d.click(modal.locator("[name=external-link-chooser-url]"))
    d.type("https://github.com/timonweb/wagtail-non-admin-draftail", delay=20)
    d.pause(400)
    d.click(modal.locator("form [type=submit]"))
    wait_for_modal_to_close(page)
    d.page.keyboard.press("End")
    d.pause()

    d.page.keyboard.press("Enter")
    d.type("Grab the cheat sheet.")
    d.select_back("cheat sheet", skip=1)
    d.click(page.locator("button[name=DOCUMENT]"))
    wait_for_modal(page, "Upload a document")
    document = workdir / "cheat-sheet.txt"
    document.write_text("Draftail keyboard shortcuts\n")
    file_input = modal.locator("form [type=file]")
    d.move_to(file_input)
    file_input.set_input_files(document)
    expect(modal.locator("#id_document-chooser-upload-title")).to_have_value(
        "cheat-sheet"
    )
    d.pause(700)
    d.click(modal.locator("form [type=submit]"))
    wait_for_modal_to_close(page)
    d.page.keyboard.press("End")
    d.pause()

    d.page.keyboard.press("Enter")
    d.type("/image", delay=90)
    d.pause(500)
    d.page.keyboard.press("Enter")
    wait_for_modal(page, "Upload an image")
    file_input = modal.locator("form [type=file]")
    d.move_to(file_input)
    file_input.set_input_files(IMAGE)
    expect(modal.locator("#id_image-chooser-upload-title")).to_have_value("example")
    d.pause(700)
    d.click(modal.locator("form [type=submit]"))
    page.get_by_text("Choose a format").wait_for()
    d.pause(500)
    d.click(modal.locator("label[for=id_image-chooser-insertion-format_0]"))
    d.click(modal.locator("form [type=submit]"))
    wait_for_modal_to_close(page)
    d.pause()

    d.type("/embed", delay=90)
    d.pause(500)
    d.page.keyboard.press("Enter")
    wait_for_modal(page, "Insert embed")
    d.click(modal.locator("[name=embed-chooser-url]"))
    d.type(YOUTUBE_URL, delay=20)
    d.pause(400)
    d.click(modal.locator("form [type=submit]"))
    wait_for_modal_to_close(page)
    # The embed lands below the fold. Its thumbnail loads from YouTube and grows the
    # page, so wait for it before scrolling it into view.
    thumbnail = page.locator(".Draftail-Editor img.MediaBlock__img").last
    expect(thumbnail).to_have_js_property("complete", True)
    page.evaluate(
        "window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})"
    )
    d.pause(2500)


def record(base_url, password, workdir):
    """Drive the editor and return its screencast frames as (jpeg, seconds) pairs."""
    frames = []

    def on_frame(frame):
        frames.append((frame["data"], frame["timestamp"]))

    with sync_playwright() as p:
        browser = p.chromium.launch()

        login = browser.new_context(viewport=VIEWPORT)
        page = login.new_page()
        page.goto(f"{base_url}/admin/login/")
        page.fill("[name=username]", USERNAME)
        page.fill("[name=password]", password)
        page.click("form [type=submit]")
        page.wait_for_url(f"{base_url}/admin/")
        state = login.storage_state()
        login.close()

        context = browser.new_context(viewport=VIEWPORT, storage_state=state)
        context.add_init_script(PAGE_SCRIPT)
        page = context.new_page()
        page.goto(f"{base_url}/notes/new/")
        page.locator('[role="textbox"]').wait_for()
        # Screencast frames are near-lossless JPEGs sent only when the page repaints,
        # so the GIF has no video-compression noise and no duplicate frames to drop.
        with page.screencast.start(on_frame=on_frame, quality=100, size=VIEWPORT):
            perform(page, workdir)
            stopped = time.time() * 1000
        browser.close()

    if not frames:
        sys.exit("The screencast didn't deliver any frames.")
    # Timestamps are in milliseconds; each frame lasts until the next one arrives.
    ends = [timestamp for _, timestamp in frames[1:]] + [stopped]
    return [
        (data, (end - timestamp) / 1000)
        for (data, timestamp), end in zip(frames, ends, strict=True)
    ]


def to_gif(ffmpeg, frames, workdir):
    frame_dir = workdir / "frames"
    frame_dir.mkdir()
    lines = ["ffconcat version 1.0"]
    for index, (data, seconds) in enumerate(frames):
        path = frame_dir / f"{index:05}.jpg"
        path.write_bytes(data)
        lines += [f"file '{path}'", f"duration {seconds:.3f}"]
    # The concat demuxer ignores the last entry's duration unless the file repeats.
    lines.append(f"file '{path}'")
    playlist = workdir / "frames.txt"
    playlist.write_text("\n".join(lines) + "\n")

    OUTPUT.parent.mkdir(exist_ok=True)
    # fps resamples to an even frame rate and mpdecimate drops the repeats that
    # creates (the GIF keeps their timing as longer frame delays). A palette built
    # from frame changes favours what moves, and diff_mode=rectangle re-encodes
    # only the part of each frame that changed. Undithered, text stays crisp.
    filters = (
        f"fps={GIF_FPS},mpdecimate,split[a][b];"
        "[a]palettegen=max_colors=256:stats_mode=diff[palette];"
        "[b][palette]paletteuse=dither=none:diff_mode=rectangle"
    )
    subprocess.run(  # noqa: S603 - fixed arguments, ffmpeg resolved with shutil.which
        [ffmpeg, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(playlist),
         "-vf", filters, "-fps_mode", "vfr", "-loop", "0", str(OUTPUT)],
        check=True,
    )  # fmt: skip


def main():
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        sys.exit("ffmpeg is required to convert the recording to a GIF.")

    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        password = secrets.token_urlsafe(16)
        env = {
            **os.environ,
            "DATABASE_NAME": str(workdir / "db.sqlite3"),
            "MEDIA_ROOT": str(workdir / "media"),
            "DJANGO_SUPERUSER_PASSWORD": password,
        }
        manage = [sys.executable, str(REPO / "demo" / "manage.py")]
        subprocess.run([*manage, "migrate", "-v", "0"], env=env, check=True)  # noqa: S603
        subprocess.run(  # noqa: S603
            [*manage, "createsuperuser", "--noinput", "--username", USERNAME,
             "--email", "demo@example.com"],
            env=env, check=True, stdout=subprocess.DEVNULL,
        )  # fmt: skip

        port = free_port()
        base_url = f"http://127.0.0.1:{port}"
        server = subprocess.Popen(  # noqa: S603
            [*manage, "runserver", f"127.0.0.1:{port}", "--noreload"],
            env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )  # fmt: skip
        try:
            wait_for_server(base_url, server)
            frames = record(base_url, password, workdir)
            to_gif(ffmpeg, frames, workdir)
        finally:
            server.terminate()
            server.wait()

    size_kb = OUTPUT.stat().st_size / 1024
    print(f"Wrote {OUTPUT.relative_to(REPO)} ({size_kb:.0f} KB).")


if __name__ == "__main__":
    main()
