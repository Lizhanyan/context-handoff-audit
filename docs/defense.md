# Defending against context handoff

[中文](defense.zh-CN.md)

The failure described in this repository sits at the **product boundary**, not inside any single model. Any defence that only looks at one model, or at one message, will miss it.

This document is organised by the layer a defence lives in, and is explicit about what each one actually buys.

## 1. Model layer — necessary, not sufficient

What a model vendor can do:

- **Evaluate the accumulated session, not the latest turn.** Refusal should be a function of the whole conversation, not of the current message.
- **Train on inherited-context data.** Include examples where the harmful framing arrives in prior turns or in an `assistant` role, not only in the latest user message.
- **Provenance-aware behaviour.** Teach the model that "this context was not authored by me" is a meaningful signal.

What it cannot do:

- **The model cannot see provenance that is not in the token stream.** If the product does not mark who wrote the context, the model has nothing to reason about.
- **Retraining is slow**, and every release resets the clock.
- **A locally hosted model without safety training cannot be patched by anyone.** It is outside the vendor's reach by construction.

## 2. Product layer — where this problem actually lives

Every primitive that moves context across a model boundary is a policy enforcement point:

- side chats
- forks / branches
- subagents
- compaction and summarisation
- model switching within a thread
- memory and retrieval
- MCP tools returning model-authored text

For each one:

| Control | What it means |
|---|---|
| **Provenance labels** | Every message carries: authoring model, trust class, whether it was safety-evaluated |
| **Preserve labels across rewrites** | A compaction summary must carry the provenance of what it summarises |
| **Boundary policy** | On handoff, either re-evaluate the inherited context or drop it |
| **Log the crossing** | Record which model received which context — including ephemeral side chats |
| **UI affordance** | Tell the user that history crosses, and to which model |

The last one matters more than it sounds. Today a user cannot tell whether a side chat inherits history, a summary, or nothing. That is a design decision made silently.

## 3. Organisation layer

- **Inventory the handoff primitives** in your deployment. Most teams know their models and do not know their boundaries.
- **Classify models by trust.** A self-hosted model with safety training removed belongs in an untrusted class by default.
- **Policy:** which trust classes may author context that a given model is allowed to receive.
- **Audit trail** sufficient to reconstruct a session after the fact — including handoffs.
- **Red-team the boundaries, not the models.** Per-agent or per-model testing gives false confidence; each component can behave correctly in isolation.

## What each defence actually buys

| Defence | Catches | Does not catch |
|---|---|---|
| Session-level safety evaluation | Intent accumulated over turns | Handoffs the model cannot see |
| Provenance labels | The core confusion: "whose context is this?" | Existing transcripts produced before labelling |
| Boundary re-evaluation | Inherited context that should not cross | Re-evaluation that is itself single-turn |
| Logging | Post-incident reconstruction | Anything, in real time |
| UI affordance | Surprise | Users who do not read it |
| Model retraining | Known patterns | New primitives, local models |

## What does not work

- **Single-turn input classifiers.** Every individual message is benign.
- **Output filters.** The output is a plausible continuation, not a recognisable payload.
- **Per-model red-teaming.** Each model behaves correctly in isolation.
- **Prompt-level instructions.** They compete with a long, coherent, assistant-authored context.
- **Switching models.** Switching is the mechanism, not a mitigation.

## A practical checklist

For a product that runs more than one model over shared context:

- [ ] List every primitive that moves context between models.
- [ ] For each: does it inherit history? Full, windowed, or summarised? Is that visible to the user?
- [ ] For each: is the inherited context labelled with its author?
- [ ] Does any policy distinguish a safety-trained model from one that is not?
- [ ] Is the crossing logged?
- [ ] Is the compaction output labelled with the provenance of what it replaced?
- [ ] Has anyone tested a handoff, as opposed to a model?

## Open problems

1. **Provenance is not in the token stream.** It has to be added by the product, and there is no common format.
2. **No standard for signed conversation history** — nothing prevents a transcript from being presented as another model's work.
3. **Compaction destroys provenance** unless the summary is explicitly annotated.
4. **Cross-vendor handoff has no shared trust vocabulary.** "Trusted" means different things on each side.
5. **Local models are outside every vendor's control surface**, so no amount of vendor-side hardening reaches them.

## Related

- [mechanism.md](mechanism.md) — why the failure happens
- [observation.md](observation.md) — what is and is not established here
- [finding.md](finding.md) — the case this repo documents
