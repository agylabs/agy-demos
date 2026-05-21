# Demo 6: Web Browsing and Search

**Feature**: Agy can search the web and read URLs in real-time to get up-to-date information.

## What Can Agy Do on the Web?

- **Web Search**: Query search engines for current information
- **URL Reading**: Fetch and process content from any public URL
- **Live Documentation**: Look up the latest API docs, release notes, changelogs

## Demo: Research a Recent Release

**Prompt sent to agy:**
```
Search the web for "Google Gemini 3.5 Flash release date" and tell me when it was released
and what its key improvements are. Then create a file with your findings.
```

**What agy did:**
1. Ran two parallel web searches:
   - `"Google Gemini 3.5 Flash release date"`
   - `"Google Gemini 3.5 Flash features key improvements"`
2. Synthesized findings from multiple search results
3. Created `gemini-flash-notes.md` with structured findings

**Key findings retrieved:**
- Released May 19, 2026 at Google I/O
- Enhanced agentic workflows and multi-step reasoning
- 280+ output tokens/second, 1M context window
- Configurable thinking levels (Minimal/Low/Medium/High)
- Lower hallucinations, higher coding benchmarks

## Practical Use Cases

| Use Case | Example |
|----------|---------|
| API docs | "Look up the latest FastAPI middleware docs" |
| Debugging | "Search for this error message and find the fix" |
| Research | "What's new in Python 3.13?" |
| Best practices | "Find the current OWASP top 10 for 2026" |
| Dependency check | "Is there a newer version of React Router?" |

## Key Takeaway

Agy's knowledge isn't frozen — it can search the web in real-time to get current information, making it useful for researching new releases, finding documentation, and debugging with the latest solutions.
