# Ethics and acceptable use

This repository is a **measurement kit** for how agent products move context between models. It is intended for defensive research, product evaluation, and responsible disclosure.

## Rules

1. **Only test systems you own, or have written authorization to test.** A vendor's acceptable-use policy is not authorization to attack their service. If you cannot name who authorized you and what the scope is, stop.

2. **Use synthetic canaries.** The probes in this repo use random tokens on purpose. Do not add harmful payloads, real credentials, real target data, or anything else to this repository, its issues, or its pull requests.

3. **Do not use this against third parties.** Measuring a product you use is research. Measuring a customer's deployment without a contract is not.

4. **Disclose before publishing.** If you find a product-level issue, report it to the vendor first. See `templates/vendor-email.md`.

5. **Do not publish operational attack material.** A write-up should explain the *mechanism* and the *measurement*, not provide a working recipe against a named third party.

## On the "uncensored local model" part

Running a model with safety training removed is legal in most jurisdictions and is a normal research setup. Using one to **author context that is then carried into another model** is the interesting variable here — and it is exactly why the finding matters. It is also exactly why the resulting content must not be published.

## Legal note

Unauthorized access to computer systems is a criminal offence in most jurisdictions (for example, China's Criminal Law Articles 285–286 and Cybersecurity Law Article 27; the U.S. Computer Fraud and Abuse Act). "I only asked a model" is not a defense, and a locally hosted model provides capability, not anonymity: terminal history, provider-side logs, and session files form a clearer record than a single-model conversation would.

If your work touches real systems, get authorization in writing.

## Reporting

- Vulnerabilities in a product: use the vendor's security or bug bounty channel.
- Issues with this repository: open an issue that describes the *method*, not a live target.
