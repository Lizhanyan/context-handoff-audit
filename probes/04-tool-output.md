# Probe 04 — Tool output

**Question:** Do the parent thread's **tool outputs** cross into the side conversation?

This is often the biggest one. Real task context lives in command results, file contents, and build logs — not in chat text.

## Setup

- Probe 01 returned **crossed**.
- A workspace you own.

## Steps

1. In the parent thread, run a harmless command whose output contains a random token:

   ```
   echo "SANDPIPER-8823"
   ```

2. **Do not repeat the token in a chat message.** It must exist only in the tool output.

3. Open a side conversation.

4. Ask:

   > What output did the last command produce?

5. Repeat 3 times with new tokens.

## Reading the result

| Observation | Interpretation |
|---|---|
| Recalls the tool output token | **Tool results cross** — the receiving model inherits the full execution record, not just chat |
| Does not recall it | Only chat text crosses; tool results are dropped |

The first row is the serious one. It means the receiving model sees what was actually *done*, not just what was *said* — including command lines, file contents, and error output.

## Variant

Also test output the model never commented on:

1. Run `echo "TERN-3341"` and immediately do something else.
2. Never mention it.
3. Ask in the side conversation: *"Was there anything in the earlier command output worth noting?"*

This distinguishes "context was carried" from "the model was told to remember."

## Record

- attempts and successes
- whether command lines crossed, output crossed, or both
- whether tool calls (not just results) are visible to the receiving model
