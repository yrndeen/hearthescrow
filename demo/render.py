#!/usr/bin/env python3
"""Render the HearthEscrow demo: gnoweb stills + asciinema terminal + Piper narration.

Pipeline follows the Patchbrief demo renderer (pyte frames, OSC captions, two-pass
loudnorm). Visuals include Playwright captures of the live Onyx gnoweb pages.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import wave
from pathlib import Path

import pyte
from PIL import Image, ImageDraw, ImageFont

COLS, ROWS = 100, 38
W, H = 1280, 800
TERM_H = 690
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
GAP_LIMIT, CUT_TO, FPS = 8.0, 2.0, 10
PIPER = str(Path.home() / ".local/bin/piper")
VOICE = str(Path.home() / ".local/share/piper-voices/en_US-ljspeech-medium.onnx")
# About -16 LUFS; true peak <= -1.5 dBTP as required.
LOUDNORM = "loudnorm=I=-16:TP=-1.5:LRA=11"

CAPTIONS = {
    0: "HearthEscrow is a pure-Gno milestone escrow realm, now live on the Gno.land Onyx testnet.",
    1: "The live gnoweb dashboard shows two real smoke-test escrows: one completed release, and one deadline refund.",
    2: "Escrow one locked one GNOT. The recipient submitted a deliverable, the depositor approved it, and the full tranche was released.",
    3: "Escrow two hit its block-height deadline, and the depositor claimed a full refund. Nothing stayed locked.",
    4: "On-chain package metadata reports status live, and Render is served from the same Onyx RPC.",
    5: "Live Render views confirm escrow one completed and escrow two refunded, with the Onyx transaction hashes in the README.",
    6: "Seven unit test suites pass locally, covering dust-free math, dispute freezes, and deadline refunds. HearthEscrow is MIT-licensed and open source.",
}

COLORS = {
    "default": (220, 220, 220), "black": (40, 40, 40), "red": (240, 90, 90), "green": (110, 210, 110),
    "brown": (220, 190, 90), "yellow": (230, 210, 100), "blue": (110, 150, 240), "magenta": (210, 120, 210),
    "cyan": (100, 200, 210), "white": (235, 235, 235),
}
OSC = re.compile(r"\x1b\]1337;PBCAP=(\d+)\x07")

font = ImageFont.truetype(FONT, 16)
font_b = ImageFont.truetype(FONT_B, 16)
cap_font = ImageFont.truetype(SANS, 24)
cw = font.getbbox("M")[2]
lh = TERM_H // ROWS
DEMO = Path("/workspace/bounties/hearthescrow/demo")


def wrap(text: str, fnt, width: int) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if fnt.getlength(trial) > width and cur:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur]


def draw_caption(img: Image.Image, cap: int | None, banner: str | None) -> None:
    d = ImageDraw.Draw(img)
    d.rectangle([0, TERM_H, W, H], fill=(18, 18, 30))
    if cap is not None:
        for i, ln in enumerate(wrap(CAPTIONS[cap], cap_font, W - 80)[:3]):
            d.text((40, TERM_H + 14 + i * 32), ln, font=cap_font, fill=(255, 255, 255))
    if banner:
        tw = font_b.getlength(banner)
        y = TERM_H - 46
        d.rectangle([W - tw - 40, y, W - 10, y + 34], fill=(200, 60, 60))
        d.text((W - tw - 25, y + 7), banner, font=font_b, fill=(255, 255, 255))


def frame_from_shot(shot: Path, cap: int | None) -> Image.Image:
    src = Image.open(shot).convert("RGB")
    img = Image.new("RGB", (W, H), (12, 12, 16))
    # Fit the screenshot into the terminal area, preserving aspect.
    src = src.resize((W, TERM_H), Image.Resampling.LANCZOS) if src.size != (W, TERM_H) else src
    # If aspect differs, letterbox.
    if src.size != (W, TERM_H):
        src.thumbnail((W, TERM_H), Image.Resampling.LANCZOS)
        x = (W - src.width) // 2
        y = (TERM_H - src.height) // 2
        img.paste(src, (x, y))
    else:
        img.paste(src, (0, 0))
    draw_caption(img, cap, None)
    return img


def render_screen(screen: pyte.Screen, cap: int | None, banner: str | None) -> Image.Image:
    img = Image.new("RGB", (W, H), (12, 12, 16))
    d = ImageDraw.Draw(img)
    x0 = (W - COLS * cw) // 2
    for y in range(ROWS):
        row = screen.buffer[y]
        for x in range(COLS):
            ch = row[x]
            if ch.data.strip():
                color = COLORS.get(ch.fg, COLORS["default"])
                d.text((x0 + x * cw, 4 + y * lh), ch.data, font=font_b if ch.bold else font, fill=color)
    draw_caption(img, cap, banner)
    return img


def title_card() -> Image.Image:
    img = Image.new("RGB", (W, H), (12, 12, 16))
    d = ImageDraw.Draw(img)
    big = ImageFont.truetype(SANS, 64)
    mid = ImageFont.truetype(SANS, 28)
    small = ImageFont.truetype(SANS, 22)
    d.text((W // 2, 200), "HearthEscrow", font=big, fill=(255, 255, 255), anchor="mm")
    d.text((W // 2, 280), "Trustless milestone escrow on Gno.land", font=mid, fill=(180, 200, 255), anchor="mm")
    d.text((W // 2, 330), "Live on Onyx testnet  ·  smoke-tested 24 Nov 2026 ET", font=small, fill=(160, 160, 160), anchor="mm")
    d.text((W // 2, 400), "onyx.testnets.gno.land/r/…/hearthescrow", font=small, fill=(140, 180, 160), anchor="mm")
    draw_caption(img, 0, None)
    return img


def end_card() -> Image.Image:
    img = Image.new("RGB", (W, H), (12, 12, 16))
    d = ImageDraw.Draw(img)
    mid = ImageFont.truetype(SANS, 32)
    small = ImageFont.truetype(SANS, 22)
    d.text((W // 2, 240), "HearthEscrow is live on Onyx", font=mid, fill=(255, 255, 255), anchor="mm")
    d.text((W // 2, 310), "github.com/yrndeen/hearthescrow", font=small, fill=(180, 200, 255), anchor="mm")
    d.text((W // 2, 360), "MIT license  ·  no music  ·  see demo/CREDITS.md", font=small, fill=(160, 160, 160), anchor="mm")
    draw_caption(img, 6, None)
    return img


def tts(text: str, out: Path) -> float:
    subprocess.run([PIPER, "--model", VOICE, "--output_file", str(out)], input=text.encode(), check=True,
                   capture_output=True)
    with wave.open(str(out)) as w:
        return w.getnframes() / w.getframerate()


def main(cast_path: str, out_dir: str) -> None:
    out = Path(out_dir)
    frames_dir = out / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    for f in frames_dir.glob("*.png"):
        f.unlink()
    lines = Path(cast_path).read_text().splitlines()
    events = [json.loads(ln) for ln in lines[1:] if ln.strip()]

    screen = pyte.Screen(COLS, ROWS)
    stream = pyte.Stream(screen)
    frames: list[tuple[Path, float]] = []
    cuts: list[dict] = []
    cap_starts: dict[int, float] = {}
    voice_dir = out / "voice"
    voice_dir.mkdir(exist_ok=True)

    t_out = 0.0
    idx = 0

    def emit(img: Image.Image, dur: float) -> None:
        nonlocal idx, t_out
        p = frames_dir / f"f{idx:05d}.png"
        img.save(p)
        frames.append((p, dur))
        idx += 1
        t_out += dur

    voice_len = {k: tts(v, voice_dir / f"cap{k}.wav") for k, v in CAPTIONS.items()}

    # Title + live gnoweb stills (captions 0–3), then the terminal recording (4–6).
    cap_starts[0] = 0.0
    emit(title_card(), max(4.0, voice_len[0] + 0.5))

    shots = [
        (1, DEMO / "shots" / "dashboard.png"),
        (2, DEMO / "shots" / "escrow1.png"),
        (3, DEMO / "shots" / "escrow2.png"),
    ]
    for cap_id, shot in shots:
        cap_starts[cap_id] = t_out
        emit(frame_from_shot(shot, cap_id), max(4.0, voice_len[cap_id] + 0.5))

    cap: int | None = 3
    prev_t, acc, banner_until, banner = 0.0, 0.0, -1.0, None

    def flush() -> None:
        nonlocal acc
        if acc > 0:
            emit(render_screen(screen, cap, banner if t_out < banner_until else None), acc)
            acc = 0.0

    for ev in events:
        t, kind, data = ev[0], ev[1], ev[2]
        if kind != "o":
            continue
        gap = t - prev_t
        prev_t = t
        if gap > GAP_LIMIT:
            flush()
            cut = round(gap - CUT_TO)
            banner = f"[wait cut: {cut}s]"
            cuts.append({"at_out_s": round(t_out, 1), "real_gap_s": round(gap, 1), "cut_s": cut})
            emit(render_screen(screen, cap, banner), CUT_TO)
            banner_until = t_out + 2.5
        else:
            acc += gap
            if acc >= 1 / FPS:
                flush()
        for m in OSC.finditer(data):
            flush()
            if cap is not None:
                need = cap_starts.get(cap, t_out) + voice_len.get(cap, 0) + 0.3 - t_out
                if need > 0:
                    emit(render_screen(screen, cap, None), need)
            cap = int(m.group(1))
            cap_starts[cap] = t_out
        stream.feed(OSC.sub("", data))
    flush()
    tail = max(1.5, cap_starts.get(cap, 0) + voice_len.get(cap, 0) + 0.6 - t_out)
    emit(render_screen(screen, cap, None), tail)
    emit(end_card(), 2.2)

    concat = out / "frames.txt"
    with concat.open("w") as fh:
        for p, dur in frames:
            if dur >= 0.01:
                fh.write(f"file '{p.resolve()}'\nduration {dur:.3f}\n")
        fh.write(f"file '{frames[-1][0].resolve()}'\n")

    inputs, filters = [], []
    for i, (k, start) in enumerate(sorted(cap_starts.items(), key=lambda kv: kv[1])):
        inputs += ["-i", str(voice_dir / f"cap{k}.wav")]
        filters.append(f"[{i}:a]adelay={int(start * 1000)}:all=1[a{i}]")
    n = len(filters)
    mix = ";".join(filters) + ";" + "".join(f"[a{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0,volume=1.0[aout]"
    voice = out / "voice.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", mix, "-map", "[aout]",
                    "-ar", "44100", str(voice)], check=True)

    probe = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(voice), "-af", f"{LOUDNORM}:print_format=json",
                            "-f", "null", "-"], check=True, capture_output=True, text=True).stderr
    m = json.loads(probe[probe.rindex("{"):probe.rindex("}") + 1])
    voice_norm = out / "voice-norm.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(voice), "-af",
                    f"{LOUDNORM}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
                    f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true",
                    "-ar", "44100", str(voice_norm)], check=True)

    mp4 = out / "hearthescrow-demo.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat),
                    "-i", str(voice_norm), "-af", "apad", "-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264",
                    "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "160k",
                    "-t", f"{t_out:.2f}", "-movflags", "+faststart", str(mp4)],
                   check=True)
    print(json.dumps({"duration_s": round(t_out, 1), "cuts": cuts, "voice_lens": {k: round(v, 2) for k, v in voice_len.items()}}, indent=2))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
