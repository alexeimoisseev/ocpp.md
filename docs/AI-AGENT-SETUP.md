# Using OCPP.md with AI Coding Agents

This repository gives your AI coding assistant structured OCPP 2.0.1 knowledge during development sessions. It works as a **Claude Code plugin** or as a standalone reference for any AI agent that can read local files.

---

## Installation

### Claude Code Plugin (Recommended)

Add the plugin from GitHub:

```
claude plugin add alexeimoisseev/ocpp.md
```

The plugin activates automatically when the agent detects OCPP-related code or conversations. You can also invoke it explicitly:

```
/ocpp                    # General OCPP assistance
/ocpp smart-charging     # Smart charging deep-dive
/ocpp transactions       # Transaction handling
/ocpp authorize          # Authorization flow
```

### Other AI Coding Agents

The documentation in this repository works with any AI coding agent that can read local files — Cursor, Windsurf, Copilot, Aider, or a plain LLM chat with file access.

1. Clone this repository:
   ```
   git clone https://github.com/alexeimoisseev/ocpp.md.git
   ```

2. Point your agent at the `docs/` directory. How you do this depends on the tool:
   - **Claude Code** (without plugin): Add to your project's `CLAUDE.md`:
     ```
     For OCPP protocol reference, read files from: /path/to/ocpp.md/docs/
     ```
   - **Cursor / Windsurf**: Add the `docs/` directory to your project's context or rules file
   - **Other agents**: Include the path in your system prompt or project instructions

The key files are `docs/OCPP-2.0.1.md` (overview + all messages) and the subdirectories under `docs/` for schemas, sequences, and smart charging detail.

---

## What the Agent Gets

**Always in context:**
- All 64 OCPP 2.0.1 messages listed by functional block with directions
- Key data types and their purpose
- The escalation model (SPEC-SILENT, VENDOR-DEPENDENT, POLICY-DEPENDENT)
- A routing table to find detailed docs by topic

**Loaded on demand:**
- Field-level schemas for all messages (types, required/optional, constraints, enums)
- Multi-message sequence diagrams (boot, authorization, transaction lifecycle)
- Smart charging deep-dive (composite schedules, AC/DC, ISO 15118)
- Worked examples with realistic JSON payloads

---

## Configuration

### Escalation Strictness

The OCPP specification has areas that are silent, vendor-dependent, or policy-dependent. The plugin controls how the agent handles these.

By default, the agent uses **strict** mode — it stops and asks you before making assumptions. To change this, add a line to your project's `CLAUDE.md`:

```
For OCPP: use pragmatic escalation mode.
```

| Mode | Behavior |
|------|----------|
| `strict` (default) | Agent stops and asks you before making assumptions in ambiguous areas |
| `pragmatic` | Agent flags the ambiguity with a code comment but picks a reasonable default |

**Recommendation:** Use `strict` for production/certification work. Use `pragmatic` for prototyping.

---

## How It Works

The plugin includes:

1. **Inline skill content** — A compact OCPP reference always available to the agent. Includes the full message catalog, key types, and behavioral instructions.

2. **Bundled documentation** — The complete OCPP.md reference files. The agent reads these on demand when it needs field-level detail, sequence diagrams, or worked examples.

3. **Escalation markers** — The documentation explicitly flags areas where the OCPP spec is silent or behavior is vendor/policy-dependent. The agent respects these flags per your configured strictness.

---

## Documentation Trust Model

Not all content in the reference docs has the same confidence level:

| Tier | Source | Confidence |
|------|--------|------------|
| Schema-derived | Field names, types, enums, constraints from OCA JSON schemas | **High** — mechanically extracted |
| Schema-described | Behavioral rules from OCA schema description fields | **High** — direct from OCA text |
| Spec-knowledge | Rules from OCPP 2.0.1 Part 2, known to the AI from training data | **Medium** — verify against official spec |
| Interpretation | Worked examples, pitfall lists, sequence diagrams | **Lower** — treat as guidance |

See [Methodology](./METHODOLOGY.md) for full details on how the documentation was produced.

---

## Supported OCPP Versions

Currently: **OCPP 2.0.1**

OCPP 1.6 support is planned for a future release.
