# kb-anchors · 公开心跳证据（比特币时间戳）

本仓只存放**证据**，不含任何策略内容。作用是让任何人**无需账号、无需信任**地独立验证：
「某个哈希确实在某个比特币区块之前就已经存在」。

## 这是什么

`anchors/` 里每个锚点：

| 文件 | 内容 |
|---|---|
| `*.txt` | 一行：`<完整 sha256>  MANIFEST.sha256` —— 当轮归档清单的哈希 |
| `*.ots.b64` | OpenTimestamps 证明的 base64（已提交 4 个互不隶属的 calendar，锚定比特币） |

母仓保持私有，但**哈希可公开验证**——验证只关心"这串字节在何时已存在"，不看内容。

## 如何独立验证

```bash
pip install opentimestamps-client
git clone https://github.com/ouweiquan/kb-anchors && cd kb-anchors/anchors
base64 -d 20261121-1027-44b98c13.ots.b64 > prove.ots
ots verify prove.ots
```

| 输出 | 含义 |
|---|---|
| `Pending confirmation in Bitcoin blockchain` | 已进入 calendar 聚合树，等下一个比特币区块 |
| `Success! Bitcoin block 8xxxxx attestation` | **已完成**：附区块高度与区块时间，可完全独立证明 |
| `Failed` | 证明不成立 |

（`ots verify` 会自动按同目录下的 `.txt` 找目标文件；若提示找不到，用 `ots verify -d <hash> prove.ots`。）

## 自动升级

`.github/workflows/anchor.yml` 每天 02:17 UTC 在 **GitHub 服务器**上：解码 `.b64` → `ots upgrade` → 提交回本仓。**与本地沙盒是否存活无关。**

## 为什么单开一个公开仓

母仓私有，未认证访问 GitHub 一律 404——那样"任何人可验证"就是空话。证据搬到公开仓后：母仓继续保密策略，证据对外可查，两者用哈希咬合。
