# HearthEscrow

**HearthEscrow** is a trustless milestone-escrow and arbiter-split realm built for Gno.land.

It lets two parties lock `ugnot` behind explicit milestone tranches (in basis points summing to 10,000), release funds incrementally as deliverables are approved, resolve disputes via an optional neutral arbiter with arbitrary percentage splits, and automatically unlock depositor refunds once a target block height passes — all inspectable live through `gnoweb`.

## Why HearthEscrow

Freelance bounties, DAO grants, and guild quests onchain usually fall into two extremes: full upfront trust or heavyweight multi-sig governance. HearthEscrow gives contributors and sponsors a self-contained, auditable escrow primitive in pure Gno with zero external dependencies beyond the standard library and `p/nt/*` utilities.

## Architecture

| File | Responsibility |
| --- | --- |
| `types.gno` | Lifecycle statuses (`active`, `disputed`, `completed`, `resolved`, `refunded`), `Milestone`, `DisputeRecord`, `Escrow`, `Stats`, and safety bounds |
| `errors.gno` | Sentinel error values for every validation, auth, and state-transition guard |
| `escrow.gno` | Core crossing entrypoints, AVL storage (`escrows` + `addressIndex`), accounting invariants, and `chain.Emit` events |
| `render.gno` | `gnoweb` Markdown UI (`/`, `/?status=...`, `/escrow/<id>`, `/address/<addr>`) with dynamic realm path links and copy-pasteable `gnokey` snippets |
| `escrow_test.gno` | Full GnoVM unit test suite covering happy paths, dust-free math, disputes, deadline refunds, auth guards, and `Render()` views |

### Lifecycle State Machine

```mermaid
stateDiagram-v2
    [*] --> Active: CreateEscrow (ugnot deposit)
    Active --> Active: SubmitMilestone / ApproveMilestone (partial)
    Active --> Completed: ApproveMilestone (final tranche)
    Active --> Disputed: OpenDispute (depositor or recipient)
    Disputed --> Resolved: ResolveDispute (arbiter bps split)
    Active --> Refunded: ClaimRefund (depositor, height >= deadline)
```

## Public Crossing API

- `CreateEscrow(cur realm, title string, recipient address, arbiter address, deadlineHeight int64, milestoneTitles string, milestoneBps string) uint64` — Locks the attached `ugnot` deposit into a new escrow. Pass `""` for `arbiter` if no arbiter is needed.
- `SubmitMilestone(cur realm, id uint64, milestoneIndex int, deliverable string)` — Recipient attaches a deliverable URI or note to a pending milestone.
- `ApproveMilestone(cur realm, id uint64, milestoneIndex int) int64` — Depositor approves a milestone (pending or submitted) and releases its `ugnot` tranche. Approving the final unapproved milestone sweeps any integer-division remainder so zero dust is ever trapped.
- `OpenDispute(cur realm, id uint64, reason string)` — Depositor or recipient freezes an active escrow for arbiter review.
- `ResolveDispute(cur realm, id uint64, recipientBps int64, resolutionNote string) (int64, int64)` — Arbiter splits all remaining locked funds between recipient (`recipientBps / 10000`) and depositor (the remainder).
- `ClaimRefund(cur realm, id uint64) int64` — Depositor reclaims remaining locked funds once `runtime.ChainHeight() >= deadlineHeight` (blocked while a dispute is open).

Read-only queries: `GetEscrow(id uint64) *Escrow`, `GetStats() Stats`, `GetAddressEscrowIDs(addr address) []uint64`, and `Render(path string) string`.

## Security Invariants

