# OpenCode Skills Setup

Snapshot of the shared `~/.agents` configuration for OpenCode, Cursor, Codex, and Antigravity. Use this folder as a portable reference, or copy/symlink the pieces into a tool-specific config root.

## Quick Setup

1. **Clone this repo** (or copy the contents).

2. **For OpenCode**: Copy the snapshot into `~/.config/opencode/`:
   ```bash
   cp -R agents command docs skills AGENTS.md agent-policy.json .skill-lock.json ~/.config/opencode/
   mkdir -p ~/.config/opencode/scripts
   cp scripts/*.py ~/.config/opencode/scripts/
   ```

3. **For canonical local use**: Prefer keeping `~/.agents` as the source of truth and symlinking peer roots with:
   ```bash
   python3 ~/.agents/scripts/sync_peer_roots.py
   ```

4. **Validate the canonical setup**:
   ```bash
   python3 ~/.agents/scripts/validate_agent_policy.py
   ```

## Contents

| Path | Purpose |
|------|---------|
| `AGENTS.md` | Root instructions for skill composition |
| `agent-policy.json` | Machine-readable rules, triggers, task mapping, delegation, sync, and supply-chain defaults |
| `.skill-lock.json` | Skill inventory lock from the canonical tree |
| `agents/` | Native specialist subagents copied from `~/.agents/agents` |
| `command/` | OpenCode task commands |
| `docs/CODEBASE_MAP.md` | Navigation map for this packaged setup |
| `skills/` | Full visible skill library copied from `~/.agents/skills` |
| `skills/.system/` | System skills bundled with Codex |
| `scripts/validate_agent_policy.py` | Policy validator |
| `scripts/sync_peer_roots.py` | Symlink sync helper for local peer roots |

## Included Snapshot

- 57 visible skill directories.
- 2 system skills under `skills/.system/`.
- 13 native subagent prompts, including game-focused agents.
- Current shared policy with TDD, skill disclosure, native subagent routing, AI bridge constraints, and supply-chain defaults.
