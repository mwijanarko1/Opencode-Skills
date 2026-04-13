---
last_mapped: 2026-04-13T09:22:14Z
---

# Codebase Map

## System Overview

This repository packages the shared `~/.agents` setup for OpenCode-oriented use. The root files describe the agent contract, `skills/` contains canonical skill directories, `agents/` contains reusable specialist agent prompts, `command/` contains task command prompts, and `scripts/` contains validation/sync utilities.

## Directory Guide

- `AGENTS.md`: Human-readable operating instructions for agent tools.
- `agent-policy.json`: Machine-readable skill loading, task mapping, subagent routing, sync, TDD, and supply-chain rules.
- `skills/`: Local copy of the shared skill library from `~/.agents/skills`.
- `agents/`: Local copy of selected native subagent prompts from `~/.agents/agents`.
- `command/`: OpenCode command prompts and workflow entry points.
- `scripts/`: Utility scripts, including `validate_agent_policy.py`.
- `docs/`: Navigation and maintenance documentation for this repository.

## Key Workflows

- Validate the package with `AGENTS_ROOT=/Users/mikhail/Desktop/opencode-skills python3 scripts/validate_agent_policy.py`.
- Refresh policy and skill content from `~/.agents` when the canonical tree changes.
- Keep `skills/` broad enough for all advertised task mappings and keep `agents/` aligned with `agent-policy.json` subagent requirements.

## Known Risks

- The package is a snapshot of `~/.agents`; it can drift from the canonical tree unless refreshed intentionally.
- Hidden files such as `.DS_Store` are ignored and should not be committed.
- Some skill directories include supporting references or scripts beyond `SKILL.md`; preserve directory contents during syncs.
