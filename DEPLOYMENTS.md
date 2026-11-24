# Deployments

## Onyx testnet (`onyx-1`)

| Field | Value |
| --- | --- |
| Chain ID | `onyx-1` |
| RPC | `https://rpc.onyx.testnets.gno.land:443` |
| Realm path | `gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow` |
| gnoweb dashboard | https://onyx.testnets.gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow |
| gnoweb escrow #1 (released / completed) | https://onyx.testnets.gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow:escrow/1 |
| gnoweb escrow #2 (refunded) | https://onyx.testnets.gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow:escrow/2 |
| gnoweb recipient portfolio | https://onyx.testnets.gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow:address/g1w2ersazyzwlwgxh3vwpmeewtkkn8zdqw59pff2 |
| Package status page | https://gpas.onyx.testnets.gno.land/?path=gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow |
| Tx explorer | https://gnoscope.com/?network=onyx (official alias: https://explorer.onyx.testnets.gno.land) |
| Deployer | `g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n` |
| Smoke-test recipient (throwaway) | `g1w2ersazyzwlwgxh3vwpmeewtkkn8zdqw59pff2` |
| `addpkg` transaction (base64) | `hls9k2tXcqr4tR3+lo/bBiVOEq6K7MzF3taIspfUEUs=` |
| `addpkg` transaction (hex) | `865B3D936B5772AAF8B51DFE968FDB06254E12AE8AECCCC5DED688B297D4114B` |
| Deploy height | `1353513` |
| Deploy time | 2026-11-23, 9:24:44 AM ET (`2026-11-23T14:24:44Z`) |
| Gas used / wanted | `64806955` / `70000000` |
| Gas fee | `100000ugnot` |
| Max storage deposit cap | `50000000ugnot` |
| On-chain status after `addpkg` | `inert`, pending package-approver (gpao) enablement |
| On-chain status now | `live` — `qpkgmeta_json` `status=live` at creator height `1353513` (confirmed 2026-11-24, 4:13 PM ET and re-checked after smoke tests). `Render("")` works. |
| Deployer balance after `addpkg` | `99900000ugnot` |
| Deployer balance after smoke tests | `89433500ugnot` (account sequence `6`) |
| Recipient balance after smoke tests | `1889800ugnot` (1 GNOT funded + 1 GNOT released from escrow #1, minus the recipient's submit fee) |

### Smoke-test transactions (2026-11-24, 4:18–4:19 PM ET)

All calls used `-gas-fee 100000ugnot -gas-wanted 10000000 -chainid onyx-1` against `https://rpc.onyx.testnets.gno.land:443`. Crossing `CreateEscrow` calls also set `-max-deposit 10000000ugnot` and attached `-send 1000000ugnot`. Each hash was verified on the Onyx RPC (`/tx?hash=0x<hex>`) and on `https://gnoscope.com/api/tx/<hex>?network=onyx` (`success: true`). gnoweb pages for the dashboard and both escrow routes returned HTTP 200 with the expected titles/status after the runs.

| Step | Height | Time (ET) | Gas used / wanted | Tx (base64) | Explorer (hex) |
| --- | --- | --- | --- | --- | --- |
| Fund recipient `1_000_000ugnot` | `1385769` | 4:18:25 PM | `1238010` / `10000000` | `Awr+Pr4BPl2zFnhmczzsbJ5F5kgNYfmnGlDGMZWoP8g=` | [030AFE3E…A83FC8](https://gnoscope.com/tx/030AFE3EBE013E5DB3167866733CEC6C9E45E6480D61F9A71A50C63195A83FC8?network=onyx) |
| `CreateEscrow` #1 “Smoke Release” (deadline `1585769`, 1×10000 bps, no arbiter) | `1385770` | 4:18:28 PM | `7948809` / `10000000` | `evcIxdh6XL9otqAtXIbG0czOZ6reLsskoTIRE/Hp/F0=` | [7AF708C5…E9FC5D](https://gnoscope.com/tx/7AF708C5D87A5CBF68B6A02D5C86C6D1CCCE67AADE2ECB24A1321113F1E9FC5D?network=onyx) |
| `SubmitMilestone` #1 index 0 (recipient) | `1385772` | 4:18:35 PM | `6229371` / `10000000` | `SQrtx27HmtyJDTaTS79VTXf10I1df83iaN3q+ohuZ1M=` | [490AEDC7…6E6753](https://gnoscope.com/tx/490AEDC76EC79ADC890D36934BBF554D77F5D08D5D7FCDE268DDEAFA886E6753?network=onyx) |
| `ApproveMilestone` #1 index 0 — release, status `completed` | `1385774` | 4:18:42 PM | `7236768` / `10000000` | `MmORzSEDf++mHG/2LhHb9Xch8eM19xJklLZEYAsumQw=` | [326391CD…2E990C](https://gnoscope.com/tx/326391CD21037FEFA61C6FF62E11DBF57721F1E335F7126494B644600B2E990C?network=onyx) |
| `CreateEscrow` #2 “Smoke Refund” (deadline `1385782`) | `1385776` | 4:18:48 PM | `8665309` / `10000000` | `+R/sA3/rYxhW/waJVAOXFoJAawjshIdS5KhblCOSBTQ=` | [F91FEC03…920534](https://gnoscope.com/tx/F91FEC037FEB631856FF06895403971682406B08EC848752E4A85B9423920534?network=onyx) |
| `ClaimRefund` #2 — status `refunded` (closed at `1385783`; deadline reached at `1385782`, 4:19:09 PM ET) | `1385783` | 4:19:12 PM | `6860224` / `10000000` | `wtJdTQZOhgIFGDMy+ifCuSUIFIuzHPnO16BtbW/mGkc=` | [C2D25D4D…E61A47](https://gnoscope.com/tx/C2D25D4D064E860205183332FA27C2B92508148BB31CF9CED7A06D6D6FE61A47?network=onyx) |

`Render` after the final refund (also confirmed on gnoweb): **2** total escrows, **0** active, **1** completed, **1** refunded, TVL locked **0**, total released **1 GNOT (1000000 ugnot)**. Escrow #1 paid the full 1 GNOT tranche to the recipient. Escrow #2 returned the full 1 GNOT to the depositor.

Query package metadata:

```bash
gnokey query vm/qpkgmeta_json \
  -data "gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow" \
  -remote https://rpc.onyx.testnets.gno.land:443
```

`Render("")` (dashboard) and per-escrow views:

```bash
gnokey query vm/qrender \
  -data "gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow:" \
  -remote https://rpc.onyx.testnets.gno.land:443

gnokey query vm/qrender \
  -data "gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow:escrow/1" \
  -remote https://rpc.onyx.testnets.gno.land:443

gnokey query vm/qrender \
  -data "gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow:escrow/2" \
  -remote https://rpc.onyx.testnets.gno.land:443
```
