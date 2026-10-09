# Detour Into VR

Astra's setup for streaming **DETOUR Mile 04** (an IRL + VR rave in Washington DC) to TikTok LIVE from VRChat, Oct 9–10, 2026.

- **`recorder/`**: records every minute of [twitch.tv/detourvr](https://www.twitch.tv/detourvr) at source quality (1080p60) until a stop time. It waits while the stream is offline, starts a new part whenever the stream drops and comes back, and saves each part as `.ts` plus an `.mp4` copy. Output: `%USERPROFILE%\Videos\detour-into-vr\twitch-recordings`.
  - Start: `recorder\start-recorder.cmd` (keep its window open; it blocks sleep while it runs).
  - Stop early: `recorder\stop-recorder.cmd`.
  - Needs Python 3 + `pip install streamlink`, and ffmpeg (uses the ShareX copy if present).
- **`overlay/promo-bar.html`**: a 1080×96 OBS browser-source strip that rotates follow reminders (TikTok @findastra, DETOUR on Twitch/Instagram) in random order, and shows who's playing in the Barn and Bassment right now.
- **`docs/handoff-laptop-obs-20261009.md`**: step-by-step OBS setup for the streaming laptop: a 1080×1920 vertical, three-panel layout (DETOUR / VRChat avatar / IRL), the TikTok key, the SRT link from the main PC, TikFinity chat commands, and pre-flight checks.

Schedule source: [vrc.tl/detour](https://vrc.tl/detour).