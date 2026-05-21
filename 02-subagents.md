# Demo 2: Subagents

**Feature**: Multi-agent architecture — spawn background agents for parallel work.

## What Are Subagents?

Agy can delegate tasks to specialized subagents that run concurrently in the background. When a subagent finishes, it reports back and the main agent integrates the results. This enables true parallel workflows.

## Available Subagent Types

| Type | Capability | Use Case |
|------|-----------|----------|
| `research` | Read-only, web search, codebase exploration | Finding docs, researching APIs |
| `self` | Full capabilities (clone of main agent) | Independent coding tasks |
| Custom | User-defined system prompt + toolset | Domain-specific agents |

## Demo: Parallel Research + File Creation

**Prompt sent to agy:**
```
Spawn a research subagent to find the top 3 newest features in Go 1.24,
while you simultaneously create a short summary file called go-news.md.
Show me how you can work in parallel with the subagent.
```

**What agy did (in parallel):**

| Main Agent | Research Subagent |
|-----------|-------------------|
| Created `go-news.md` with placeholder | Searched the web for Go 1.24 features |
| Yielded execution, waited | Found and structured the top 3 features |
| Received subagent report | Reported results back |
| Updated `go-news.md` with final content | — |
| Killed subagent (cleanup) | — |

**Result**: `go-news.md` was created with:
1. Generic Type Aliases
2. First-Class Tool Dependencies (`go get -tool`)
3. Directory-Scoped Filesystem Access (`os.Root`)

## Key Details

- Subagents show in the status bar: `1 subagent(s)`
- View all subagents with `/agents`
- Navigate subagent approvals with `ctrl+j` (teleport) and `ctrl+k` (quick approve)
- Subagents can be spawned in isolated workspaces to avoid conflicts

## Key Takeaway

Subagents let agy parallelize work — research while coding, test while building, explore while implementing. The main agent orchestrates and integrates results automatically.
