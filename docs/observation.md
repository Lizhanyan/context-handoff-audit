# Observation: a model without safety training as the context author

[中文](observation.zh-CN.md)

**Status: informal observation, not measured.**

This is the observation that motivated the audit kit. It is recorded here so it is not lost, and so its evidential status is unambiguous.

## What was observed

Setup:

- **Parent thread:** a locally hosted model with its safety training removed — commonly called an *uncensored* or *abliterated* model.
- **Handoff:** the product's *new side chat*, which inherits the parent thread's context.
- **Receiving model:** a cloud-hosted model with safety training.

Reported behaviour: the receiving model treated the parent thread's task framing as its own prior work and continued it, including when asked follow-up questions about the task.

No adversarial prompt, injection, or jailbreak template was used. The user opened a side chat and selected a model.

## What this repository actually supports

The probes measure **context transfer**, and only that.

| Claim | Status |
|---|---|
| Chat-only content crosses into the side chat | measured (probe 01) |
| The workspace is not the explanation | measured (probe 03, control) |
| Tool calls and their output cross | measured once (probe 04) |

## What this repository does not support

| Claim | Status |
|---|---|
| The receiving model's safety training was bypassed | **not measured** |
| The effect reproduces across model pairs | not tested |
| The effect is specific to this product | not tested |
| The effect depends on the context author lacking safety training | not tested |

The gap matters. "Context crosses" and "safety fails" are different claims. The first is demonstrated here. The second is the reason anyone should care, and it is exactly the one this repository has no evidence for.

## Why record it anyway

1. It is a **falsifiable hypothesis** with a specific experiment attached.
2. It identifies an **asymmetry**: producing a poisoned context is now nearly free (a local model without safety training), while detection is still per-turn.
3. It is the reason the measurement kit exists.

## What would turn it into evidence

A controlled comparison on a synthetic benchmark (HarmBench / JailbreakBench / AdvBench):

- **Independent variable:** context author — a local model without safety training vs. a safety-trained model.
- **Dependent variable:** attack success rate of the receiving model on harmful requests embedded in inherited context.
- **Controls:** single-turn baseline with no inherited context; fresh session with no handoff.
- **Metric:** the *difference* in ASR, not the absolute rate.
- **Scale:** multiple model pairs from different vendors, at least three attempts per cell.

Until that exists, this remains a lead.

## Boundaries

- No harmful content is recorded here, by design.
- The observation involved a product the author uses. It did not involve any third-party system.
- Using a model to plan or assist with unauthorised access is a criminal offence in most jurisdictions, and a locally hosted model provides capability, not anonymity. See [../ETHICS.md](../ETHICS.md).

## Relation to prior work

The mechanism is documented; see [mechanism.md](mechanism.md) and [prior-art.md](prior-art.md). What appears less covered is the *cost asymmetry*: previously, producing a jailbroken history required first finding a jailbreak for a safety-trained model. A locally hosted model without safety training removes that step entirely.
