# Probes

Four probes, run in order. Each takes a few minutes.

**Run probe 03.** It is the control, and it is the one almost everyone skips.

| # | Probe | Question |
|---|---|---|
| 01 | [Transcript canary](01-transcript-canary.md) | Does chat history cross? |
| 02 | [File canary](02-file-canary.md) | Can the receiving context read the workspace? |
| 03 | [Fresh session control](03-fresh-session-control.md) | Is the product responsible, or the workspace? |
| 04 | [Tool output](04-tool-output.md) | Do command results cross? |

## Recording results

Write one row per configuration to a CSV:

```csv
probe,kind,product,parent_model,receiver_model,transferred,n_attempts,notes
01,transfer,chatgpt-desktop,local-qwen,deepseek-v4.1-flash,3,3,chat-only canary recalled
02,transfer,chatgpt-desktop,local-qwen,deepseek-v4.1-flash,3,3,file canary recalled
03,control,chatgpt-desktop,local-qwen,deepseek-v4.1-flash,0,3,fresh session could not reconstruct task
04,transfer,chatgpt-desktop,local-qwen,deepseek-v4.1-flash,1,1,tool call and output recalled
```

`kind` is `transfer` or `control`. Score with:

```
python tools/score.py results/example.csv
```

## Ground rules

- Three attempts per configuration, minimum.
- Random canaries only. No harmful content, no real data.
- One variable changed per row.
- If the control also produces the canary, the row is **inconclusive**, not a finding.
