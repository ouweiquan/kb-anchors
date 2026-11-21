# KB Anchors — 公开锚定证据（紧凑口径）

���仓为私有仓 `ouweiquan/kb-system` 的**外部时间戳证据**公开处，只公开「事实」，不公开文件清单。

## 文件

- `anchors/<id>.txt` — 单个锚点的紧凑证明，含：`anchor_id` / `manifest_sha256` / `manifest_files` / `merkle_root` / `ots_b64`
- `merkle/*.json` — 单文件 Merkle 证明（可验至 `merkle_root`）
- `anchors/anchor_ledger.csv` — 历史锚点台账

## 第三方验证（三���）

1. `grep '^ots_b64:' <id>.txt | sed 's/^ots_b64: *//' | base64 -d > <id>.sha256.ots`
2. `ots verify <id>.sha256.ots` —— 证明该哈希在某比特币区块时间前已存在
3. 该哈希 = 私有仓 MANIFEST 全量清单的 sha256；任一文件用 `merkle/` 下的证明验至 `merkle_root`

不再发布完整清单，避免泄露私有仓文件结构。历史上曾发布过完整清单（seq≤31），已停止。
