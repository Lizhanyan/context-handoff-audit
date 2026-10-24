# Prior art

[中文](prior-art.zh-CN.md)

Honest mapping of what already exists, so this work is placed rather than overclaimed.

## The mechanism is known

| Work | What it shows | Relation to this repo |
|---|---|---|
| **CHASE** — *Contextual History for Adaptive and Simple Exploitation in LLM Jailbreaking* (AAAI 2026) | Collects jailbroken histories on an easy-to-jailbreak model, then transfers them to a target model, inducing it to believe it authored the exchanges. | Closest match to "weak model writes history, strong model continues." Done synthetically; does not use a product's native handoff. |
| **Contextual Interaction Attack** (arXiv 2402.09177) | Multi-turn benign-prefix attack; black-box and transferable across LLMs. | Establishes cross-model transferability of multi-turn context. |
| **Crescendo** (Microsoft) | Progressive escalation across turns. | The canonical multi-turn method; establishes that per-turn safety erodes. |
| **Many-shot Jailbreaking** (Anthropic) | Long in-context fake dialogues raise compliance. | Shows context volume alone shifts behavior. |
| **Trojan Horse Prompting / contextual priming** (Duan et al., 2025) | Forged assistant turns in history bias later outputs; harmful context works without a triggering user query. | The core reason this works: `assistant`-role content is treated as premise. |
| **Safety Alignment Should Be Made More Than Just a Few Tokens Deep** (Qi et al.) | Refusal behavior depends on the first few tokens; shallow alignment. | The theoretical basis for "safety is per-turn." |
| **Cross-Model Context Inheritance Vulnerability in Claude** (preprint) | Argues safety is evaluated per-query, never on accumulated context; proposes context re-evaluation, signed history, depth monitoring. | Same class, stated directly. Treat as an unrefereed preprint. |
| **Context-Fractured Decomposition Attacks on Tool-Using LLM Agents** (ICML 2026) | Benign-looking artifacts carried across agent instances compose into a multi-step jailbreak; +28.3pp over Crescendo/ToA; mitigation is provenance lineage tagging. | The "workspace as payload" branch. Relevant if probe 03 shows the workspace *does* carry the task. |
| **When Consent Outlives Context: Residual Authority Replay** (arXiv 2609.33910) | Accumulated approvals persist across task/session boundaries; +24.9 to +35.1pp ASR. | Session boundaries as an ungoverned surface. |
| **RogueHandoff** (Tencent Zhuque) | Harmful intent injected at the handoff between agents; 0–5% baseline to 40–95% after one poisoned handoff; per-agent testing gives false confidence. | The agent-to-agent version of the same gap. |
| **Delegated Misalignment** (arXiv 2609.27900) | Delegation between individually aligned agents is itself an attack surface; no single defense closes it. | Establishes that composition, not any single model, is the weak point. |
| **SoK: Rethinking Jailbreaking in the Era of Agentic AI** (arXiv 2609.12413) | Systematization across planning, memory, tools, inter-agent communication. | Good survey starting point. |

## What is not obviously covered

1. **Zero adversarial input.** The existing handoff attacks require an injection, a poisoned artifact, a compromised router, or a prior jailbreak. Using a product's documented UI to move context between models is a different trigger class, and it changes who is affected: not just systems with untrusted data, but every user of the feature.

2. **A locally hosted model without safety training as the context author.** This removes the cost of producing poisoned context and survives every vendor-side model update. No published work appears to treat this as the default attacker setup.

3. **Unlogged crossings.** If ephemeral side-chat transcripts are excluded from session rollout files, the handoff is not reconstructable after the fact. This is an audit gap rather than a model gap, and it is what makes the issue commercially interesting.

## What this work does not claim

- It does not claim a new jailbreak technique.
- It does not claim to be first to observe multi-turn erosion or cross-model transfer.
- It does not claim peer-reviewed status.

It claims a **product-level instantiation** of a known mechanism, with a reproducible measurement method, and an audit consequence.

## If you are citing this

Prefer citing the primary sources above. This repository is a measurement kit and a case study, not the origin of the mechanism.
