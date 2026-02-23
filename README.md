# SHABBAT.md

**Make Agents Kosher Again.**

SHABBAT.md is a simple, open format for declaring Shabbat and Yom Tov compliance
settings for AI coding agents. Place it at the root of your repository.

Think of SHABBAT.md as a contract between you and your agent: a declaration of what it
may do when you are unavailable to supervise — and when it must rest alongside you.

## The She'elah That Started It All

> **@jacob_posel:** Can a Jew let his agent run over Shabbat if the last prompt was Friday afternoon?
>
> **@levie:** If the agent is assuming your identity, no, but if it's openclaw style with its own identity on its own machine should be fine.

@levie's reply is a precise application of *amirah l'akum* and *grama* — two foundational
halachic principles governing indirect labor. SHABBAT.md makes this determination automatic.

## Quick Start

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

See [SHABBAT.md](./SHABBAT.md) for the full format specification.

## The Psak (Verdict)

A Shabbat-aware agent reads this file and issues one of three verdicts:

- **MUTAR** ✅ — permitted; agent may run through Shabbat
- **SAFEK** ⚠️ — uncertain; consult a posek before proceeding  
- **ASUR** ❌ — forbidden; pause the agent before shkia on Friday

## Key Principles

| Principle | Application |
|---|---|
| *Grama* (indirect causation) | Agent instructed before Shabbat, runs autonomously → may be permitted |
| *Amirah l'akum* | Agent with its own identity → different category than one acting as you |
| *Shvitat keilim* | Your tools should rest when you do |
| *Pikuach nefesh* | Life-safety systems override Shabbat entirely |

## Coexistence with AGENTS.md

SHABBAT.md and AGENTS.md serve complementary purposes:

- **AGENTS.md** tells agents *how* to work on your project
- **SHABBAT.md** tells them *when* to stop

Both can live at the root of the same repository.

## Website

[shabbatmd.com](https://shabbatmd.com)

## Contributing

Pull requests welcome. Novel halachic edge cases especially appreciated.
Please include a citation to relevant responsa literature when proposing changes
to the melachot mapping or psak logic.

## Disclaimer

SHABBAT.md is a configuration format. It is not a halachic authority. Consult a
qualified posek for novel edge cases and actual halachic decisions. This project
identifies the question; it does not replace a rabbi.

## License

MIT. See [LICENSE](./LICENSE).

---

*Shabbat Shalom.*
