# Detour Into VR

*By Astra.* Astra's setup for streaming **DETOUR Mile 04** (an IRL + VR rave in Washington DC) to TikTok LIVE from
VRChat, Oct 9–10, 2026.

## The Overlay

The promo bar on the stream: it rotates follow reminders in random order, and shows who's playing in the Barn and
Bassment right now.

<img src="docs/images/detour-into-vr-promo-bar-20261029.png" alt="The Detour Into VR promo bar: Follow me on TikTok @findastra, in white and cyan on a dark strip with pink and cyan edges" width="100%">

**[▶ DETOUR on Twitch](https://www.twitch.tv/detourvr)** · schedule: [vrc.tl/detour](https://vrc.tl/detour)

**Needs:** Windows with Python 3 + `pip install streamlink` and ffmpeg for the recorder; OBS on the streaming laptop.

### What's in it

| Folder or file | What it does |
| --- | --- |
| `recorder/` | Records every minute of [twitch.tv/detourvr](https://www.twitch.tv/detourvr) at source quality (1080p60) until a stop time. It waits while the stream is offline, starts a new part whenever the stream drops and comes back, and saves each part as `.ts` plus an `.mp4` copy. Output: `%USERPROFILE%\Videos\detour-into-vr\twitch-recordings`. |
| `overlay/promo-bar.html` | A 1080×96 OBS browser-source strip that rotates follow reminders (TikTok @findastra, DETOUR on Twitch/Instagram) in random order, and shows who's playing in the Barn and Bassment right now. |
| `docs/handoff-laptop-obs-20261009.md` | Step-by-step OBS setup for the streaming laptop: a 1080×1920 vertical, three-panel layout (DETOUR / VRChat avatar / IRL), the TikTok key, the SRT link from the main PC, TikFinity chat commands, and pre-flight checks. |

## Developer Notes

1. **Start the recorder:** `recorder\start-recorder.cmd` (keep its window open; it blocks sleep while it runs).
2. **Stop it early:** `recorder\stop-recorder.cmd`.
3. **ffmpeg:** the recorder uses the ShareX copy if present.
4. **Rules:** [AGENTS.md](AGENTS.md).

## Credits

1. DETOUR is its own event: [twitch.tv/detourvr](https://www.twitch.tv/detourvr), schedule at
   [vrc.tl/detour](https://vrc.tl/detour). This repo is only Astra's streaming setup.
2. Built with Claude Opus 5.5, 2026-10-09.
3. The picture above is a screenshot of the overlay, 2026-10-29.

## License

MIT for the code, see [LICENSE](LICENSE). Pictures and art stay Astra's. DETOUR's name belongs to its event.
