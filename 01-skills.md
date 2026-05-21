# Demo 1: Skills

**Feature**: Built-in skill ecosystem — 56+ specialized skills for web, mobile, Firebase, science, and more.

## What Are Skills?

Skills are expert playbooks that give agy deep domain knowledge. They're loaded on-demand and can fetch live data, run CLI tools, and follow curated best practices. Skills come from plugins and can be created per-workspace or globally.

## How to Use

```
/skills              # List all available skills in the TUI overlay
```

Then reference a skill in your prompt — agy activates it automatically.

## Demo: Modern Web Guidance Skill

**Prompt sent to agy:**
```
Use the modern-web-guidance skill to look up the latest CSS container queries best practices.
Give me a short summary of what you find.
```

**What agy did:**
1. Read the skill definition (`SKILL.md`) to understand how to use it
2. Ran `npx -y modern-web-guidance@latest search "container queries"` to find relevant guides
3. Retrieved multiple guides: `fluid-scaling`, `size-aware-styling`, `css-layout`
4. Synthesized a concise summary covering:
   - Defining containment (`container-type`, `container-name`)
   - Fluid scaling with container query units (`cqi`, `cqb`) + `clamp()`
   - Size-aware layouts with `@container` rules
   - Progressive enhancement fallbacks

## Available Skill Categories (56 skills)

| Category | Count | Examples |
|----------|-------|---------|
| Chrome DevTools | 5 | a11y debugging, LCP optimization, memory leak diagnosis |
| Firebase | 11 | Auth, Firestore, Data Connect, Crashlytics, security rules |
| Modern Web | 2 | CSS/HTML best practices, Chrome Extensions (Manifest V3) |
| Science | 25+ | AlphaFold, PubMed, PDB, PyMOL, genomics, proteomics |
| Android | 1 | Android CLI orchestration |
| Utility | 1 | Workflow skill creator (distill workflows into reusable skills) |

## Key Takeaway

Skills turn agy into a domain expert on demand — no configuration needed. Just describe what you want and reference the domain; agy loads the right skill automatically.
