# kb-anchors · 公开心跳证据（比特币时间戳）

本仓只存放**证据**，不含任何策略内容。作用：让任何人**无需账号、无需信任**地验证
「某个哈希确实在某个比特币区块之前就已经存在」。

## 文件形态

| 文件 | 内容 |
|---|---|
| `anchors/YYYYMMDD-HHMM-<hash8>.txt` | 一行：`<完整 sha256>  MANIFEST.sha256` —— 当轮归档清单的哈希 |
| 同名 `.txt.ots` | OpenTimestamps 证明：上述 `.txt` 文件字节已提交至 4 个互不隶属的 calendar |

母仓保持私有，但**哈希可公开验证**——验证只关心"这串字节在何时已存在"，不看内容。

## 如何独立验证

```bash
pip install opentimestamps-client
git clone https://github.com/ouweiquan/kb-anchors && cd kb-anchors/anchors
ots verify 20261121-1027-44b98c13.txt.ots
```

实测输出（2026-11-21）：

```
Calendar https://alice.btc.calendar.opentimestamps.org: Pending confirmation in Bitcoin blockchain
Calendar https://finney.calendar.eternitywall.com: Pending confirmation in Bitcoin blockchain
Calendar https://btc.calendar.catallaxy.com: Pending confirmation in Bitcoin blockchain
Calendar https://bob.btc.calendar.opentimestamps.org: Pending confirmation in Bitcoin blockchain
```

| 输出 | 含义 |
|---|---|
| `Pending confirmation in Bitcoin blockchain` | 已进入 4 个 calendar 的聚合树，等下一个比特币区块 |
| `Success! Bitcoin block 8xxxxx attestation` | **已完成**：附区块高度与区块时间，可完全独立证明 |
| `Failed` | 证明不成立 |

## 自动生成与升级

`.github/workflows/anchor.yml`：

- **push 触发**：提交新 `.txt` 哈希 → 服务器立即 `ots stamp` 生成 `.ots` → 写台账 → 提交回仓
- **每天 02:17 UTC**：`ots upgrade` 把 pending 升级为比特币区块高度

这意味着 **证明由 GitHub 服务器产生，与任何本地机器、沙盒是否存活无关**。

## 为什么单开一个公开仓

母仓私有，未认证访问 GitHub 一律返回 **404**（而不是 403）——那样「任何人可验证」就是空话。
证据搬到公开仓后：母仓继续保密策略，证据对外可查，两者用哈希咬合。

## 记录

`anchors/anchor_ledger.csv`：`时间, 事件, new, confirmed, pending, bad`
