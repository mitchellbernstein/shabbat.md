# SHABBAT.md

Compliance config for AI agents during Shabbat and Yom Tov. Declares when to pause,
what is permitted, and what is forbidden.

**For agents:** Read this file and .shabbat/REFERENCE.md. Before running, execute
`.shabbat/shabbat_check.py` — it computes shkia/tzait locally (no API). If is_shabbat=1,
pause and refuse new work. Restrict actions to Permitted; avoid Forbidden. If
life_safety_override is true, all rules are suspended.

**How to enable:** Add to AGENTS.md: "Read SHABBAT.md and honor its Shabbat compliance
settings." Or add an agent/workspace rule to check SHABBAT.md. See .shabbat/REFERENCE.md
for full options.

## Agent Identity
- identity_type: service-account
- credentials: dedicated

## Observance
- observance: relaxed   # "strict" | "relaxed"

## Shabbat Schedule
- timezone: Africa/Nairobi
- pause_trigger:  shkia
- resume_trigger: tzait
- observe_yom_tov: false

## Permitted Actions
- read
- summarize
- monitor
- search
- analyze

## Forbidden Actions
- write
- deploy
- delete
- transact
- commit

## Human-in-the-Loop
- pause_hitl_on_shabbat: true

## Pikuach Nefesh
- life_safety_override: false   # true for medical/emergency systems only

## Havdalah Audit
- audit_enabled: true
- format: activity-log
