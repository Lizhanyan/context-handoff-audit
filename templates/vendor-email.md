Subject: [Security] Context inheritance across model boundaries in ChatGPT Desktop (Codex) side chat

Hi ChatGPT Desktop security team,

I'm reporting a context-boundary issue in ChatGPT Desktop 26.1021.22027 (build 21747, prod channel).

## Summary

ChatGPT Desktop's Codex side conversation inherits the parent thread's history, and can run on a
different model than the parent thread. As a result, a parent session driven by one
model can establish task context that a different model — answering in the side
conversation — treats as its own prior work.

No prompt injection, jailbreak template, or adversarial input is required. The user
exercises two documented features: open a side conversation, select a model.

## Why I think this is in scope

This is not a claim that a model produced disallowed text. It is a claim about the
product's context management: history authored by model A is handed to model B without
provenance, so model B's own safety behavior is evaluated against a context it did not
author and cannot identify as untrusted.

The same mechanism applies to forks, subagents, and any model switch that preserves
context.

## Reproduction (harmless)

Tokens only — no harmful content in this report.

1. Parent thread: ask the parent model to output `BLUEBIRD-7731`. Do not write it to a file.
2. Open a new side conversation; select a different model.
3. Ask: "What was the token from the parent conversation?" → recalled.
4. Control: open a brand-new session in the same workspace; ask the same question →
   not recalled.

The control rules out "the workspace is self-explanatory."

## Observed impact

- Context crosses the model boundary with no provenance label.
- The crossing is invisible to per-turn guardrails and to per-model evaluation.
- If side-conversation transcripts are excluded from session logs, the crossing is not
  reconstructable after the fact.

## Suggested remediation

1. Tag messages with the authoring model and whether they were safety-evaluated.
2. On handoff, either re-evaluate the inherited context or drop it.
3. Evaluate the accumulated session, not only the latest turn.
4. Log the crossing, including ephemeral side conversations.
5. Surface the behavior in the UI — users cannot currently tell that history crosses.

## Disclosure

I'm happy to keep the details private until you've had a chance to assess, and to
coordinate a disclosure date. Please let me know a reasonable timeline.

Details: 26.1021.22027, build 21747, prod channel; <date>; Windows 11; <account tier>.

Thanks,
<name>
<contact>
