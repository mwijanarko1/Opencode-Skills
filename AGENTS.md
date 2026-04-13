# Instructions for Agent Tools

Canonical config for Cursor, Codex, OpenCode, and Antigravity. All tools reference this folder.

## Goal

These skills compose into a single high-agency coding system. Build a stack for the task; layer the minimum useful set instead of loading everything blindly.

**Stack order:** Foundation → Domain → Verification → Finish

## Test-Driven Programming Default

Agents should work test-first whenever they are changing behavior or fixing defects.

1. **Define the expected behavior first** — Start by identifying the observable behavior, edge cases, and regression risk before editing production code.
2. **Write or update a failing test first** — For bug fixes and feature work, add the narrowest meaningful unit, integration, or end-to-end test that fails for the current behavior. If a test-first step is genuinely impractical, state why and use the smallest alternative verification.
3. **Make the smallest production change** — Implement only what is needed to pass the new or updated test while preserving existing behavior.
4. **Run the relevant test target** — Prefer the closest fast test first, then broader checks when the change touches shared behavior or user-facing flows.
5. **Report verification clearly** — Final responses should name the tests run. If tests were not run, state the blocker or reason.

TDD does not mean adding brittle coverage for implementation details. Follow `testing-strategies`: prioritize confidence, behavior, and critical user journeys over raw coverage numbers.

## Enforced Contract

All rules, constraints, and checklists that the agent MUST follow every time live in structured form:

| Source | Purpose |
|--------|---------|
| **`agent-policy.json`** | Default stack, skill triggers, task mapping, conflict resolution, codebase awareness, delegation |
| **`scripts/validate_agent_policy.py`** | Validates policy, checks skills exist, optional CODEBASE_MAP gate |

**If prose and structured policy disagree, the JSON contract and validator win.**

## Skill loading and disclosure (mandatory)

Applies to Cursor, OpenCode, Codex, Antigravity, and every shared subagent under `agents/`. This aligns all tools with the same explicit skill contract Codex uses.

1. **Read** — Before substantive work (edits, plans, or reviews), read each active skill’s `SKILL.md` from the canonical tree (`skills_root` in `agent-policy.json`, usually `~/.agents/skills/<skill-name>/SKILL.md`). Build the stack from `default_stack`, `task_mapping`, `skill_triggers`, and `capability_clusters` (for subagents, include every path listed in that subagent file). Peer `skills/` symlinks must resolve to these same files.

2. **Disclose** — In the first substantive assistant message of the thread (or at the start of a one-shot subagent run), list which skills you actually loaded, using each skill’s directory name only (for example `coding-standards`, `frontend-web-development`).

3. **Gaps** — If a `SKILL.md` is missing or unreadable, name the path and rely on `AGENTS.md` plus `agent-policy.json` only for what you could not load.

Run the validator before substantial work (or as a gate):

```bash
python3 ~/.agents/scripts/validate_agent_policy.py
# Or: AGENTS_ROOT=~/.agents python3 scripts/validate_agent_policy.py
# Exit 0 = pass. Set AGENT_STRICT_CODEBASE=1 to require CODEBASE_MAP.
```

## Available Skills

Skills live in `~/.agents/skills/` (canonical). Each tool may symlink `skills/` into its own config.

| Category | Skills |
|----------|--------|
| Foundation | ai-interaction-workflow, coding-standards, security-vulnerability-mitigation, testing-strategies, output-skill, cartographer |
| Product | frontend-web-development, backend-architecture, ios-development, ios-app-store-compliance, expo-docs |
| iOS/Swift | swiftui-pro, swiftdata-pro, swift-concurrency-pro, swift-testing-pro, add-component, build-feature, explore-recipes |
| Automation | agent-delegation, ai-bridge (shared multi-agent delegation and peer-bridge workflow built around the `agent-delegation` skill and `ai-delegate` / `ai-dispatch` commands) |
| Imported | vercel-composition-patterns, vercel-react-best-practices, vercel-react-native-skills, web-design-guidelines, website-compliance, technical-seo |
| Design | taste-skill, redesign-skill, soft-skill (secondary only), design-md-gallery (secondary reference only), design-systems-reference (secondary reference only) |

**Icon preference for UI work:** Prefer Phosphor (`@phosphor-icons/react`), Hugeicons (`@hugeicons/react` with `@hugeicons/core-free-icons`), and Tabler Icons (`@tabler/icons-react`) over Lucide defaults. Check `package.json` before imports and avoid adding icon dependencies unless the task justifies it.