1. **Direct EOA guard on deposits:** `CreateEscrow` requires `cur.Previous().IsUserCall()` before reading `unsafe.OriginSend()`, preventing indirect `maketx run` or intermediate-realm coin-envelope confusion.
2. **Realm solvency check:** Every deposit verifies the realm's live `ugnot` balance is at least `stats.TotalLocked + amount`.
3. **Checks-Effects-Interactions (CEI):** Every payout and refund updates milestone/escrow status, balances, and protocol stats before calling `banker.SendCoins`.
4. **Overflow-safe & dust-free math:** Deposits are bounded by `math.MaxInt64 / 10000`, milestone basis points must be positive and sum to exactly `10000`, and the final milestone approval sweeps the exact remaining `ugnot`.
5. **Dispute protection:** An open dispute freezes the escrow — neither milestone approvals nor deadline refunds can bypass the arbiter.
6. **Zero-send protection:** `ResolveDispute` skips `SendCoins` for any side whose share is `0` (0 bps or 10,000 bps splits).

## `gnoweb` Routes

- `/` — Protocol dashboard with TVL locked, total released, status counts, filter bar (`All`, `Active`, `Disputed`, `Closed`), and escrow table.
- `/escrow/<id>` — Full escrow detail view with progress bar, party links, milestones table, dispute record, and ready-to-run `gnokey` commands.
- `/address/<addr>` — Per-address portfolio showing counts and volume across Depositor, Recipient, and Arbiter roles.

## Running Tests Locally

