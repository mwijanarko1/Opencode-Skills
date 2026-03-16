# Review

1. **Ask the user**: "Full codebase review or diff from latest commit?" If not specified, ask before proceeding.
2. **Load the applicable skill stack** from [AGENTS.md](../AGENTS.md). Start with the foundation stack: `ai-interaction-workflow`, `coding-standards`, `testing-strategies`. Add `security-vulnerability-mitigation` for auth, input handling, networking, persistence, secrets, or user data. Add the relevant domain skills: `frontend-web-development`, `backend-architecture`, `ios-development`, `vercel-composition-patterns`, `vercel-react-best-practices`, `vercel-react-native-skills`, `web-design-guidelines`, `website-compliance`, `technical-seo`, `expo-docs`. Use `cartographer` first if the codebase map is missing or stale.
3. **Get scope**:
   - **Diff only**: `git diff HEAD~1` or `git diff HEAD~1..HEAD`
   - **Full codebase**: Review all relevant files (e.g. `git ls-files` or project structure)
4. Read full files for complex/security-sensitive changes
5. Context: `git log --oneline -10 -- path`, `git blame`
6. Flag only 75%+ confidence. Skip style, naming, existing patterns.
7. **Review against loaded skills**: For each applicable skill, check the diff for violations of that skill's guidelines. Include skill-specific findings in the output.

## Confidence

| Level | Threshold | Examples |
|-------|-----------|----------|
| CRITICAL | 95%+ | Injection, auth bypass, data loss |
| WARNING | 85%+ | Bugs, logic errors, perf, unhandled errors |
| SUGGESTION | 75%+ | Quality, best practices |

## Focus

Apply all loaded skills. Base focus: Security (injection, auth, data exposure, validation). Bugs (null/race/edge cases). Perf (N+1, leaks, re-renders). Errors (try-catch, promise rejections). Plus skill-specific checks: API design, schema, testing, UI/UX, accessibility, compliance, composition patterns, React/RN best practices, etc.

## Output

Summary (2–3 sentences). Table: Severity | File:Line | Issue. Per-issue: Problem + Suggestion (before/after). Recommendation: APPROVE | APPROVE WITH SUGGESTIONS | NEEDS CHANGES | NEEDS DISCUSSION.
