# Demo credits

The demo video (`hearthescrow-demo.mp4`, rendered by `demo/render.py` from `hearthescrow-demo-raw.cast` plus live gnoweb screenshots) uses:

| Asset | Source | Licence |
|---|---|---|
| Narration voice: Piper TTS `en_US-ljspeech-medium` | https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US/ljspeech/medium (model card: https://huggingface.co/rhasspy/piper-voices/raw/main/en/en_US/ljspeech/medium/MODEL_CARD) | Trained on the LJ Speech dataset (https://keithito.com/LJ-Speech-Dataset/), which the model card lists as **public domain**. |
| TTS engine: `piper`, run locally | https://github.com/OHF-Voice/piper1-gpl | GPL-3.0-or-later. Used as a local tool to generate the audio; no Piper code ships in this repo. |
| Font: DejaVu Sans / DejaVu Sans Mono | https://dejavu-fonts.github.io/ | DejaVu Fonts licence (free, permissive). |
| Terminal footage | Real `gnokey` queries against Onyx and `gno test` on this repo, recorded with asciinema | Ours (MIT, see `LICENSE`). |
| Browser stills | Live gnoweb pages on `onyx.testnets.gno.land` | Public testnet UI; captured for this demo. |

No music, sound effects or other third-party audio is used. Narration is loudness-normalised to about -16 LUFS with true peak at or below -1.5 dBTP (ffmpeg `loudnorm`, two-pass).
