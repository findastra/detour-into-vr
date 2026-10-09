# Handoff: set up OBS on the streaming laptop for DETOUR (Oct 9 + Oct 10, 2026)

**For:** the Claude account running on Astra's streaming laptop (MSI Stealth GS77 12UE, NVIDIA RTX GPU).
**From:** Claude on Astra's main PC (AMD RX 9070 XT, runs VRChat), Oct 9 2026, 2:50 PM Mountain.
**Repo:** https://github.com/findastra/detour-into-vr. Clone it to the laptop first: the overlay file lives in it.

Follow Astra's global rules: `git fetch` / check for a newer `docs/handoff-*.md` before you start, and add your own notes as `docs/handoff-claude-laptop-YYYYMMDD.md` rather than editing this file.

## What Astra is doing

Astra is attending the VR side of **DETOUR Mile 04**, an IRL + VR rave happening in Washington DC, and going live on **TikTok LIVE** both nights. VRChat runs on the main PC. The laptop does all broadcasting: OBS → TikTok, TikFinity, and a local recording of the vertical stream.

Already handled on the main PC (do not duplicate): the DETOUR Twitch broadcast is being recorded at source quality by `recorder/record_detour.py` until Sun Oct 11, 5:00 AM Mountain.

## Schedule (all times Mountain = Astra's local time; DC is +2h)

| Night | Room | Mountain | Eastern (DC) |
|---|---|---|---|
| Fri Oct 9 | BARN | 2:30 PM – 4:15 AM | 4:30 PM – 6:15 AM |
| Fri Oct 9 | BASSMENT | 6:15 PM – 3:15 AM | 8:15 PM – 5:15 AM |
| Sat Oct 10 | BARN | 3:00 PM – 3:30 AM | 5:00 PM – 5:30 AM |
| Sat Oct 10 | BASSMENT | 6:15 PM – 3:15 AM | 8:15 PM – 5:15 AM |

Full DJ lineup: https://vrc.tl/detour. The promo bar overlay already contains every set and shows who's on now.

## The layout: 1080×1920 vertical, three stacked panels

```
y=0     ┌──────────────────────────┐
        │  DETOUR Twitch (16:9)    │  1080×608   Browser Source
y=608   ├──────────────────────────┤
        │  promo bar               │  1080×96    overlay/promo-bar.html
y=704   ├──────────────────────────┤
        │  VRChat avatar (Astra)   │  1080×608   SRT feed from main PC
y=1312  ├──────────────────────────┤
        │  IRL camera (Astra)      │  1080×608   webcam/phone cam
y=1920  └──────────────────────────┘
```

The promo bar sits between the Detour panel and the avatar panel on purpose. TikTok's own UI (comments, gift buttons) covers roughly the bottom quarter and the right edge of the phone screen, so nothing that must be read goes at the bottom.

"IRL lined up with VRChat avatar" means that **the avatar panel and the IRL panel are framed the same way**: same 16:9 crop, same zoom, and Astra's head at the same height and horizontal position in both, so the two read as mirror images of each other. Get Astra to stand in place, then adjust the IRL crop (Alt+drag the edges in OBS, or use a Crop/Pad filter) until it matches the VRChat camera framing. Add a guide line to check it if that helps, then remove the guide.

## Step 1: OBS profile and scene collection

1. OBS → Profile → New → `TikTok Vertical`. Scene Collection → New → `DETOUR`.
2. Settings → Video: Base (Canvas) **1080×1920**, Output **1080×1920**, FPS **30**.
3. Settings → Output → Output Mode **Advanced**:
   - **Streaming:** encoder NVIDIA NVENC H.264, Rate Control CBR, Bitrate **6000 Kbps**, Keyframe Interval **2 s**, Preset P5 (or "Quality"), Profile high, B-frames 2. Audio track 1, AAC **160**.
   - **Recording:** Type Standard, path `C:\Users\<user>\Videos\detour-into-vr\tiktok-recordings`, format **Hybrid MP4** (crash-safe; fall back to MKV if this OBS version lacks it), encoder **NVENC H.264** (separate from the stream), Rate Control **CQP 18**. Audio tracks 1.
   - Settings → Advanced → Recording: enable "Automatically remux to MP4" if using MKV.
4. Settings → Audio: Sample Rate 48 kHz. Disable Desktop Audio and Mic/Aux at the global level. Add audio deliberately as sources (Step 3), so nothing doubles.

## Step 2: TikTok LIVE stream key

Get the server URL and stream key from **TikTok LIVE Producer** (`https://livecenter.tiktok.com/producer`, logged in as **@findastra**) → set up a LIVE → copy Server URL + Stream Key. In OBS: Settings → Stream → Service **Custom**, paste both.

- The key usually changes every session. **Get a fresh key both nights.**
- Astra types the TikTok login. Never enter the password yourself.
- If LIVE Producer does not offer a key on this account, the fallback is **TikTok LIVE Studio**: OBS → Start Virtual Camera, then in LIVE Studio add a Camera source = "OBS Virtual Camera" in a vertical layout. LIVE Studio's recording would then be the recording; keep OBS recording on as well.

## Step 3: Sources (top to bottom in the scene list = front to back)

Scene `DETOUR Live` (create sources in this order, and position with Edit Transform: right-click → Transform → Edit Transform → set Position/Size exactly):

1. **Promo Bar** (Browser Source): tick *Local file* and select `<repo>\overlay\promo-bar.html`. Width 1080, Height 96. Position 0,608. Leave "Shutdown source when not visible" off.
2. **DETOUR Twitch** (Browser Source): URL `https://player.twitch.tv/?channel=detourvr&parent=twitch.tv&muted=false&autoplay=true`, Width 1080, Height 608, Position 0,0. Tick "Control audio via OBS".
   - If the embed refuses to load (shows a "parent" error), use the fallback: open `https://www.twitch.tv/popout/detourvr/player` in Chrome/Edge in its own window, add a **Window Capture** of that window, crop to the video, size 1080×608.
   - Twitch will show its own ads at the start. Astra can't skip these without Twitch Turbo or a sub to detourvr.
