# Web Interface Guidelines

Review $ARGUMENTS. Terse output—`file:line` format, high signal.

## Rules

**A11y:** Icon buttons `aria-label`. Form controls `<label>`/`aria-label`. Keyboard handlers. `<button>`/`<a>` not `<div onClick>`. Images `alt`. Decorative `aria-hidden`. Async updates `aria-live`. Semantic HTML first. Headings hierarchical; skip link. `scroll-margin-top` on anchors.

**Focus:** Visible focus (`focus-visible:ring-*`). Never `outline-none` without replacement. `:focus-visible` over `:focus`. `:focus-within` for compound controls.

**Forms:** `autocomplete`, `name`, correct `type`/`inputmode`. No paste block. Labels clickable. `spellCheck={false}` on email/code. Checkbox/radio: single hit target. Submit enabled until request; spinner during. Errors inline; focus first error. Placeholders end `…`. `autocomplete="off"` on non-auth. Warn on unsaved nav.

**Animation:** `prefers-reduced-motion`. Animate `transform`/`opacity` only. Never `transition: all`. Correct `transform-origin`. SVG: `<g>` with `transform-box: fill-box`. Interruptible.

**Typography:** `…` not `...`. Curly quotes. `&nbsp;` for units, shortcuts. Loading `…`. `tabular-nums` for numbers. `text-wrap: balance` on headings.

**Content:** `truncate`/`line-clamp`/`break-words`. Flex children `min-w-0`. Empty states. Handle long UGC.

**Images:** `width`/`height`. Below-fold `loading="lazy"`. Above-fold `priority`/`fetchpriority="high"`.

**Perf:** Lists >50: virtualize. No layout reads in render. Batch DOM. Uncontrolled inputs preferred. `preconnect`, `preload` fonts.

**Nav:** URL reflects state. `<a>`/`<Link>`. Deep-link state. Destructive = confirm/undo.

**Touch:** `touch-action: manipulation`. `overscroll-behavior: contain` in modals. During drag: no text select, `inert`.

**Layout:** `env(safe-area-inset-*)` for full-bleed. Flex/grid over JS measurement.

**Dark:** `color-scheme: dark`, `theme-color`, native select colors.

**i18n:** `Intl.DateTimeFormat`, `Intl.NumberFormat`. `Accept-Language` not IP.

**Hydration:** `value` needs `onChange`. Guard date/time. `suppressHydrationWarning` sparingly.

**Copy:** Active voice, Title Case, numerals, specific labels, errors with fix, second person.

**Anti-patterns:** `user-scalable=no`, paste block, `transition: all`, `outline-none` no replacement, `onClick` nav, `<div>` click, images no dimensions, large `.map()` no virtualize, inputs no labels, icons no aria-label, hardcoded formats, `autoFocus` unjustified.

## Output

Group by file. `file:line - issue`. `✓ pass` if clean. No preamble.