Requires the Gno CLI (`gno`) built from [gnolang/gno](https://github.com/gnolang/gno):

```bash
gno test -v .
```

If running against a local checkout of `gnolang/gno`, pass `-root-dir <path-to-gno-repo>`:

```bash
gno test -root-dir <path-to-gno-repo> -v .
```

## Testnet deployment (Onyx)

HearthEscrow is **live** on the Gno Onyx testnet (`onyx-1`). `qpkgmeta_json` reports `status=live` (first confirmed 2026-11-24, 4:13 PM ET; still `live` after the smoke tests). `Render` and crossing calls work. Browse the realm on gnoweb, and track package status on [gpas](https://gpas.onyx.testnets.gno.land/?path=gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow).

| | |
| --- | --- |
| Chain ID | `onyx-1` |
| RPC | `https://rpc.onyx.testnets.gno.land:443` |
| Realm path | `gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow` |
| gnoweb dashboard | [onyx.testnets.gno.land/r/…/hearthescrow](https://onyx.testnets.gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow) |
| gnoweb escrow #1 (released / completed) | […:escrow/1](https://onyx.testnets.gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow:escrow/1) |
| gnoweb escrow #2 (refunded) | […:escrow/2](https://onyx.testnets.gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow:escrow/2) |
| Deploy transaction (base64) | `hls9k2tXcqr4tR3+lo/bBiVOEq6K7MzF3taIspfUEUs=` |
| Deploy transaction (hex) | `865B3D936B5772AAF8B51DFE968FDB06254E12AE8AECCCC5DED688B297D4114B` |
| Deploy height | `1353513` (2026-11-23, 9:24:44 AM ET) |
| Package status | `live` (on-chain `qpkgmeta_json`, height `1353513`) |

### Smoke tests (2026-11-24, 4:18–4:19 PM ET)

Two real crossing-call flows were broadcast from the throwaway Onyx deployer `g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n`, with throwaway recipient `g1w2ersazyzwlwgxh3vwpmeewtkkn8zdqw59pff2`. After the runs, `Render("")` showed **2** escrows, **1** completed, **1** refunded, **0** TVL locked, and **1 GNOT** total released. Every hash below was re-checked against the Onyx RPC (`/tx?hash=0x…`) and the gnoscope API (`/api/tx/<hex>?network=onyx`). Explorer links use [gnoscope](https://gnoscope.com/?network=onyx) (official Onyx explorer alias: `https://explorer.onyx.testnets.gno.land`).

| Step | Height | Time (ET) | Gas used / wanted | Tx (base64) | Tx (hex) / explorer |
| --- | --- | --- | --- | --- | --- |
| Fund recipient `1_000_000ugnot` | `1385769` | 4:18:25 PM | `1238010` / `10000000` | `Awr+Pr4BPl2zFnhmczzsbJ5F5kgNYfmnGlDGMZWoP8g=` | [`030AFE3E…A83FC8`](https://gnoscope.com/tx/030AFE3EBE013E5DB3167866733CEC6C9E45E6480D61F9A71A50C63195A83FC8?network=onyx) |
| `CreateEscrow` #1 “Smoke Release” (1 GNOT, 1 milestone, no arbiter) | `1385770` | 4:18:28 PM | `7948809` / `10000000` | `evcIxdh6XL9otqAtXIbG0czOZ6reLsskoTIRE/Hp/F0=` | [`7AF708C5…E9FC5D`](https://gnoscope.com/tx/7AF708C5D87A5CBF68B6A02D5C86C6D1CCCE67AADE2ECB24A1321113F1E9FC5D?network=onyx) |
| `SubmitMilestone` #1 / index 0 (recipient) | `1385772` | 4:18:35 PM | `6229371` / `10000000` | `SQrtx27HmtyJDTaTS79VTXf10I1df83iaN3q+ohuZ1M=` | [`490AEDC7…6E6753`](https://gnoscope.com/tx/490AEDC76EC79ADC890D36934BBF554D77F5D08D5D7FCDE268DDEAFA886E6753?network=onyx) |
| `ApproveMilestone` #1 / index 0 (release / completed) | `1385774` | 4:18:42 PM | `7236768` / `10000000` | `MmORzSEDf++mHG/2LhHb9Xch8eM19xJklLZEYAsumQw=` | [`326391CD…2E990C`](https://gnoscope.com/tx/326391CD21037FEFA61C6FF62E11DBF57721F1E335F7126494B644600B2E990C?network=onyx) |
| `CreateEscrow` #2 “Smoke Refund” (deadline height `1385782`) | `1385776` | 4:18:48 PM | `8665309` / `10000000` | `+R/sA3/rYxhW/waJVAOXFoJAawjshIdS5KhblCOSBTQ=` | [`F91FEC03…920534`](https://gnoscope.com/tx/F91FEC037FEB631856FF06895403971682406B08EC848752E4A85B9423920534?network=onyx) |
| `ClaimRefund` #2 (refunded) | `1385783` | 4:19:12 PM | `6860224` / `10000000` | `wtJdTQZOhgIFGDMy+ifCuSUIFIuzHPnO16BtbW/mGkc=` | [`C2D25D4D…E61A47`](https://gnoscope.com/tx/C2D25D4D064E860205183332FA27C2B92508148BB31CF9CED7A06D6D6FE61A47?network=onyx) |

Full command details, gas fees, and post-tx `Render` notes are in [DEPLOYMENTS.md](./DEPLOYMENTS.md). A walkthrough of the live realm and these transactions is in [demo/](./demo/).

## Example CLI Flow (`gnokey`)

```bash
# 1. Create a 2-milestone escrow with 1 GNOT (1,000,000 ugnot)
gnokey maketx call -pkgpath "gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow" \
  -func CreateEscrow -send 1000000ugnot \
  -args "Landing Page Build" -args <recipient_addr> -args <arbiter_addr> -args 500000 \
  -args "Wireframes,Production Build" -args "4000,6000" \
  -gas-fee 100000ugnot -gas-wanted 10000000 \
  -chainid onyx-1 -remote https://rpc.onyx.testnets.gno.land:443 \
  <depositor_key>

# 2. Recipient submits milestone 0
gnokey maketx call -pkgpath "gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow" \
  -func SubmitMilestone -args 1 -args 0 -args "https://example.com/wireframes" \
  -gas-fee 100000ugnot -gas-wanted 10000000 \
  -chainid onyx-1 -remote https://rpc.onyx.testnets.gno.land:443 \
  <recipient_key>

# 3. Depositor approves milestone 0 (releases 400,000 ugnot)
gnokey maketx call -pkgpath "gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow" \
  -func ApproveMilestone -args 1 -args 0 \
  -gas-fee 100000ugnot -gas-wanted 10000000 \
  -chainid onyx-1 -remote https://rpc.onyx.testnets.gno.land:443 \
  <depositor_key>
```

## License

MIT — see [LICENSE](./LICENSE).
