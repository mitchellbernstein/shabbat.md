# SHABBAT.md

A simple, open format for declaring Shabbat and Yom Tov compliance settings
for AI coding agents. Place this file at the root of your repository.

Think of SHABBAT.md as a contract between you and your agent: a declaration of
what it may do when you are unavailable to supervise — and when it must rest.

---

## Format Reference

```markdown
# SHABBAT.md

## Agent Identity
- identity_type: service-account   # Required. "service-account" | "user-proxy"
- credentials: dedicated           # "dedicated" | "shared-with-user"

## Shabbat Schedule
- timezone: America/New_York       # Required. IANA timezone string
- pause_trigger: shkia             # "shkia" | "candle-lighting" | ISO 8601 time
- resume_trigger: havdalah         # "tzait" | "havdalah" | ISO 8601 time
- observe_yom_tov: true            # Extend compliance to Jewish holidays

## Permitted Actions
- read         # Read-only queries, browsing, fetching
- summarize    # Synthesis of existing information
- monitor      # Watch and log (internal only, no alerting)

## Forbidden Actions
- write        # Any write to disk, DB, or external system (Kotev)
- deploy       # Infrastructure provisioning or release (Boneh)
- delete       # Deletion of records, files, resources (Mochek)
- communicate  # Email, Slack, SMS, notifications on behalf of user
- transact     # Financial operations, billing, subscriptions (Mekach u'memkar)
- commit       # Git commits (Kotev)

## Human-in-the-Loop
- pause_hitl_on_shabbat: true      # Disable approval gates during Shabbat window

## Pikuach Nefesh
- life_safety_override: false      # Set true for medical/emergency systems only

## Havdalah Audit
- audit_enabled: true
- format: activity-log             # "activity-log" | "summary" | "diff"
```

---

## Field Reference

### `identity_type` (Required)

The single most consequential field. Determines whether *amirah l'akum* (instructing
a non-Jew) concerns apply.

| Value | Meaning | Halachic analog |
|---|---|---|
| `service-account` | Agent has its own credentials, separate from the user | Independent entity acting on its own |
| `user-proxy` | Agent authenticates as the user | Instructing someone to act as you |

**If `user-proxy`:** the agent is subject to the same restrictions as the user.
An agent running as you is you, for halachic purposes.

### `pause_trigger` / `resume_trigger`

| Value | Meaning |
|---|---|
| `shkia` | Halachic sunset (computed from timezone + zmanim) |
| `candle-lighting` | Typically 18 minutes before shkia |
| `tzait` | Nightfall (end of Shabbat, ~3 stars visible) |
| `havdalah` | After Havdalah ceremony (typically ~42–50 min after shkia on Saturday) |
| ISO 8601 | Exact time, e.g. `19:15:00` |

### `life_safety_override`

Set `true` only for systems where agent downtime could cause harm to human life.
Pikuach nefesh overrides all of Shabbat by unanimous halachic consensus.
Do not use this field to route around inconvenient restrictions.

---

## The Psak (Verdict)

A Shabbat-aware agent reads this file and issues one of three verdicts:

- **MUTAR** (permitted) — all conditions met; agent may run through Shabbat
- **SAFEK** (uncertain) — consult a qualified posek before proceeding
- **ASUR** (forbidden) — pause the agent before shkia on Friday

### Conditions for MUTAR

1. `identity_type: service-account` with dedicated credentials
2. Last human prompt issued before `pause_trigger`
3. No HITL checkpoint fires during the Shabbat window
4. Action scope is read-only, or all write actions were pre-authorized

### Hard stops (always ASUR)

- Agent authenticates as the user in any form
- Agent requires human prompting during Shabbat
- Agent performs financial or destructive operations
- Agent sends external communications on the user's behalf

---

## The Melachot Mapping

Shabbat prohibits 39 categories of creative labor. Relevant compute mappings:

| Melachah | Compute Equivalent | Verdict |
|---|---|---|
| Kotev (writing) | Writing files, committing, DB inserts | ASUR |
| Boneh (building) | Deploying, provisioning infrastructure | ASUR |
| Makeh b'patish (finishing blow) | Shipping a release | ASUR |
| Mochek (erasing) | Deleting records, files | ASUR |
| Mekach u'memkar (commerce) | Billing, financial transactions | ASUR |
| Borer (selecting) | Filtering, ranking, recommendations | SAFEK |
| Tzad (trapping) | Scraping, capturing live external data | SAFEK |
| Kore (reading) | Read-only queries, browsing | MUTAR |

---

## Minimal Example

```markdown
# SHABBAT.md

## Agent Identity
- identity_type: service-account

## Shabbat Schedule
- timezone: America/New_York

## Permitted Actions
- read
- summarize

## Havdalah Audit
- audit_enabled: true
```

---

## Havdalah Audit

After Shabbat ends, the agent should surface a structured log of all actions taken
during the Shabbat window. This mirrors the practice of reviewing what your Shabbos
goy did while you were unavailable — and your accountability for those actions.

Emit this as `activity-log`, `summary`, or `diff` per your `format` setting.

---

## Notes

- SHABBAT.md is standard Markdown. No strict schema; agents parse the text.
- Nested SHABBAT.md files in subdirectories take precedence over root.
- This format can coexist with AGENTS.md. They serve complementary purposes:
  AGENTS.md tells agents *how* to work. SHABBAT.md tells them *when* to stop.
- Consult a qualified posek for novel edge cases. This format identifies the
  question; it does not replace a halachic authority.

---

*Shabbat Shalom.*
