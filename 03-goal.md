# Demo 3: /goal — Autonomous Task Completion

**Feature**: `/goal` makes agy work autonomously until a task is fully complete — no intermediate questions, no pausing for approval.

## What Is /goal?

Normally, agy may pause to ask clarifying questions or request approval. The `/goal` command tells agy to lock in and aggressively pursue the task to completion without stopping. It plans, implements, tests, and verifies — all autonomously.

## Demo: Build a CLI Tool End-to-End

**Prompt sent to agy:**
```
/goal Create a Python CLI tool called "countdown.py" that takes a number as an argument
and prints a countdown from that number to 1, with each number on a new line, followed
by "Liftoff!" at the end. Include argument validation and a --reverse flag to count up
instead. Write tests in test_countdown.py and make sure they pass.
```

**What agy did autonomously (zero human input):**

| Step | Action | Details |
|------|--------|---------|
| 1 | Environment check | Verified Python 3 and unittest available |
| 2 | Created implementation plan | Wrote `implementation_plan.md` |
| 3 | Auto-approved plan | Didn't wait for human — `/goal` mode |
| 4 | Created task tracker | Wrote `task.md` with checklist |
| 5 | Wrote `countdown.py` | argparse, validation, `--reverse` flag |
| 6 | Wrote `test_countdown.py` | 9 test cases using `unittest` + subprocess |
| 7 | Ran automated tests | All 9 passed |
| 8 | Manual verification | Tested `countdown.py 3`, `5 -r`, `-1`, and no-args |
| 9 | Created walkthrough | Wrote `walkthrough.md` with design + diffs |
| 10 | Final audit | Requirements checklist mapped to evidence |

**Result**: 9/9 tests passing, fully working CLI tool.

```bash
$ python3 countdown.py 5
5
4
3
2
1
Liftoff!

$ python3 countdown.py 3 --reverse
1
2
3
Liftoff!
```

## Artifacts Generated

Agy also created planning artifacts tracked via `/artifact`:
- `implementation_plan.md` — design before coding
- `task.md` — progress checklist
- `walkthrough.md` — post-completion summary with diffs

## Key Takeaway

`/goal` is agy's "overnight mode" — give it a well-defined task and walk away. It plans, builds, tests, verifies, and documents everything without needing human intervention.
