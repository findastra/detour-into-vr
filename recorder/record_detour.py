"""Record every minute of twitch.tv/detourvr at source quality until a stop time.

Polls the channel while it is offline, records with Streamlink while it is live,
and starts a new part whenever the stream drops and comes back. Each part is
written as .ts (safe if the PC crashes mid-write) and then copied into an .mp4
without re-encoding.

Usage:
    python record_detour.py --until "2026-10-11 05:00"   (local time on this PC)
Stop early: create the file STOP in the output folder, or run stop-recorder.cmd.
"""
import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

CHANNEL = "https://www.twitch.tv/detourvr"
DEFAULT_OUT = Path.home() / "Videos" / "detour-into-vr" / "twitch-recordings"
FFMPEG_CANDIDATES = [
    r"C:\Program Files\ShareX\ffmpeg.exe",
    shutil.which("ffmpeg") or "",
]
POLL_OFFLINE_SECONDS = 20
MIN_FREE_BYTES = 10 * 1024**3


def now():
    return dt.datetime.now().astimezone()


class Recorder:
    def __init__(self, out: Path, until: dt.datetime):
        self.out = out
        self.until = until
        self.out.mkdir(parents=True, exist_ok=True)
        self.log_path = out / "recorder-log.txt"
        self.status_path = out / "recorder-status.json"
        self.stop_flag = out / "STOP"
        self.ffmpeg = next((p for p in FFMPEG_CANDIDATES if p and Path(p).exists()), None)
        self.status = {"channel": CHANNEL, "until": until.isoformat(), "parts": []}

    def log(self, msg):
        line = f"{now():%Y-%m-%d %H:%M:%S} {msg}"
        print(line, flush=True)
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    def save(self, **kw):
        self.status.update(kw, updated_at=now().isoformat())
        self.status_path.write_text(json.dumps(self.status, indent=2), encoding="utf-8")

    def should_stop(self):
        if self.stop_flag.exists():
            return "STOP file found"
        if now() >= self.until:
            return "reached stop time"
        if shutil.disk_usage(self.out).free < MIN_FREE_BYTES:
            return "less than 10 GB free on disk"
        return None

    def is_live(self):
        r = subprocess.run(
            [sys.executable, "-m", "streamlink", "--json", CHANNEL],
            capture_output=True, text=True, timeout=60,
        )
        try:
            return "streams" in json.loads(r.stdout or "{}")
        except json.JSONDecodeError:
            return False

    def record_part(self):
        dest = self.out / f"detourvr-{now():%Y%m%d-%H%M%S}.ts"
        cmd = [
            sys.executable, "-m", "streamlink",
            "--hls-live-edge", "6",          # start a little behind live so nothing is missed
            "--stream-segment-attempts", "10",
            "--stream-timeout", "120",
            "--retry-open", "5",
            "--loglevel", "warning",
            "-o", str(dest),
            CHANNEL, "best",
        ]
        self.log(f"LIVE - recording to {dest.name}")
        self.save(state="recording", active_file=str(dest))
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        while proc.poll() is None:
            reason = self.should_stop()
            if reason:
                self.log(f"Stopping current part: {reason}")
                proc.terminate()
                proc.wait(timeout=60)
                break
            time.sleep(5)
        out = proc.stdout.read() if proc.stdout else ""
        if out.strip():
            self.log("streamlink: " + out.strip()[-800:])
        if dest.exists() and dest.stat().st_size > 1_000_000:
            self.status["parts"].append(str(dest))
            self.remux(dest)
        elif dest.exists():
            dest.unlink()  # empty part from a false start

    def remux(self, ts: Path):
        if not self.ffmpeg:
            self.log("ffmpeg not found; kept .ts only")
            return
        mp4 = ts.with_suffix(".mp4")
        r = subprocess.run(
            [self.ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(ts),
             "-map", "0", "-c", "copy", "-movflags", "+faststart", str(mp4)],
            capture_output=True, text=True,
        )
        if r.returncode == 0:
            self.log(f"Saved {mp4.name} (the .ts is kept as a backup)")
        else:
            self.log(f"MP4 copy failed, .ts kept: {r.stderr[-500:]}")

    def run(self):
        self.log(f"Recorder started. Watching {CHANNEL} until {self.until:%a %b %d %I:%M %p %Z}")
        self.save(state="watching", started_at=now().isoformat())
        was_offline_logged = False
        while True:
            reason = self.should_stop()
            if reason:
                self.log(f"Recorder finished: {reason}")
                self.save(state="finished", reason=reason)
                return
            try:
                live = self.is_live()
            except Exception as exc:  # network blip, timeout
                self.log(f"Check failed: {exc}")
                live = False
            if live:
                was_offline_logged = False
                self.record_part()
                continue
            if not was_offline_logged:
                self.log("Offline - checking every 20 seconds")
                self.save(state="waiting for stream")
                was_offline_logged = True
            time.sleep(POLL_OFFLINE_SECONDS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--until", required=True, help='local time, e.g. "2026-10-11 05:00"')
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    a = ap.parse_args()
    if sys.platform == "win32":
        # Keep the PC from sleeping while this process runs (ES_CONTINUOUS | ES_SYSTEM_REQUIRED).
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
    until = dt.datetime.strptime(a.until, "%Y-%m-%d %H:%M").astimezone()
    Recorder(Path(a.out), until).run()


if __name__ == "__main__":
    main()
