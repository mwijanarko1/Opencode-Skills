# Debug

1. 5–7 hypotheses (data flow, API, UI, env, timing, deps, config) → prioritize top 2
2. Add logs: `[DEBUG]` at entry, transforms, state, API req/res
3. Collect: browser console, network, server logs
4. Analyze: timeline, state at failure, data flow, root cause
5. Fix + verify. Remove logs after.

## Output

Hypotheses (initial + prioritized), evidence, analysis, fix, verification.
