# Instructions for Cursor Agents

## Available Skills

- **[ai-interaction-workflow](./skills/ai-interaction-workflow/SKILL.md)**: AI behavior, protocols, and version control.
- **[coding-standards](./skills/coding-standards/SKILL.md)**: Universal engineering standards for code quality.
- **[security-vulnerability-mitigation](./skills/security-vulnerability-mitigation/SKILL.md)**: Security guidelines and OWASP mitigation.
- **[testing-strategies](./skills/testing-strategies/SKILL.md)**: Testing philosophy and implementation.
- **[frontend-web-development](./skills/frontend-web-development/SKILL.md)**: Web & Frontend stack guidelines.
- **[backend-architecture](./skills/backend-architecture/SKILL.md)**: Backend design, API design, and database schema.
- **[ios-development](./skills/ios-development/SKILL.md)**: Swift development.
- **[cartographer](./skills/cartographer/SKILL.md)**: Codebase mapping and architecture documentation.
- **[vercel-composition-patterns](./skills/vercel-composition-patterns/SKILL.md)**: Scalable React composition patterns and compound components.
- **[vercel-react-best-practices](./skills/vercel-react-best-practices/SKILL.md)**: React/Next.js performance optimization guidelines from Vercel.
- **[vercel-react-native-skills](./skills/vercel-react-native-skills/SKILL.md)**: Best practices for building performant React Native and Expo apps.
- **[web-design-guidelines](./skills/web-design-guidelines/SKILL.md)**: Comprehensive UI/UX and accessibility auditing guidelines.
- **[website-compliance](./skills/website-compliance/SKILL.md)**: Global website legal compliance (GDPR, CCPA, WCAG, e-commerce regulations).
- **[ios-app-store-compliance](./skills/ios-app-store-compliance/SKILL.md)**: Pre-submission compliance scanner for Apple App Store (iOS, macOS, tvOS, watchOS, visionOS).

---

## Operational Protocols

### Codebase Awareness
When starting work in any project, you MUST check for the presence of a `docs/CODEBASE_MAP.md` (or `CODEBASE_MAP.md`).
- **If missing**: proactively use the **`cartographer`** skill to generate a comprehensive map of the codebase.
- **If present**: review it to understand the architecture, data flow, and navigation before making changes.

---

## Available Subagents

The following subagents are available in `~/.config/opencode/agents/` and can be invoked via the Task tool or @mention:

### Core Subagents

- **@ai-interaction-workflow**: AI behavior, operational protocols, output formats, and version control guidelines
- **@coding-standards**: Universal engineering standards for naming, code style, documentation, and modularity
- **@security-auditor**: Security guidelines including input validation, encryption, and OWASP mitigation
- **@testing-strategies**: Testing philosophy and implementation for Unit, Integration, and E2E testing
- **@backend-architecture**: Backend design patterns, API design, database schemas, auth, and observability
- **@frontend-web-development**: Next.js setup, UI/UX principles, A11y, performance, and best practices
- **@ios-development**: Mobile app development standards for Swift (iOS) and React Native/Expo
- **@cartographer**: Maps and documents codebases by orchestrating parallel subagents

### Specialized Subagents

- **@react-composition-patterns**: React composition patterns that scale (compound components, render props, context)
- **@react-best-practices**: React and Next.js performance optimization from Vercel Engineering
- **@react-native-skills**: React Native and Expo best practices for performant mobile apps
- **@web-design-guidelines**: UI code review for Web Interface Guidelines compliance
- **@website-compliance**: Global website legal compliance (GDPR, CCPA, WCAG, e-commerce regulations)
- **@ios-app-store-compliance**: Pre-submission App Store compliance checks (greenlight scans, rejection-risk fixes)

---

## Subagent Management Protocol

As the primary agent, you act as a manager and orchestrator to the subagents:

### When to Delegate

Delegate to subagents when:
- The task requires specialized knowledge (security, testing, accessibility, etc.)
- You need to verify code against specific standards or guidelines
- The task can be parallelized across multiple domains
- Deep expertise in a specific area is required

### How to Delegate

Use the **Task tool** with `subagent_type: "general"` to invoke subagents:

```
Task: "Analyze this code for security vulnerabilities"
subagent_type: "general"
Prompt: "@security-auditor review the following files for security issues:
- src/api/auth.ts
- src/lib/db.ts

Check for:
1. Input validation with Zod
2. OWASP Top 10 vulnerabilities
3. Proper auth checks
4. Data encryption patterns

Return findings in file:line format."
```

### Parallel Delegation

For multi-domain tasks, spawn subagents in parallel:

```
Task 1: "@frontend-web-development review accessibility"
Task 2: "@react-best-practices check for performance issues"
Task 3: "@coding-standards verify naming and TypeScript"
```

### Subagent Workflow

Each subagent will:
1. Read their corresponding SKILL.md file for authoritative guidelines
2. Analyze the provided code/files against those guidelines
3. Return findings in the appropriate format (usually file:line)
4. Provide specific recommendations with code examples

### Manager Responsibilities

When managing subagents:
1. **Route appropriately**: Match the task to the right subagent based on their specialization
2. **Provide context**: Give subagents the files/patterns they need to analyze
3. **Synthesize results**: Combine findings from multiple subagents into coherent recommendations
4. **Coordinate updates**: When multiple subagents suggest changes, coordinate the order of operations
5. **Final review**: Validate that subagent recommendations align with the overall project goals

---
# Workflow Orchestration

### 1. Plan Mode Default

- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately - don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy

- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

### 3. Self-Improvement Loop

- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done

- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)

- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes - don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing

- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests - then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

## Task Management

1. **Plan First**: Write plan to `tasks/todo.md` with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review section to `tasks/todo.md`
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.

## Configuration Quality Gates

Before considering config changes complete, run:

```bash
npm run lint:config
npm run eval:smoke
```

Guardrails:
- Keep review logic local and deterministic; do not require remote prompt fetching.
- Keep agent-to-skill references valid and in-repo.
- Never store plaintext secrets in config files; use `{env:...}` placeholders.
___

Refer to the individual `AGENTS.md` and `SKILL.md` files in the `skills` directory for detailed guidelines. You can load these skills on-demand using the `skill` tool.
