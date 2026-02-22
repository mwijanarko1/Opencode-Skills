---
name: build
version: 2.0.0
description: |
  Production-grade build and verification workflow for web and mobile projects.
  Prioritizes deterministic checks (lint, typecheck, tests, build) and fixes root
  causes before reporting success.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
---

# Build: Senior Verification Pipeline

Use this command to verify production readiness, not just compile output.

## Rules

1. Do not update dependencies unless the user explicitly asks.
2. Prefer deterministic checks over ad-hoc fixes.
3. If a command is missing, report it and continue with available checks.
4. Keep scope to current workspace unless user requests otherwise.

## Stack Detection

Use repository signals to select checks:
- Next.js/React web: `next`, `react`, `app/`, `src/app/`
- React Native / Expo: `react-native`, `expo`, `app.json`, `eas.json`
- Swift iOS: `*.xcodeproj`, `Package.swift`, `*.swift`

## Build Workflow

### 1) Fast preflight

- Verify package manager/lockfile consistency.
- Inspect available scripts before running commands.

Node example:
```bash
cat package.json
```

### 2) Run verification gates

#### Web (React / Next.js / Vercel)
Run in this order when present:
```bash
npm run lint --if-present
npm run typecheck --if-present
npm run test --if-present
npm run build --if-present
```

Additional Vercel-focused checks when available:
```bash
npx vercel build
```

#### React Native / Expo
Run in this order when present:
```bash
npm run lint --if-present
npm run typecheck --if-present
npm run test --if-present
npx expo-doctor
npx expo export --platform all
```

#### Swift iOS
Prefer project-provided scripts first. If none exist, use xcodebuild if available:
```bash
xcodebuild -list
xcodebuild -scheme <Scheme> -destination 'platform=iOS Simulator,name=iPhone 15' build
xcodebuild -scheme <Scheme> -destination 'platform=iOS Simulator,name=iPhone 15' test
```

### 3) Fix failures

- Diagnose root cause from logs.
- Apply minimal targeted code/config fix.
- Re-run the failed gate and downstream gates.

### 4) Report

Report exactly what ran and outcomes.

## Output Format

### Build Status
`PASS` or `FAIL`

### Commands Run
- `<command>` - pass/fail/skipped

### Issues Fixed
- `<file>` - `<summary>`

### Remaining Risks
- Missing gates, unavailable tools, or unexecuted tests

## Senior Quality Bar

A build is only `PASS` when:
- Required gates for detected stack have passed, or
- Any skipped gate has an explicit reason and risk note.

If this bar is not met, return `FAIL` with next required action.
