# Demo 5: /schedule — Recurring and One-Shot Tasks

**Feature**: `/schedule` lets agy set timers and recurring jobs that wake it up automatically — no polling needed.

## What Is /schedule?

Agy can schedule itself to wake up after a delay or on a recurring interval. While waiting, it goes idle (uses no resources). When the timer fires, the system wakes agy and it executes the scheduled task.

## Demo: One-Shot Reminder (60 seconds)

**Prompt sent to agy:**
```
Use /schedule to set up a one-shot reminder that triggers in 1 minute to check if the
url_shortener directory exists and report its contents.
```

**What agy did:**

| Step | Time | Action |
|------|------|--------|
| 1 | T+0s | Registered a 60-second timer via `Schedule()` tool (task-150) |
| 2 | T+0s | Went idle — yielded control, stopped all tool calls |
| 3 | T+60s | System fired the timer, woke agy with a notification |
| 4 | T+60s | Agy ran `ListDir()` on `url_shortener/` and reported contents |

**Result after wakeup:**
```
url_shortener/
├── app/          # FastAPI modules + static frontend
├── tests/        # unittest integration tests
├── requirements.txt
└── shortener.db  # Active SQLite database
```

## Use Cases

| Pattern | Example |
|---------|---------|
| One-shot timer | "Remind me in 10 minutes to check the deploy" |
| Recurring poll | "Check CI status every 5 minutes until it passes" |
| Background monitor | "Watch the server logs and alert me if errors spike" |
| Deferred task | "In 30 minutes, run the full test suite" |

## How It Works Under the Hood

1. **Register**: Agy calls `Schedule(DurationSeconds=N, prompt="...")` 
2. **Yield**: Agy ends its turn and goes idle
3. **Fire**: System tracks the countdown and sends a wakeup notification
4. **Execute**: Agy resumes with the scheduled prompt and runs the task

## Key Takeaway

`/schedule` turns agy into an autonomous background worker. Set a timer and walk away — agy wakes itself up and handles it. No terminal babysitting required.
