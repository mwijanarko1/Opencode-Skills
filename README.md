# OpenCode Skills Setup

Shared agent configuration for OpenCode, Cursor, Codex, and Antigravity. Use this as a reference or copy into your own config.

## Quick Setup

1. **Clone this repo** (or copy the contents).

2. **For OpenCode**: Copy or symlink into `~/.config/opencode/`:
   ```bash
   cp -r agents command skills AGENTS.md agent-policy.json ~/.config/opencode/
   mkdir -p ~/.config/opencode/scripts
   cp scripts/validate_agent_policy.py ~/.config/opencode/scripts/
   ```

3. **For Cursor**: Copy `AGENTS.md` and `agent-policy.json` into your project's `.cursor/` or `~/.cursor/`. Symlink or copy `skills/` to `~/.cursor/skills/` or `~/.agents/skills/`.

4. **Validate** (optional):
   ```bash
   AGENTS_ROOT=/path/to/this/repo python scripts/validate_agent_policy.py
   ```

## Contents

| Path | Purpose |
|------|---------|
| `AGENTS.md` | Root instructions for skill composition |
| `agent-policy.json` | Machine-readable rules, triggers, task mapping |
| `agents/` | Clustered specialist subagents |
| `command/` | Task-specific commands (e.g. review) |
| `skills/` | Skill library (foundation, product, iOS, design) |
| `scripts/validate_agent_policy.py` | Policy validator |

## iOS Skills

Includes SwiftUI Pro, SwiftData Pro, Swift Concurrency Pro, Swift Testing Pro. Use "all iOS skills" or "ios full stack" to load the bundle.
