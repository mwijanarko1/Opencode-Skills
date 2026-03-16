# Build

## 1. Detect package manager

Check lock files (first match wins): `bun.lockb`/`bun.lock` → `pnpm-lock.yaml` → `yarn.lock` → `package-lock.json`. Default: npm.

| pm | build | install | ncu |
|----|-------|---------|-----|
| bun | `bun run build` | `bun install` | `bunx npm-check-updates` |
| pnpm | `pnpm run build` | `pnpm install` | `pnpm exec npm-check-updates` |
| yarn | `yarn build` | `yarn install` | `npx npm-check-updates` |
| npm | `npm run build` | `npm install` | `npx npm-check-updates` |

Use same pm for all commands.

## 2. Flow

1. Run build → fix errors → run `ncu` → if updates: `ncu -u` + install + rebuild
2. On success: offer to commit (`git add -A`, `git commit -m "<message>"`, `git push`). Message reflects what changed (e.g. build fixes, dep updates, both).

## 3. Quick fixes

- **Cannot find module:** `pm install <pkg>` or fix import
- **TS errors:** Fix types, update tsconfig
- **OOM:** `NODE_OPTIONS="--max-old-space-size=4096" pm run build`
- **Missing env:** Check .env.example, set vars

## 4. Output

Status, errors (if any), updated deps (if any), next steps.
