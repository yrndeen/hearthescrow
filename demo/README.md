# HearthEscrow demo

`hearthescrow-demo.mp4` is a ~63-second walkthrough of the live Onyx realm: gnoweb stills of the dashboard and both smoke-test escrows, then a terminal recording of `qpkgmeta_json`, `Render`, and `gno test`. Narration is Piper `en_US-ljspeech-medium` (public domain; see `CREDITS.md`). No music.

Recorded 2026-11-24, ~4:27 PM ET. Resolution 1280×800.

To rebuild (after `playwright install chromium` and a venv with `pyte`, `pillow`, and `asciinema`):

```bash
python demo/capture_gnoweb.py
asciinema rec --overwrite --cols 100 --rows 38 -c demo/demo-steps.sh demo/hearthescrow-demo-raw.cast
python demo/render.py demo/hearthescrow-demo-raw.cast demo/build
```
