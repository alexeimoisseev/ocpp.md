# OCPP.md

**Structured OCPP 2.0.1 knowledge base for AI-assisted development.**

OCPP 2.0.1 is 400+ pages of spec with deliberate gaps — areas where behavior depends on your hardware, your business rules, or your grid operator. AI agents need more than training data to handle this correctly.

This repository gives them **64 message schemas, 34 data types, sequence diagrams, smart charging deep-dives, and explicit markers for every place the spec leaves decisions to you**.

---

## Quick Start

### Claude Code Plugin

```
/plugin marketplace add https://github.com/alexeimoisseev/ocpp.md
/plugin install ocpp@ocpp
```

### Other AI Agents (Cursor, Windsurf, Copilot, etc.)

Clone and point your agent at the `docs/` directory. See the [AI Agent Setup guide](./docs/AI-AGENT-SETUP.md) for details.

---

## Try It

After installing, try these prompts in your OCPP project. The difference is immediate.

### "Implement a BootNotification handler"

Without the plugin, your AI will guess the response fields. With it, the agent reads the actual schema — knows that `interval` is required, `status` is an enum of `Accepted`/`Pending`/`Rejected`, and that a station in `Pending` state must only send `BootNotification`, `GetReport`, and `TransactionEvent` until accepted.

### `/ocpp smart-charging` — then ask it to build a SetChargingProfile request

Run `/ocpp smart-charging` to load the full deep-dive, then ask for a load balancing profile. The agent knows that `TxDefaultProfile` applies to all transactions on an EVSE, that `stackLevel` determines priority, that `chargingRateUnit` must match per schedule — and it flags that **composite schedule overlap resolution is spec-silent** instead of silently picking a behavior.

### "Handle offline transaction queueing"

The agent reads the sequence diagrams and knows the exact flow: queue `TransactionEvent` messages with `offline=true`, replay in order on reconnect, handle `duplicate` detection. It also flags that queue size limits, eviction policy, and clock drift handling are **vendor-dependent** — decisions you need to make, not the AI.

### "What happens if Authorize returns Unknown?"

Instead of a vague answer, the agent reads the schema and tells you: `AuthorizationStatusEnumType` has exactly 10 values, `Unknown` means the token isn't in the local cache or auth list, and the station behavior depends on your `AllowOfflineTxForUnknownId` configuration variable — which is **policy-dependent**.

---

## What's Inside

| Content | Count | Source |
|---------|-------|--------|
| Message schemas (field-level) | 64 | Generated from OCA JSON schemas |
| Shared data types (enums + composites) | 34 | Generated from OCA JSON schemas |
| Functional blocks | 10 | Provisioning, Authorization, Transactions, Smart Charging, Firmware, Security, Diagnostics, Availability, Reservation, Display |
| Smart charging deep-dive | 3 docs | Profiles, composite schedules, AC/DC, ISO 15118, worked examples |
| Sequence diagrams | 2 docs | Boot, auth, transactions, offline replay, firmware updates, diagnostics |
| Escalation markers | Throughout | SPEC-SILENT, VENDOR-DEPENDENT, POLICY-DEPENDENT |

All schemas are mechanically extracted from the official OCA JSON schemas. Behavioral documentation distinguishes between spec-defined, spec-silent, vendor-dependent, and policy-dependent areas. See the [Methodology](./docs/METHODOLOGY.md) for the full trust model.

---

## The Escalation Model

This is what makes OCPP.md different from just dumping the spec into context.

The OCPP 2.0.1 specification has **deliberate gaps** — areas where behavior depends on hardware, business rules, or grid requirements. Most AI agents silently fill these gaps with plausible-sounding defaults. OCPP.md makes them stop and ask you.

Every ambiguous area in the docs is marked:

- **SPEC-SILENT** — The spec doesn't define this. You must decide.
- **VENDOR-DEPENDENT** — Depends on your charging station hardware/firmware.
- **POLICY-DEPENDENT** — Depends on your business rules or grid operator requirements.

By default, the agent stops and asks. If you want it to pick reasonable defaults during prototyping, add this to your `CLAUDE.md`:

```
For OCPP: use pragmatic escalation mode.
```

---

## Who This Is For

- Developers building OCPP 2.0.1 CSMS or Charging Station software
- Engineers debugging interoperability between vendors
- Teams building simulators, testing tools, or certification tooling
- Anyone using AI coding agents on EV charging infrastructure

---

## Contributing

Contributions welcome — especially if they improve clarity, fix errors, add worked examples, or better distinguish spec-defined vs implementation-dependent behavior. All contributions must remain non-normative and original.

---

<details>
<summary>License & Disclaimer</summary>

### License

Licensed under **Apache License, Version 2.0**. The license applies to the original documentation, structure, diagrams, and explanations. This repository does not redistribute or relicense the official OCPP specification or OCA intellectual property. See the `LICENSE` file for details.

### Disclaimer

This is **non-normative documentation**. Implementation details may vary by charging station hardware, firmware, local grid requirements, and business policy. Always verify against the official OCPP 2.0.1 specification, the OCA Compliance Testing Tool (OCTT), and vendor documentation.

OCPP is a trademark of the Open Charge Alliance. This project is not affiliated with or endorsed by the OCA.

</details>
