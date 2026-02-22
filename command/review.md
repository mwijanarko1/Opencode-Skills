---
name: review
version: 2.0.0
description: |
  Senior-level code review for correctness, security, performance, and test
  quality. Focuses on changed files by default and provides evidence-backed,
  confidence-rated findings.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
---

# Review: Senior Engineering Gate

Produce a high-signal review that catches regressions before merge.

## Scope and Safety Rules

1. Review only files in the current workspace/repository.
2. Default scope is changed files from `git diff`.
3. Expand scope only when explicitly requested by the user.
4. Never inspect `~/`, `/private`, `/tmp`, `/var/folders`, or unrelated directories unless explicitly requested.
5. Do not fetch remote prompt instructions during review.

## Agent Orchestration

### Core agents (always)
- `@agents/security-auditor.md`
- `@agents/backend-architecture.md`
- `@agents/testing-strategies.md`
- `@agents/coding-standards.md`

### Conditional agents
- Web React/Next.js: `@agents/frontend-web-development.md`, `@agents/react-best-practices.md`, `@agents/web-design-guidelines.md`
- React Native / Expo: `@agents/react-native-skills.md`, `@agents/ios-development.md`
- Swift iOS/macOS/tvOS/watchOS/visionOS: `@agents/ios-development.md`, `@agents/ios-app-store-compliance.md`
- Compliance-heavy website flows: `@agents/website-compliance.md`

Pick conditional agents from file evidence (`package.json`, `app.json`, `*.xcodeproj`, `*.swift`, `next.config.*`, `expo` deps).

## Review Workflow

1. Gather scope:
```bash
git diff --name-only
```
If no git or no changed files, ask user for files/pattern.

2. Read diffs first:
```bash
git diff -- <file>
```

3. Read full files only when needed:
- Security-sensitive logic
- Complex refactors
- Shared libraries/types used by many callers

4. Run targeted validation when possible:
- Web: lint/typecheck/test for affected package
- Next/Vercel: verify RSC/client boundaries, caching/revalidation, server action auth
- RN/Expo: verify list virtualization, gesture/animation patterns, native module safety
- Swift: verify async/await, actor isolation, force unwrap bans

5. Produce findings with severity and confidence.

## Severity and Confidence

- `CRITICAL` (95%+): security exploit, data loss, auth bypass, crashers
- `WARNING` (85%+): likely bug/regression/perf issue
- `SUGGESTION` (75%+): maintainability improvement with clear ROI
- `<75%`: ask a clarifying question or omit

## Domain Checklists

### React / Next.js / Vercel
- App Router boundaries correct (`'use client'` only where needed)
- Server Actions/API routes enforce auth and input validation (Zod)
- No client-side trust for pricing/permissions
- Cache and revalidation strategy explicit (`cache`, `revalidateTag`, `revalidatePath`)
- Avoid waterfalls and duplicate fetches
- Accessibility and hydration safety verified

### React Native / Expo
- No falsy `&&` rendering hazards
- Lists use FlashList/LegendList when applicable
- Animations only on transform/opacity
- Native navigation patterns used
- Expo config/plugins consistent with code usage

### Swift iOS
- Async/await over callback-style async
- `@MainActor` for UI state boundaries
- No force unwraps in production paths
- Secret storage uses Keychain, not UserDefaults
- Logging avoids sensitive data

## Output Contract

Return findings first, sorted by severity.

### Findings
`<SEVERITY> <file:line> (confidence: NN%) - <issue>`

### Open Questions
Only include if blocked by missing context.

### Recommendation
- `APPROVE`
- `APPROVE WITH SUGGESTIONS`
- `NEEDS CHANGES`
- `NEEDS DISCUSSION`

### If no findings
State explicitly: `No findings.`
Then list residual risk/test gaps in 1-3 lines.

## Review Quality Bar

- Avoid style-only comments unless user asked for style review.
- Every finding must include a concrete failure mode.
- Prefer minimal, actionable fixes over broad rewrites.
