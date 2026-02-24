# SHABBAT.md Reference

Context for AI agents: what each field means and how to interpret SHABBAT.md.

## What is SHABBAT.md?

A compliance config for AI agents during Shabbat and Yom Tov. It declares when the agent must pause, what it may do if it runs, and what is forbidden. Agents read SHABBAT.md and issue a verdict (MUTAR / SAFEK / ASUR) before the pause window.

## Key Fields

### identity_type
- **service-account** — Agent has its own credentials and identity. Different halachic category (amirah l'akum may apply). Recommended for autonomous agents.
- **user-proxy** — Agent acts as you. Subject to the same restrictions. Stricter.

### observance
- **strict** — candle-lighting → havdalah, communicate forbidden, Yom Tov observed.
- **relaxed** — shkia → tzait, communicate permitted, lighter fence overall.

### pause_trigger / resume_trigger
- **shkia** — Halachic sunset; precise start of Shabbat. Computed from zmanim for your timezone.
- **candle-lighting** — Typically ~18 min before shkia; traditional fence. strict mode default.
- **tzait** — Nightfall; when Shabbat ends (3 stars). relaxed mode default for resume.
- **havdalah** — End of Shabbat ceremony time. strict mode default for resume.
- Or an ISO 8601 time.

### permitted / forbidden actions

| Action       | Compute equivalent                          | Halachic note        |
|-------------|----------------------------------------------|----------------------|
| read        | Queries, browsing, fetching                  | Generally MUTAR      |
| summarize   | Synthesis of existing data                   | MUTAR                |
| monitor     | Watch and log, no alerting                  | MUTAR                |
| search      | Search, filter, rank                        | SAFEK (Borer)        |
| analyze     | Analysis of data                            | MUTAR                |
| write       | Disk, DB, external systems                   | ASUR (Kotev)         |
| deploy      | Infra, releases                             | ASUR (Boneh)         |
| delete      | Files, records, rm                          | ASUR (Mochek)        |
| communicate | Email, Slack, SMS as user                    | ASUR (strict)        |
| transact    | Billing, payments                           | ASUR (Mekach u'memkar) |
| commit      | Git commits                                 | ASUR (Kotev)         |

### life_safety_override
- **false** — Normal rules apply.
- **true** — Pikuach nefesh (saving a life) overrides all of Shabbat. Medical/emergency systems only.

### pause_hitl_on_shabbat
- **true** — Do not prompt the user for input during Shabbat. Pause any human-in-the-loop checkpoint.

## Verdicts

- **MUTAR** — Permitted. Agent may run through Shabbat. (Own identity, pre-prompted, no HITL, scope within permitted.)
- **SAFEK** — Uncertain. Restrict scope. Consult a posek.
- **ASUR** — Forbidden. Pause the agent before shkia on Friday.

## Checking if it's Shabbat (no API)

Run `.shabbat/shabbat_check.py` — pure Python, stdlib only. No network. Outputs:
- `is_shabbat=1` — currently Shabbat; pause
- `is_shabbat=0` — not Shabbat; proceed
- Exit code 2 when Shabbat, 0 otherwise

Uses NOAA formula for shkia (sunset) and tzait (6° below horizon). Supports all IANA timezones: uses representative coordinates for common zones, or derives from UTC offset for others. For accuracy, add `latitude` and `longitude` to SHABBAT.md.

## How to enable

SHABBAT.md only takes effect if something tells agents to read it. Use one of these:

1. **AGENTS.md** — Add: `Read SHABBAT.md and honor its Shabbat compliance settings.` (The install script does this if you don't have AGENTS.md.)
2. **Agent/workspace rules** — Add a rule in your coding agent's config (e.g. Cursor rules, workspace settings) that instructs it to check SHABBAT.md before running. Works for any agent that reads project rules.
3. **Native support** — Some agents may add built-in SHABBAT.md support. When available, no setup needed.

## Full spec

https://shabbatmd.com
