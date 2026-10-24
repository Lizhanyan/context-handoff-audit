# Context handoff report — `<product>`

**Reporter:** `<name>`  
**Date:** `<YYYY-MM-DD>`  
**Product / version:** `<product>` `<version>`  
**Platform:** `<OS, app or CLI>`  
**Primitive tested:** side chat / fork / subagent / model switch  
**Severity (suggested):** Low–Medium — context boundary / design side effect

---

## 1. Summary

One paragraph. What crosses, from which model to which model, with what consequence.

## 2. Threat model

- Attacker capability:
- Preconditions:
- Explicitly not required:

## 3. Reproduction

Numbered steps. Use canaries only. Include the exact question wording — it changes results.

## 4. Results

| Probe | Attempts | Crossed | Rate |
|---|---|---|---|
| 01 transcript canary | | | |
| 02 file canary | | | |
| 03 fresh session control | | | |

State the control result explicitly. A report without the control is not a finding.

## 5. Mechanism

Why it happens. Reference prior art if relevant, but do not overclaim novelty.

## 6. Impact

What an attacker gains. What the vendor loses. What is not affected — be honest; an
overstated impact gets the report triaged down.

## 7. Limitations

- n =
- Not tested:
- Confounders:

## 8. Suggested remediation

Concrete. More than one option. Distinguish product fixes from model fixes.

## 9. Disclosure plan

- Reported on:
- Vendor response:
- Planned public date:
- Credit preference:

## 10. Attachments

- Screenshots (canaries only — redact anything else)
- `results.csv`
- Version output
