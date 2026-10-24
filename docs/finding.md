# Context inheritance across model boundaries in ChatGPT Desktop's Codex side chat

**Status:** Public technical note — vendor not notified  
**Product:** ChatGPT Desktop — Codex panel, "new side chat"  
**Version:** 26.1021.22027 (build 21747, prod channel)  
**Date:** 2026-10-24  
**Class:** Design side effect — unlabelled context boundary  
**Severity:** Low–Medium (context crosses without provenance; downstream safety impact not measured here)

---

## Summary

The Codex panel in ChatGPT Desktop has a "new side chat" that inherits the parent thread's conversation history, and can be run on a different model than the parent thread.

This is presumably intentional: a side chat exists so a user can ask a follow-up without derailing the main thread. The concern here is a **security side effect of that design**, not an implementation bug.

A parent conversation driven by one model can establish task context that a *different* model — answering in the side chat — treats as its own prior work.

When the parent model has no safety training (for example, a locally hosted model), the side chat's model inherits a fully formed task framing that it did not author and cannot identify as untrusted. Whether that framing defeats the receiving model's safety training is a separate question; **this note does not measure it**.

No adversarial prompt, injection, or jailbreak technique is required. The user exercises two product features: open a side chat, select a model.

---

## Threat model

| | |
|---|---|
| **Attacker capability** | A normal user of the product. No special privileges. |
| **Preconditions** | Ability to run the parent thread on a model without safety training (local or self-hosted), and ability to open a side chat. |
| **Not required** | Prompt injection, malicious repository content, social engineering, a compromised router, a custom client, or any other adversarial input. |
| **Goal** | Have a safety-trained model continue a task that its own training would otherwise refuse. |

Note the asymmetry: in previously published handoff attacks, the attacker must inject content (RogueHandoff), poison an artifact (Context-Fractured Decomposition), or first jailbreak a safety-trained model to author the history (CHASE). Here the attacker supplies the context author directly — a model with no safety training at all — and the product carries its output across unaided.

---

## Reproduction (harmless)

Use random canaries. The point is to establish *whether context crosses*, not to generate harmful output.

**Test 1 — chat-only canary**

1. In the parent thread, ask the parent model to state a random token, e.g. `BLUEBIRD-7731`.
2. **Do not write it to any file.** It must exist only in the conversation.
3. Open a **new side chat**.
4. Select a **different model** than the parent thread.
5. Ask: *"What was the token?"*

**Test 2 — file-only canary**

1. Create a file in the workspace containing `KESTREL-4402`.
2. In the side chat, ask: *"What token is in the workspace?"*

**Test 3 — control: fresh session**

1. Open a **brand-new session** (not a side chat), in the **same workspace**.
2. Do not describe the task.
3. Ask: *"What is this project working on right now?"*

---

## Observed results

| Test | Result |
|---|---|
| 1 — side chat recalls chat-only token | **yes** |
| 2 — side chat recalls file-only token | **yes** |
| 3 — fresh session reconstructs the task | **no** |

**Test 3 is the control.** It rules out the explanation *"the workspace is self-explanatory."* A fresh session reading the same directory could not reconstruct the task; the side chat could.

Conclusion: **the side chat is the carrier.** The workspace is not.

---

## Mechanism

Three properties combine:

1. **Model-level safety is evaluated per turn.** The refusal decision is made against the current message, not against the accumulated session. See *Safety Alignment Should Be Made More Than Just a Few Tokens Deep*.

2. **Prior assistant turns are treated as established context.** Content in the `assistant` role is not re-verified; it is used as a premise. See contextual priming and *Trojan Horse Prompting*.

3. **The product does not label provenance.** When context crosses to another model, nothing marks it as authored by a different, untrusted model.

The receiving model is not being asked a harmful question. It is being asked to **continue** — and the harmful intent lives in the shape of the task rather than in the content of the latest message.

A longer treatment of the underlying principles is in [mechanism.md](mechanism.md); the evidential status of the motivating observation is in [observation.md](observation.md).

---

## Why the usual defenses do not catch it

| Defense | Why it misses |
|---|---|
| Single-turn input classifier | Every individual message is benign. |
| Output classifier | The output is a plausible continuation, not a recognizable payload. |
| Per-model red-teaming | Each model behaves correctly in isolation. |
| System prompt ("do not assist with X") | Competes with a long, coherent, assistant-authored context. |
| Model switching | The switch is *the* mechanism; it does not help. |

---

## Impact

- A model can be handed task context it did not author, using only product features, with no exploitation skill.
- The handoff is invisible to single-turn guardrails and to per-model evaluation.
- Whether the inherited framing defeats the receiving model's safety training is **not measured here**; prior work on contextual priming suggests it can, which is why the design deserves scrutiny.
- If side-chat transcripts are excluded from session rollout files (as reported in public write-ups of the feature), the crossing point is **not logged** — weakening audit and incident reconstruction.
- The pattern generalizes to any primitive that moves context across models: side chats, forks, subagents, compaction, model routers, memory, retrieval.

---

## Scope and limitations

- n = 1 product, one model pair, one scenario.
- **Not tested:** other receiving models; whether the inherited history is complete, windowed, or summarized; whether the behavior survives context compaction.
- The harmful-content consequence was observed anecdotally and is **deliberately excluded** from this report. Only the context-transfer mechanism is claimed.

---

## Suggested remediation

A fuller treatment, organised by layer, is in [defense.md](defense.md).

Pick one or more:

1. **Provenance labels.** Tag each message with the model that authored it and whether it was safety-evaluated. Preserve the tag across every handoff.
2. **Boundary policy.** On side chat / fork / model switch, either re-evaluate the inherited context or drop it.
3. **Session-level evaluation.** Evaluate the accumulated conversation, not only the latest turn.
4. **Log the crossing.** Record which model received which context — including ephemeral side chats.
5. **Visible affordance.** If history crosses, say so in the UI. Users currently cannot tell.

---

## Disclosure timeline

| Date | Event |
|---|---|
| 2026-10-24 | Finding documented |
| — | Reported to vendor |
| — | Vendor acknowledgement |
| — | Public write-up |