**iOS bundle**: For full-stack native Apple development, use all iOS skills together. Trigger: "use all iOS skills", "ios full stack", "swift native full". See `agent-policy.json` → `task_mapping.mobile.ios_bundle`.

See `agent-policy.json` for: default stack, when to add which skills, task mapping, design rules, conflict resolution.

## Shared Subagents

Shared subagents live in `~/.agents/agents/` and are the canonical source for every tool.

- Cursor should expose them via `.cursor/agents/`
- OpenCode should expose them via `agents/`
- Codex should expose them via `agents/` with `child_agents_md = true`

Keep the peer roots synced to the canonical files instead of maintaining separate per-tool copies.

Subagent prompts under `agents/` include mandatory **Skill loading** lines: read the listed canonical `SKILL.md` files before substantive output and disclose loaded skills the same way as the main agent (see **Skill loading and disclosure** above and `agent-policy.json` → `skill_loading_disclosure`).

### Native Subagent Routing

The main agent may invoke native subagents independently without asking first when the task benefits from specialist focus, parallel work, fresh review, or context isolation.

Use native subagents before cross-tool delegation. Route by capability cluster, not by raw skill count:

| Task intent | Preferred subagent |
|-------------|--------------------|
| codebase mapping | `cartographer` |
| broad code review | `code-reviewer` |
| backend/API/schema/auth | `backend-architect` |
| web/frontend implementation | `frontend-engineer` |
| greenfield UI or redesign | `design-engineer` |
| UI/accessibility audit | `ui-auditor` |
| security review | `security-auditor` |
| privacy/compliance/SEO audit | `compliance-seo-auditor` |
| mobile/Swift/React Native/Expo | `mobile-engineer` |

The main agent remains responsible for final synthesis, conflict resolution, and verification. Do not delegate code review away from the final reviewer when the active tool's higher-priority instructions reserve review for the main agent.

## AI Bridge

The AI bridge (`ai-delegate` / `ai-dispatch`) is a backup and cross-tool escape hatch, not the default work router.

- Use the AI bridge only when the user explicitly asks for it.
- The user must name the target coding tool (`codex`, `cursor`, `opencode`, `claude`, `goose`, or a configured adapter). If they ask for the bridge without naming a target, ask which tool to open.
- Do not use `--target auto` or difficulty-based bridge routing unless the user explicitly asks for automatic bridge routing.
- Prefer native subagents for normal specialist work inside the active tool.

## Codebase Awareness

Before substantial changes: check for `docs/CODEBASE_MAP.md` or `CODEBASE_MAP.md`. It is usually in a docs folder.

- **Missing** → use `cartographer`, create map first.
- **Present** → review before editing.

(Defined in `agent-policy.json` → `codebase_awareness`.)

## Core Principles

- **Simplicity First**: Smallest change that fully solves the problem.
- **No Laziness**: Find root causes. Do not paper over systemic issues.
- **Minimal Impact**: Touch only what materially needs to change.

(Defined in `agent-policy.json` → `core_principles`.)

## Supply-Chain Defaults

- **Locked First**: Prefer the existing lockfile and exact pinned versions. Do not widen ranges or refresh lockfiles unless the user explicitly asked for dependency work.
- **No Ad-Hoc Executors**: Do not bake `npx`, `pnpm dlx`, `bunx`, `uvx`, `curl | sh`, or `@latest` into shared commands, configs, or automation. Prefer repo-local pinned binaries or exact installed versions.
- **Age-Gated Installs**:
  - npm should respect `~/.npmrc` with `min-release-age=7` and `ignore-scripts=true`.
  - Bun should respect `~/.bunfig.toml` with a 7-day minimum release age. Bun already avoids arbitrary dependency lifecycle scripts by default; do not add packages to `trustedDependencies` casually.
  - uv should respect `~/.config/uv/uv.toml` with a 7-day exclusion window. If the local uv build rejects friendly durations in config, use the equivalent RFC 3339 timestamp instead.
- **Build/Commit Hygiene**:
  - `/build` must not auto-upgrade dependencies.
  - `/build` must not check latest package releases or run dependency-audit/update discovery commands such as `npm outdated`, `pnpm outdated`, `bun outdated`, `npm-check-updates`, or `npm view` unless the user explicitly asked for dependency work.
  - `/build` should only install dependencies when required to unblock the requested work, using frozen lockfile modes where possible.
  - `/commit` must not widen dependency changes or introduce new package-manager fetches as a side effect.

---

Refer to individual `SKILL.md` files for task-specific workflows. Refer to `agent-policy.json` for machine-enforceable rules.
