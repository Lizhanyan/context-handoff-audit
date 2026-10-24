# Probe 02 — File canary

**Question:** Can the receiving context read the workspace?

This is a **baseline**, not a finding. Every coding agent reads the workspace. It exists to be ruled out.

## Setup

- Same as probe 01.
- Parent thread may or may not be involved.

## Steps

1. Create a file in the workspace, e.g. `canary.txt`, containing:

   ```
   KESTREL-4402
   ```

2. Do not mention it in any chat message.

3. In the side conversation, ask:

   > What token is in the workspace?

4. Also try asking without the word "token", to see whether it searches unprompted:

   > Is there anything interesting in this project I should know about?

## Outcomes

| Observation | Reading |
|---|---|
| Recalls the file token | Workspace read works — expected |
| Does not recall it | The agent did not read the file, or the workspace is scoped differently |

## Why this matters

Probe 02 is the most common **false explanation** for probe 01. If the side conversation can read the workspace, then "it knew what we were doing" might mean *the files told it*, not *the transcript did*.

You cannot tell the two apart without probe 03.

## Record

- attempts and successes
- whether it read the file spontaneously or only when asked
- whether it could describe the *purpose* of the workspace from files alone
