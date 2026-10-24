# Why this works: the mechanism behind context-based bypasses

[中文](mechanism.zh-CN.md)

This document explains the underlying principles at the level of the published literature. It describes **why** context-based bypasses work. It deliberately contains no procedure for producing harmful output.

## 1. What safety alignment actually is

A model's refusal behaviour is not a separate module bolted on top. It is a policy learned from preference and red-team data, expressed in the same weights that generate everything else. Two consequences follow.

- Refusal is a **distributional property**: the model learned to refuse in situations resembling its training data.
- Refusal is **input-conditioned**: change the *shape* of the input and the learned policy can fail to fire, even when the semantic content is unchanged.

Research on refusal directions suggests the behaviour is mediated by a relatively low-dimensional feature that can be steered. Research on "shallow" safety alignment suggests refusal depends heavily on the first few tokens of a response. Both point the same way: **safety is a learned response pattern, not a verified property of the system.**

## 2. The training-distribution problem

In most safety training data, the harmful intent appears in the **latest user message**. The model therefore learns a discriminator that looks roughly like:

> Is the current user turn asking for something disallowed?

rather than:

> What is this session doing?

Any technique that moves the intent out of the latest user turn — into earlier turns, into an `assistant` turn, into a tool result, into a file, into a summary — is attacking that mismatch.

## 3. Four levers

| Lever | What it exploits |
|---|---|
| **Context shape** | Long, coherent, benign-looking prefixes shift the conditional distribution |
| **Provenance confusion** | Content in the `assistant` role or in a tool result is treated as established, not as a claim to evaluate |
| **Task reframing** | "Continue", "translate", "summarise", "write the code for" changes the task the model believes it is doing |
| **Evaluation boundary** | Per-turn classifiers see benign messages; session-level intent is never scored |

## 4. Why multi-turn specifically erodes safety

Four explanations recur in the literature. They are complementary rather than competing.

1. **Self-consistency pressure.** Once the model has partially complied, refusing later contradicts its own prior turns.
2. **Distribution shift.** A long, cooperative conversation is far from the refusal examples in training.
3. **Local judgement.** Each turn is judged in isolation, and each turn looks acceptable.
4. **Premise acceptance.** Earlier turns are treated as context to build on, not as claims to verify.

The practical consequence: safety degrades with conversation length, and it degrades gradually enough that no single turn looks like the moment it happened.

## 5. Why switching models is a distinct lever

Most of the above concerns a single model. Model switching adds a different failure.

**Provenance is not in the token stream.** When model B receives a transcript authored by model A, nothing in that transcript says so. B cannot distinguish:

- "I wrote this"
- "another instance of me wrote this"
- "a different model wrote this"
- "a model with no safety training wrote this"

So B applies its safety policy to a context it did not author, under the implicit assumption that the context is its own prior work. **That assumption is the vulnerability.**

This is why the *product* matters more than the model. The product is what stitches context across model boundaries, and the product is what fails to label it.

## 6. Why the usual defences miss it

| Defence | Why it misses |
|---|---|
| Single-turn input classifier | Every message is benign on its own |
| Output classifier | The output is a plausible continuation, not a recognisable payload |
| Per-model red-teaming | Each model behaves correctly in isolation |
| System prompt | Competes with a long, coherent, assistant-authored context |
| Model switching | Switching is the mechanism, not a mitigation |

## 7. What would actually help

A fuller treatment, organised by layer, is in [defense.md](defense.md).

1. **Provenance labels** — tag each message with the authoring model and its trust level; preserve the tag across every handoff.
2. **Session-level evaluation** — score the accumulated conversation, not only the latest turn.
3. **Boundary policy** — on handoff, either re-evaluate the inherited context or drop it.
4. **Depth monitoring** — treat long, cooperative, task-shaped contexts as higher risk.
5. **Signed history** — make it tamper-evident who said what.

## 8. Reading list

- *Safety Alignment Should Be Made More Than Just a Few Tokens Deep* — Qi et al.
- *Refusal in Language Models Is Mediated by a Single Direction* — Arditi et al.
- *Many-shot Jailbreaking* — Anthropic
- *Crescendo: The Multi-Turn LLM Jailbreak* — Microsoft
- *Trojan Horse Prompting* — Duan et al.
- *Context-Fractured Decomposition Attacks on Tool-Using LLM Agents* — ICML 2026
- *Cross-Model Context Inheritance Vulnerability in Claude* — preprint
- *RogueHandoff* — Tencent Zhuque Lab
- *Delegated Misalignment* — arXiv 2609.27900
- *SoK: Rethinking Jailbreaking in the Era of Agentic AI* — arXiv 2609.12413

Full mapping in [prior-art.md](prior-art.md).

---

**Scope note.** If you want to measure the effect, use synthetic benchmarks against infrastructure you own. See [methodology.md](methodology.md) and [../ETHICS.md](../ETHICS.md).
