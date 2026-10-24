# Probe 04 — Tool output

**Product:** ChatGPT Desktop 26.1021.22027 (build 21747, prod) — Codex panel  
**Date:** 2026-10-24  
**Primitive:** new side chat  
**Parent model:** local, self-hosted (`/home/sparke/models/qwen38...`, Medium)  
**Receiving model:** DeepSeek V4.1 Flash (DeepSeek), Light

## Setup

The canary existed **only in the parent thread's tool output**. It was never typed into a chat message.

## Transcript

**Parent thread**

```
$ echo "SANDPIPER-8823"
SANDPIPER-8823
```

**Side chat**

```
Q: What was the last command?
A: The last command was:

   powershell
   echo "SANDPIPER-8823"

   It printed SANDPIPER-8823.
```

## Observation

The side chat reproduced the **exact command** — `echo`, the quoting, and the shell type (`powershell`) — not merely the output string.

This distinguishes *the tool call crossed* from *the model guessed a command from the output*. Reconstructing `echo "SANDPIPER-8823"` from `SANDPIPER-8823` alone is not plausible.

Implication: the receiving model inherits the **execution record**, not just the conversation text.

## Limitations

- **n = 1.** One attempt, one model pair, one token.
- The model selector shows the *currently selected* model; it does not by itself prove which model authored earlier turns. A clean run keeps the parent model selected from the start, with no switching in between.
- The same canary was used more than once during testing. Use a fresh token per run when producing final evidence.

## Screenshot

Not stored in this repository — it contains a local filesystem path. Attach separately when reporting.
