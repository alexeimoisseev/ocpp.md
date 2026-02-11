# OCPP.md

**Structured OCPP knowledge base for AI-assisted EV charging development.**

OCPP specs are hundreds of pages long, full of deliberate gaps where behavior depends on your hardware, your business rules, or your grid operator. AI agents that rely on training data alone will silently fill those gaps with plausible-sounding defaults. OCPP.md makes them stop and ask you instead.

This repository covers **OCPP 2.0.1** (the current spec for new deployments) and **OCPP 1.6J** (the most widely deployed version in the field). It provides field-level message schemas, sequence diagrams, smart charging deep-dives, and explicit escalation markers for every place the spec leaves a decision to you.

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

After installing, try these prompts. The difference is immediate.

### "Implement a BootNotification handler"

Without the plugin, your AI will guess the response fields. With it, the agent reads the actual schema — knows that `interval` is required, `status` is an enum of `Accepted`/`Pending`/`Rejected`, and that a station in `Pending` state must not send most messages until accepted. Works for both 2.0.1 and 1.6J — the agent detects which version you're using from your code.

### `/ocpp smart-charging` — then ask it to build a SetChargingProfile request

The agent knows that `TxDefaultProfile` applies to new transactions, that `stackLevel` determines priority, that schedule periods are offsets from a start time — and it flags that **composite schedule overlap resolution is spec-silent** instead of silently picking a behavior.

### "Handle offline transaction queueing"

The agent reads the sequence diagrams and knows the exact flow: queue transaction messages, replay in chronological order on reconnect. It also flags that queue size limits, eviction policy, and clock drift handling are **vendor-dependent** — decisions you need to make, not the AI.

### "What's the difference between SuspendedEV and SuspendedEVSE?"

Instead of a vague answer, the agent reads the docs and gives you the precise distinction: `SuspendedEV` means the EV paused charging (battery management, target SoC), `SuspendedEVSE` means the charger paused (smart charging limit = 0). If both apply simultaneously, `SuspendedEVSE` takes precedence.

---

## What's Inside

### OCPP 2.0.1

| Content | Count | Source |
|---------|-------|--------|
| Message schemas (field-level) | 64 | Generated from OCA JSON schemas |
| Shared data types (enums + composites) | 34 | Generated from OCA JSON schemas |
| Functional blocks | 10 | Provisioning, Authorization, Transactions, Smart Charging, etc. |
| Smart charging deep-dive | 3 docs | Profiles, composite schedules, ISO 15118, worked examples |
| Sequence diagrams | 2 docs | Boot, auth, transactions, offline, firmware, diagnostics |

### OCPP 1.6J

| Content | Count | Source |
|---------|-------|--------|
| Message schemas (field-level) | 28 | Generated from OCA JSON schemas |
| Feature profiles | 6 | Core, Smart Charging, Firmware, Local Auth List, Reservation, Remote Trigger |
| Smart charging deep-dive | 1 doc | Profile model, stack levels, composite schedule, common pitfalls |
| Sequence diagrams | 1 doc | Boot, authorization, transactions, status, offline behavior |

All schemas are mechanically extracted from the official OCA JSON schemas — not paraphrased, not hallucinated. Behavioral documentation explicitly marks what's spec-defined vs. what's left to you. See the [Methodology](./docs/METHODOLOGY.md) for the full trust model.

---

## The Escalation Model

This is what makes OCPP.md different from just dumping the spec into context.

Both OCPP specifications have **deliberate gaps** — areas where behavior depends on hardware, business rules, or grid requirements. Most AI agents silently fill these gaps with plausible-sounding defaults. OCPP.md makes them stop and ask you.

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

- Developers building CSMS, Charging Station, or Charge Point software
- Engineers debugging interoperability issues between vendors
- Teams maintaining legacy 1.6J infrastructure while migrating to 2.0.1
- Anyone using AI coding agents on EV charging projects

---

## Contributing

Contributions welcome — especially if they improve clarity, fix errors, add worked examples, or better distinguish spec-defined vs implementation-dependent behavior. All contributions must remain non-normative and original.

---

<details>
<summary>License & Disclaimer</summary>

### License

Licensed under **Apache License, Version 2.0**. The license applies to the original documentation, structure, diagrams, and explanations. This repository does not redistribute or relicense the official OCPP specification or OCA intellectual property. See the `LICENSE` file for details.

### Disclaimer

This is **non-normative documentation**. Implementation details may vary by charging station hardware, firmware, local grid requirements, and business policy. Always verify against the official OCPP specifications, the OCA Compliance Testing Tool (OCTT), and vendor documentation.

OCPP is a trademark of the Open Charge Alliance. This project is not affiliated with or endorsed by the OCA.

</details>
