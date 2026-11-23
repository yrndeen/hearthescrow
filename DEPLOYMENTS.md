# Deployments

## Onyx testnet (`onyx-1`)

| Field | Value |
| --- | --- |
| Chain ID | `onyx-1` |
| RPC | `https://rpc.onyx.testnets.gno.land:443` |
| Realm path | `gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow` |
| gnoweb | https://onyx.testnets.gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow |
| Package status page | https://gpas.onyx.testnets.gno.land/?path=gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow |
| Deployer | `g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n` |
| `addpkg` transaction (base64) | `hls9k2tXcqr4tR3+lo/bBiVOEq6K7MzF3taIspfUEUs=` |
| `addpkg` transaction (hex) | `865B3D936B5772AAF8B51DFE968FDB06254E12AE8AECCCC5DED688B297D4114B` |
| Deploy height | `1353513` |
| Deploy time | 2026-11-23, 9:24:44 AM ET (`2026-11-23T14:24:44Z`) |
| Gas used / wanted | `64806955` / `70000000` |
| Gas fee | `100000ugnot` |
| Max storage deposit cap | `50000000ugnot` |
| On-chain status after `addpkg` | `inert`, pending package-approver (gpao) enablement |
| Deployer balance after `addpkg` | `99900000ugnot` |
| Smoke-test transaction | *Pending — the realm must be enabled by gpao before crossing calls or `Render("")` can run. On Onyx, packages that pass review are typically enabled about one hour after the verdict.* |

Query package metadata:

```bash
gnokey query vm/qpkgmeta_json \
  -data "gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow" \
  -remote https://rpc.onyx.testnets.gno.land:443
```

Once enabled, `Render("")` is:

```bash
gnokey query vm/qrender \
  -data "gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow:" \
  -remote https://rpc.onyx.testnets.gno.land:443
```
