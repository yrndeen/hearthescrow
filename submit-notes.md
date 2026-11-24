# HearthEscrow — submission notes (Gnome Tavern / DoraHacks)

These notes are for crypto Scout's DoraHacks submission. **This file is not a submission.** Nothing has been posted to DoraHacks.

- **Prepared:** 2026-11-24, ~4:20 PM ET
- **Hackathon:** Gnome Tavern (https://dorahacks.io/hackathon/gnome-tavern/detail)
- **Deadline:** Thursday, Dec 17, 2026, 8:00 PM ET
- **Project name:** HearthEscrow
- **Recommended tagline:** Trustless milestone escrow, arbiter dispute splits, and block-height refunds in pure Gno.
- **Draft copy:** `qa/dorahacks_submission_draft.md`

## Links

| What | URL |
| --- | --- |
| Public GitHub | https://github.com/yrndeen/hearthescrow |
| Live gnoweb dashboard | https://onyx.testnets.gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow |
| gnoweb escrow #1 (completed / released) | https://onyx.testnets.gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow:escrow/1 |
| gnoweb escrow #2 (refunded) | https://onyx.testnets.gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow:escrow/2 |
| Recipient portfolio | https://onyx.testnets.gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow:address/g1w2ersazyzwlwgxh3vwpmeewtkkn8zdqw59pff2 |
| GPAS package status | https://gpas.onyx.testnets.gno.land/?path=gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow |
| Tx explorer (Onyx) | https://gnoscope.com/?network=onyx (alias https://explorer.onyx.testnets.gno.land) |
| Demo video | `demo/hearthescrow-demo.mp4` in the repo |

## On-chain status (verified 2026-11-24, 4:13–4:19 PM ET)

- Chain: `onyx-1`, RPC `https://rpc.onyx.testnets.gno.land:443`
- Realm: `gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow`
- `gnokey query vm/qpkgmeta_json` → `status":"live"`, `creator` `g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n`, `height` `1353513`, `max_deposit` `50000000ugnot`
- `gnokey query vm/qrender` works. After the smoke tests: 2 escrows, 1 completed, 1 refunded, 0 TVL locked, 1 GNOT total released.

## Deploy (`addpkg`)

| Field | Value |
| --- | --- |
| Tx (base64) | `hls9k2tXcqr4tR3+lo/bBiVOEq6K7MzF3taIspfUEUs=` |
| Tx (hex) | `865B3D936B5772AAF8B51DFE968FDB06254E12AE8AECCCC5DED688B297D4114B` |
| Height | `1353513` (2026-11-23, 9:24:44 AM ET) |
| Gas used / wanted | `64806955` / `70000000` |
| Explorer | https://gnoscope.com/tx/865B3D936B5772AAF8B51DFE968FDB06254E12AE8AECCCC5DED688B297D4114B?network=onyx |

## Smoke-test transactions (2026-11-24, 4:18–4:19 PM ET)

Throwaway Onyx deployer `g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n`; throwaway recipient `g1w2ersazyzwlwgxh3vwpmeewtkkn8zdqw59pff2`. Each hash was checked on the Onyx RPC and on `https://gnoscope.com/api/tx/<hex>?network=onyx` (`success: true`). gnoweb dashboard and both escrow pages returned HTTP 200 with matching status text.

| Step | Height | Time (ET) | Gas used / wanted | Tx (base64) | Explorer |
| --- | --- | --- | --- | --- | --- |
| Fund recipient `1_000_000ugnot` | `1385769` | 4:18:25 PM | `1238010` / `10000000` | `Awr+Pr4BPl2zFnhmczzsbJ5F5kgNYfmnGlDGMZWoP8g=` | https://gnoscope.com/tx/030AFE3EBE013E5DB3167866733CEC6C9E45E6480D61F9A71A50C63195A83FC8?network=onyx |
| `CreateEscrow` #1 “Smoke Release” | `1385770` | 4:18:28 PM | `7948809` / `10000000` | `evcIxdh6XL9otqAtXIbG0czOZ6reLsskoTIRE/Hp/F0=` | https://gnoscope.com/tx/7AF708C5D87A5CBF68B6A02D5C86C6D1CCCE67AADE2ECB24A1321113F1E9FC5D?network=onyx |
| `SubmitMilestone` #1 index 0 | `1385772` | 4:18:35 PM | `6229371` / `10000000` | `SQrtx27HmtyJDTaTS79VTXf10I1df83iaN3q+ohuZ1M=` | https://gnoscope.com/tx/490AEDC76EC79ADC890D36934BBF554D77F5D08D5D7FCDE268DDEAFA886E6753?network=onyx |
| `ApproveMilestone` #1 index 0 (release) | `1385774` | 4:18:42 PM | `7236768` / `10000000` | `MmORzSEDf++mHG/2LhHb9Xch8eM19xJklLZEYAsumQw=` | https://gnoscope.com/tx/326391CD21037FEFA61C6FF62E11DBF57721F1E335F7126494B644600B2E990C?network=onyx |
| `CreateEscrow` #2 “Smoke Refund” (deadline `1385782`) | `1385776` | 4:18:48 PM | `8665309` / `10000000` | `+R/sA3/rYxhW/waJVAOXFoJAawjshIdS5KhblCOSBTQ=` | https://gnoscope.com/tx/F91FEC037FEB631856FF06895403971682406B08EC848752E4A85B9423920534?network=onyx |
| `ClaimRefund` #2 | `1385783` | 4:19:12 PM | `6860224` / `10000000` | `wtJdTQZOhgIFGDMy+ifCuSUIFIuzHPnO16BtbW/mGkc=` | https://gnoscope.com/tx/C2D25D4D064E860205183332FA27C2B92508148BB31CF9CED7A06D6D6FE61A47?network=onyx |

Local unit tests (`gno test -v -root-dir /workspace/tools/gno-src .`) still pass: 7/7 suites, `ok 1.24s`, re-run 2026-11-24 ET.

## Local files to attach or point at

- README + DEPLOYMENTS (tx table and gnoweb links)
- `demo/hearthescrow-demo.mp4` (and `demo/CREDITS.md`)
- This notes file
