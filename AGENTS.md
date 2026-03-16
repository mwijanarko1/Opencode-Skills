# Instructions for Agent Tools

Canonical config for Cursor, Codex, OpenCode, and Antigravity. All tools reference this folder.

## Goal

These skills compose into a single high-agency coding system. Build a stack for the task; layer the minimum useful set instead of loading everything blindly.

**Stack order:** Foundation → Domain → Verification → Finish

## Enforced Contract

All rules, constraints, and checklists that the agent MUST follow every time live in structured form:

| Source | Purpose |
|--------|---------|
| **`agent-policy.json`** | Default stack, skill triggers, task mapping, conflict resolution, codebase awareness, delegation |
| **`scripts/validate_agent_policy.py`** | Validates policy, checks skills exist, optional CODEBASE_MAP gate |

**If prose and structured policy disagree, the JSON contract and validator win.**

Run the validator before substantial work (or as a gate):

```bash
python ~/.agents/scripts/validate_agent_policy.py
# Or: AGENTS_ROOT=~/.agents python scripts/validate_agent_policy.py
# Exit 0 = pass. Set AGENT_STRICT_CODEBASE=1 to require CODEBASE_MAP.
```

## Available Skills

Skills live in `~/.agents/skills/` (canonical). Each tool may symlink `skills/` into its own config.

| Category | Skills |
|----------|--------|
| Foundation | ai-interaction-workflow, coding-standards, security-vulnerability-mitigation, testing-strategies, output-skill, cartographer |
| Product | frontend-web-development, backend-architecture, ios-development, ios-app-store-compliance, expo-docs |
| iOS/Swift | swiftui-pro, swiftdata-pro, swift-concurrency-pro, swift-testing-pro, add-component, build-feature, explore-recipes |
| Imported | vercel-composition-patterns, vercel-react-best-practices, vercel-react-native-skills, web-design-guidelines, website-compliance, technical-seo |
| Design | taste-skill, redesign-skill, soft-skill (secondary only) |

**iOS bundle**: For full-stack native Apple development, use all iOS skills together. Trigger: "use all iOS skills", "ios full stack", "swift native full". See `agent-policy.json` → `task_mapping.mobile.ios_bundle`.

See `agent-policy.json` for: default stack, when to add which skills, task mapping, design rules, conflict resolution.

## Codebase Awareness

Before substantial changes: check for `docs/CODEBASE_MAP.md` or `CODEBASE_MAP.md`.

- **Missing** → use `cartographer`, create map first.
- **Present** → review before editing.

(Defined in `agent-policy.json` → `codebase_awareness`.)

## Core Principles

- **Simplicity First**: Smallest change that fully solves the problem.
- **No Laziness**: Find root causes. Do not paper over systemic issues.
- **Minimal Impact**: Touch only what materially needs to change.

(Defined in `agent-policy.json` → `core_principles`.)

---

Refer to individual `SKILL.md` files for task-specific workflows. Refer to `agent-policy.json` for machine-enforceable rules.