3. **VRChat (main PC)** (Media Source): untick *Local File*. Input `srt://0.0.0.0:9000?mode=listener&latency=200000`, Input Format `mpegts`, tick "Restart playback when source becomes active", untick "Close file when inactive". Size 1080×608 at 0,704. The main PC sends to this (Step 4).
4. **IRL Cam** (Video Capture Device): Astra's webcam or phone-as-webcam. Ask Astra which one. Size 1080×608 at 0,1312, cropped and framed to match the VRChat panel (see "lined up" above). If the camera is 4:3, crop top/bottom to 16:9 before scaling.

Lock every source once it's placed (padlock icon) so a stray click can't move it.

### Audio: pick ONE music source or it will echo

The Twitch stream runs ~5–15 s behind VRChat, so playing both makes the music echo. Default plan:

- **VRChat (main PC)** media source: **ON**. It carries the in-world music and Astra's mic, in sync with what Astra is doing.
- **DETOUR Twitch**: **muted** in the OBS mixer (video only).
- **IRL Cam** audio: muted, unless Astra prefers the room mic. Then mute the mic on the main PC side instead.

Peak the mix around −10 dB and test with Astra talking over a loud drop. Expect TikTok to sometimes mute or flag DJ music. That's a platform risk for any DJ stream, not a setup fault.

## Step 4: Getting VRChat from the main PC to the laptop (SRT over home Wi-Fi/LAN)

No plugins needed; both PCs have OBS. **Ethernet on both machines is strongly preferred.**

1. Get the laptop's LAN IP: `ipconfig` → IPv4 (e.g. `192.168.1.xx`). The main PC is `192.168.1.70`.
2. On the laptop, allow OBS through Windows Firewall on private networks when it prompts. Astra clicks Allow; don't change firewall rules yourself.
3. Send Astra the following for the **main PC** OBS (Astra can also ask Claude on the main PC to do it):
   - New profile `To Laptop`, Video Base/Output **1920×1080**, 30 fps.
   - Settings → Stream → Service Custom, Server `srt://<LAPTOP-IP>:9000?mode=caller&latency=200000`, Stream key blank.
   - Output: encoder **AMD HW H.264 (AMF)**, CBR **10000 Kbps**, keyframe 2 s. Audio AAC 160.
   - Source: **Game Capture** or **Window Capture** of VRChat + **Desktop Audio** (VRChat world music) + **Mic**.
   - In VRChat: open the Camera, switch to **Stream** mode, and place it facing Astra's avatar (anchored to the world, or the drone). The VRChat desktop window then shows that camera view, which is what OBS captures.
   - Press **Start Streaming** on the main PC *after* the laptop's Media Source is listening.
4. On the laptop, the VRChat panel should come alive within a few seconds. If it doesn't: check IP, firewall, and that the laptop's media source was active first. Then hide/show the source to restart it.

Fallback if SRT fights you: install **DistroAV** (NDI) on both machines, or use **VDO.Ninja** (main PC shares the VRChat window in a browser; laptop adds the view link as a Browser Source).

## Step 5: TikFinity on the laptop

1. Install TikFinity desktop (https://tikfinity.zerody.one), sign in with @findastra (Astra types the password), Connect once the LIVE is running.
2. **Chatbot → Commands** (the desktop app is needed for the chatbot). Create:
   - `!detour` → `DETOUR is live in VRChat + IRL in DC! Follow them on Twitch: twitch.tv/detourvr 🎶`
   - `!follow` → `Tap + Follow on @findastra for more VR raves 💖`
   - `!lineup` → `Full lineup: vrc.tl/detour`
3. **Timed reminders in chat:** TikFinity's chatbot answers commands but has no documented timer. For automatic reminders at random intervals, pair TikFinity with **Streamer.bot**: in TikFinity's chatbot settings enable the option that lets Streamer.bot send messages, then in Streamer.bot create a Timed Action (interval ~15 min, randomized if that version offers it) that sends one of the lines above via the TikFinity integration. Check the current menu names on screen; they move between versions. Keep it to **one message every 12–20 min**, because TikTok can rate-limit or flag spammy accounts.
4. Optional overlays from TikFinity (follow alerts, follow goal) as Browser Sources. Keep them inside the top 70% of the canvas and off the right edge.

The on-screen promo bar (`overlay/promo-bar.html`) is the reliable reminder: it rotates "follow @findastra / follow DETOUR on Twitch / now playing" lines at random 10–16 s intervals with no bot account involved. The chat bot is extra.

## Step 6: Pre-flight (do this ~30 min before going live)

- [ ] Fresh TikTok stream key pasted in OBS.
- [ ] VRChat SRT feed visible and in sync; Twitch panel muted; one music source.
- [ ] IRL cam framing matches the avatar panel.
- [ ] Promo bar rotating; shows "NOW · BARN: … · BASSMENT: …" every third message.
- [ ] Recording path has >100 GB free (≈4–6 GB/hour at CQP 18 1080×1920).
- [ ] Laptop plugged in, Windows power mode "Best performance", sleep disabled for the night (Astra changes these system settings).
- [ ] Do a 2-minute private test, or watch the TikTok preview on Astra's phone, before going public.
- [ ] Start Recording **and** Start Streaming. Recording is independent: if the stream drops, recording continues.

At the end of each night: Stop Streaming, Stop Recording, confirm the MP4 plays, and note filenames + any issues in your handoff file.
