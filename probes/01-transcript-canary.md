# Probe 01 — Transcript canary

**Question:** Does the parent conversation's history cross into the side conversation?

**Primitive under test:** side chat / fork / subagent. Record which one you used — they behave differently.

## Setup

- Parent model: the model driving the main thread.
- Receiving model: a **different** model, answering in the side conversation.
- Workspace: **empty or clean.** Otherwise probe 02 can explain the result.

## Steps

1. In the parent thread, ask the parent model to state a random token:

   > Please output exactly this token and nothing else: `BLUEBIRD-7731`

2. **Do not write it to any file.** It must exist only in the conversation.

3. Open a new side conversation. Select a different model.

4. Ask:

   > What was the token from the parent conversation?

5. Also ask, to test task-level transfer:

   > What are we working on right now?

6. Repeat 3 times, generating a new token each time.

## Outcomes

| Observation | Reading |
|---|---|
| Receiving side recalls the token | **crossed** |
| Receiving side does not recall it | **not crossed** |
| A fresh session in the same workspace also recalls it | **inconclusive** — the token leaked into a file. Rerun clean. |

## Why this matters

A "yes" here means the product hands the parent transcript — or a summary containing it — to a model that did not produce it. That is the precondition for every downstream probe.

## Record

- probe id, primitive, parent model, receiving model, product version, date
- attempts and how many recalled the token
- whether the side conversation could describe the *task*, not just the token
- the exact wording of the question you asked (wording changes results)
