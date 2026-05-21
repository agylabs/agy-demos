# Go 1.24 Release News

*Status: Research completed successfully by parallel AI subagent.*

Go 1.24 (released in February 2025) introduces several major language, tooling, and performance upgrades. Here are the top 3 newest features:

### 1. Generic Type Aliases
Go 1.24 fully supports parameterizing type aliases with generic type arguments (e.g., `type Set[T any] = map[T]struct{}`). This simplifies complex refactorings and library designs where types must be parameterized.

### 2. First-Class Tool Dependencies
A new native way to manage development tools (such as linters or code generators) directly in your module:
* **Add tools:** `go get -tool github.com/golangci/golangci-lint/cmd/golangci-lint@latest` (stores a `tool` directive in `go.mod`).
* **Run tools:** `go tool golangci-lint run ./...`
* **Benefits:** Eliminates the legacy `tools.go` workaround and locks exact versions for your entire team.

### 3. Directory-Scoped Filesystem Access (`os.Root`)
The new `os.Root` type enables directory-limited filesystem access. Any file or directory operations performed using an `os.Root` instance are strictly bound within the specified root directory, preventing directory traversal vulnerabilities at the system level.

---
*Other notable changes include under-the-hood **SwissTable-based maps** (improving map access performance and memory efficiency by 2-3%), and the experimental **`testing/synctest`** package for isolated concurrent testing with fake clocks.*
