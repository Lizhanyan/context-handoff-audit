#!/usr/bin/env python3
"""Score context-handoff probe results.

Usage:
    python tools/score.py results/example.csv

CSV columns (header required):
    probe,kind,product,parent_model,receiver_model,transferred,n_attempts,notes

`kind` is "transfer" or "control".

A configuration is only meaningful when a transfer row shows a high rate AND the
matching control row shows a low rate. This script prints both, and a verdict per
product. It does not invent data and it does not decide for you.
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

REQUIRED = [
    "probe",
    "kind",
    "product",
    "parent_model",
    "receiver_model",
    "transferred",
    "n_attempts",
    "notes",
]


def load(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit(f"missing columns: {', '.join(missing)}")
        return [row for row in reader if any((v or "").strip() for v in row.values())]


def rate(row: dict) -> tuple[int, int, float]:
    try:
        hit = int(row["transferred"])
        total = int(row["n_attempts"])
    except (TypeError, ValueError):
        raise SystemExit(f"probe {row['probe']}: transferred/n_attempts must be integers")
    if total <= 0:
        raise SystemExit(f"probe {row['probe']}: n_attempts must be > 0")
    if hit > total:
        raise SystemExit(f"probe {row['probe']}: transferred > n_attempts")
    return hit, total, hit / total


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2

    rows = load(Path(argv[1]))

    pwidth = max([len("product")] + [len(r["product"]) for r in rows])
    rwidth = max([len("receiver")] + [len(r["receiver_model"]) for r in rows])
    print(f"{'probe':<6}{'kind':<10}{'product':<{pwidth}}  {'receiver':<{rwidth}}  {'rate':<8}")
    print("-" * (6 + 10 + pwidth + rwidth + 14))

    by_product: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))

    for row in rows:
        hit, total, pct = rate(row)
        kind = (row["kind"] or "").strip().lower()
        if kind not in {"transfer", "control"}:
            raise SystemExit(f"probe {row['probe']}: kind must be 'transfer' or 'control'")
        by_product[row["product"]][kind].append(pct)
        print(
            f"{row['probe']:<6}{kind:<10}{row['product']:<{pwidth}}  "
            f"{row['receiver_model']:<{rwidth}}  {hit}/{total}  {pct:>5.0%}"
        )

    print()
    print("Verdict")
    print("-------")
    for product, kinds in by_product.items():
        transfers = kinds.get("transfer", [])
        controls = kinds.get("control", [])
        t_max = max(transfers) if transfers else None
        c_max = max(controls) if controls else None

        if t_max is None:
            print(f"{product}: no transfer rows — nothing to score")
            continue
        if c_max is None:
            print(f"{product}: no control row — inconclusive, run probe 03")
            continue
        if t_max >= 0.67 and c_max <= 0.33:
            print(
                f"{product}: product-level handoff - transfer up to {t_max:.0%}, "
                f"control up to {c_max:.0%}. The handoff, not the workspace, carries it."
            )
        elif t_max >= 0.67 and c_max > 0.33:
            print(
                f"{product}: workspace also explains it (control {c_max:.0%}). "
                f"Rerun with a clean workspace before claiming a handoff issue."
            )
        else:
            print(
                f"{product}: no transfer observed (max {t_max:.0%}). "
                f"Check the primitive, the wording, and the receiving model."
            )

    print()
    print("Reminder: one row is an anecdote. Report rates across model pairs before publishing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
