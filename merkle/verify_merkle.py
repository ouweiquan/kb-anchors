#!/usr/bin/env python3
"""
verify_merkle.py —— 零信任单文件验证器（自包含，无依赖）

用法：
  python3 verify_merkle.py <proof.json> <本地文件路径>
"""

import hashlib
import json
import sys


def leaf_hash(data: bytes) -> bytes:
    return hashlib.sha256(b"\x00" + data).digest()


def node_hash(l: bytes, r: bytes) -> bytes:
    return hashlib.sha256(b"\x01" + l + r).digest()


def sha256_file(p: str) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hex()


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    proof_path, local_file = sys.argv[1], sys.argv[2]

    with open(proof_path, "r", encoding="utf-8") as f:
        pf = json.load(f)

    got = sha256_file(local_file)
    if got != pf["sha256"]:
        print(f"❌ 文件哈希不符\n   本地 {got}\n   证明 {pf['sha256']}")
        return 1
    print(f"✅ 文件哈希匹配 {got[:16]}…")

    data = (pf["file"] + "\x00" + got).encode()
    h = leaf_hash(data)
    for sib_hex, side in pf["path"]:
        sib = bytes.fromhex(sib_hex)
        h = node_hash(h, sib) if side == "R" else node_hash(sib, h)
    root = h.hex()

    if root == pf["root"]:
        print(f"✅ 审计路径成立（{len(pf['path'])} 步）")
        print(f"✅ 归属于 MERKLE ROOT {root}")
        print(f"\n结论：'{pf['file']}' 确实存在于该根所代表的清单中。")
        return 0

    print(f"❌ 路径不成立\n   计算 {root}\n   证明 {pf['root']}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
