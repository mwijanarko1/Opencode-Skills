---
name: frontend-web-development
description: Senior web standards for React + Next.js on Vercel.
---

# Frontend Web Development (Senior)

Use this skill for React and Next.js implementation/review with production deployment on Vercel.

## Core Engineering Defaults

1. **Server-first:** Use React Server Components by default. Add `'use client'` only for true client interactivity.
2. **Trusted backend:** Never rely on client-side state for authorization, pricing, or feature gating.
3. **Typed boundaries:** Validate all external inputs at boundaries (Route Handlers, Server Actions, webhooks).
4. **Small blast radius:** Prefer minimal diffs and localized changes over large refactors.

## Next.js App Router Standards

### Structure

```text
src/
  app/
    (routes)/
    api/
  features/
  components/
  lib/
```

- Keep route handlers thin; move business logic to services.
- Co-locate feature components/hooks/types.
- Avoid dumping logic in `app/` leaf files.

### Data Fetching and Caching

- Start async work early and avoid waterfalls.
- Use cache/revalidation intentionally:
  - request memoization
  - `revalidateTag` and `revalidatePath` for write paths
  - explicit cache/no-store decisions for sensitive data
- Do not over-fetch or serialize unnecessary data into client components.

### Server Actions and API Routes

- Authenticate and authorize every mutating operation.
- Validate request payloads with Zod (or equivalent schema).
- Return consistent typed error shapes.
- Enforce idempotency for retried mutations where applicable.

## React Quality Standards

- No unnecessary global state; prefer local state + URL state.
- Avoid broad context subscriptions that trigger avoidable rerenders.
- Keep expensive computation out of render hot paths.
- Prefer composition over boolean-prop branching APIs.

## Accessibility and UX

Minimum bar:
- Semantic elements for interaction (`button`, `a`, `label`).
- Icon-only controls require `aria-label`.
- Focus-visible styles present and obvious.
- Forms have labels, inline errors, and keyboard usability.
- Respect `prefers-reduced-motion`.

## Performance Standards (Vercel-oriented)

- Use `next/image` with explicit dimensions.
- Use dynamic imports for heavy client-only modules.
- Keep third-party scripts non-blocking.
- Prevent hydration mismatches (date/time, random values, browser-only state).
- Avoid duplicate fetching and duplicate serialization to client.

## Security Standards

- Never expose secrets in client bundles.
- Use server-side checks for entitlements and role access.
- Sanitize error responses; avoid leaking internals.
- Use secure cookie/session handling patterns.

## Testing and Verification

Before completion, run available gates:
```bash
npm run lint --if-present
npm run typecheck --if-present
npm run test --if-present
npm run build --if-present
```

For critical paths, add or update:
- integration tests for data/auth flows
- UI tests for key user interactions

## Review Checklist

Flag issues when confidence is high and impact is clear:
- auth/permission bypass
- input validation gaps
- data consistency bugs
- unnecessary client bundle growth
- accessibility regressions
- missing tests for changed behavior
