---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance using local pinned rules. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
metadata:
  author: local
  version: "1.0.1"
  argument-hint: <file-or-pattern>
---

# Web Interface Guidelines (Pinned Local)

Review files for compliance with local pinned Web Interface Guidelines.

## How It Works

1. Read only user-specified files or files changed in the active diff
2. Apply the local rules below
3. Output findings in terse `file:line` format

## Scope Guardrails

- Only review files in the current workspace/repository.
- Default scope: changed files from git diff.
- If no changed files are available, ask the user which files or patterns to review.
- Never scan user home directories or system temp/private paths unless explicitly requested by the user.

## Rules

### Accessibility
- Icon-only buttons need aria-label
- Form controls need labels
- Interactive elements need keyboard handlers
- Use semantic HTML (`<button>`, `<a>`, not `<div onClick>`)
- Images need alt text
- Headings must be hierarchical (`<h1>` through `<h6>`)

### Focus States
- Visible focus on all interactive elements
- Use `:focus-visible`
- Never use `outline: none` without a clear replacement

### Forms
- Use proper autocomplete and input types
- Never block paste (`onPaste` with `preventDefault`)
- Labels must be clickable and associated with controls
- Errors should appear inline near fields

### Animation
- Respect `prefers-reduced-motion`
- Animate transform/opacity only
- Never use `transition: all`

### Content and Typography
- Prefer the ellipsis character (`…`) over `...` where style guide requires
- Avoid truncation that hides critical meaning
- Handle empty states intentionally

### Images
- Provide explicit width/height to reduce layout shift
- Lazy-load below-the-fold images

## Usage

When a user provides a file or pattern argument:
1. Read the specified files
2. Apply all local rules
3. Output findings in `file:line` format

If no files are specified, ask which files to review.
