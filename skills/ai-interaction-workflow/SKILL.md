---
name: ai-interaction-workflow
description: Guidelines for AI behavior, operational protocols, output formats, and version control.
---

# AI Interaction & Workflow

## AI Behavior & Vibe Coding Safeguards

### Business Logic & "Math"
- **Server-Side Calculation:** NEVER calculate financial data, prices, scores, or permissions on the client.
  - Bad: `const total = cart.reduce((a, b) => a + b.price, 0)` in a React component.
  - Good: Send product IDs to the server; server calculates total based on DB prices.
- **Trustless Client:** Assume the client code has been modified by the user. Do not rely on `disabled={true}` or hidden UI elements to prevent actions.

### Premium & Feature Gating
- **Withhold, Don't Hide:** Do not just hide "Premium" buttons or routes. The API/Server Action must strictly return a `403 Forbidden` or empty data if the user lacks the specific entitlement.
- **Verification:** Never trust a client-side boolean (e.g., `user.isPremium`) for sensitive operations. Re-verify subscription status on the server immediately before delivering content or performing an action.

### Database Access (Anti-Pattern)
- **No Direct Client-to-DB:** Even if using Supabase/Firebase, DO NOT write data directly from the frontend using client SDKs in `useEffect` or event handlers.
- **Middleware Requirement:** Always route data mutations through a "Middleware" layer (Next.js API Routes, Server Actions, or Edge Functions) to ensure validation and rate limiting run in a trusted environment.

### Operational Protocols
- **Manual Trigger Strategy:** Do not run `npm run dev` or `npm start`. Wait for specific user instructions before starting any server.
- **Permission Protocol:** Ask for consent before running any command in the terminal.
- **Process Management:** Avoid starting long-running or background processes. Keep the terminal available for the user.

## Output Format (for Code Reviews/Audits)

Group findings by file. Use `file:line` format (VS Code clickable). Terse findings.

```text
## src/Button.tsx

src/Button.tsx:42 - icon button missing aria-label
src/Button.tsx:18 - input lacks label
src/Button.tsx:55 - animation missing prefers-reduced-motion
src/Button.tsx:67 - transition: all → list properties

## src/Modal.tsx

src/Modal.tsx:12 - missing overscroll-behavior: contain
src/Modal.tsx:34 - "..." → "…"
```

## Version Control Guidelines

### Branching Strategy
- **Flow:** Adopt **GitHub Flow** (Trunk-Based Development).
  - `main`: Production-ready state. Deployable at any time.
  - `feature/`: New features (e.g., `feature/auth-login`).
  - `fix/`: Bug fixes (e.g., `fix/header-alignment`).
  - `chore/`: Maintenance, config, dependency updates.
- **Naming:**
  - Use lowercase kebab-case.
  - Format: `type/short-description`.
  - Example: `feature/user-profile`, `fix/login-timeout`.

### Commit Convention
- **Standard:** Follow **Conventional Commits** (`type(scope): subject`).
- **Types:**
  - `feat`: A new feature.
  - `fix`: A bug fix.
  - `docs`: Documentation only changes.
  - `style`: Formatting, missing semi-colons (no code change).
  - `refactor`: A code change that neither fixes a bug nor adds a feature.
  - `test`: Adding missing tests or correcting existing tests.
  - `chore`: Changes to the build process or auxiliary tools.
- **Subject:**
  - Imperative mood ("Add" not "Added").
  - No capitalization of first letter.
  - No period at the end.
  - **Example:** `feat(auth): implement google oauth provider`

### Pull Requests (PRs)
- **Scope:** Limit PRs to a single logical change or feature. Large PRs (>400 lines) should be split.
- **Description:** Must answer:
  1.  **What** changed?
  2.  **Why** (context/ticket link)?
  3.  **How** to test?
- **Merge Strategy:** Use **Squash and Merge**.
  - Keeps the `main` history clean and linear.
  - Combines WIP commits into a single semantic commit.

### Workflow Rules
- **Never Push to Main:** Direct pushes to `main` are blocked. All changes require a PR.
- **Syncing:** Pull `main` into your feature branch frequently (`git pull origin main`) to resolve conflicts early, not at the end.
- **Secrets:** NEVER commit `.env` files, API keys, or credentials. Use `.gitignore`.
- **Cleanup:** Delete feature branches immediately after merging.
