---
name: debug
version: 1.0.0
description: |
  Systematic debugging workflow for identifying, diagnosing, and resolving
  software issues. Uses structured hypothesis testing, logging, and root cause
  analysis to fix bugs efficiently.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
---

# Debug: Systematic Issue Resolution

Diagnose and fix software bugs through structured investigation. This approach
prioritizes understanding the problem over quick fixes that might mask symptoms.

## Your Task

When debugging an issue:

1. **Hypothesize widely** - Consider 5-7 possible causes before narrowing down
2. **Focus on likely culprits** - Distill to 1-2 most probable sources
3. **Add diagnostic logs** - Instrument code to validate assumptions
4. **Collect evidence** - Gather logs from browser, network, and server
5. **Analyze deeply** - Reflect on the data and produce comprehensive analysis
6. **Iterate if needed** - Add more logs if root cause remains unclear
7. **Clean up** - Remove diagnostic logs after fix is verified

---

## Debugging Process

### 1. Generate Hypotheses

Start broad. List 5-7 potential causes without filtering:

**Common categories:**
- **Data flow issues:** Incorrect data transformation, race conditions, state mismatches
- **API problems:** Wrong endpoints, payload errors, authentication failures
- **UI/rendering bugs:** Component lifecycle issues, prop drilling failures, CSS conflicts
- **Environment differences:** Dev vs. production, missing env vars, platform-specific bugs
- **Timing/async issues:** Promises not awaited, timeouts, event ordering
- **External dependencies:** Third-party library changes, CDN failures, service outages
- **Configuration errors:** Wrong build settings, feature flags, routing issues

**Example hypotheses:**
1. The API response format changed and parsing fails
2. State update happens after component unmounts
3. Race condition between two async operations
4. Missing error handling for edge case input
5. Environment variable not set in production
6. Third-party library version mismatch
7. Browser-specific behavior (e.g., Safari date parsing)

### 2. Prioritize Likely Causes

Rank hypotheses by probability based on:
- Recent changes (git log, last deploy)
- Error messages and stack traces
- Frequency and reproducibility
- Similar past issues

**Distill to top 2:**
- Most likely: Data parsing error after API change
- Second most likely: Race condition in async initialization

### 3. Add Diagnostic Logs

Instrument code to track data transformations:

**What to log:**
- Input values at function entry points
- Intermediate transformation results
- State changes
- API request/response payloads
- Error objects with full context

**Example logging pattern:**
```javascript
console.log('[DEBUG] Function: processUserData');
console.log('[DEBUG] Input:', JSON.stringify(userData, null, 2));
console.log('[DEBUG] After transform:', JSON.stringify(transformed, null, 2));
console.log('[DEBUG] State before set:', JSON.stringify(currentState, null, 2));
```

**Browser-specific logs:**
```javascript
// Network debugging
console.log('[DEBUG] Request:', { url, method, headers, body });
console.log('[DEBUG] Response:', { status, data, error });

// Performance debugging
console.time('[DEBUG] Operation duration');
await heavyOperation();
console.timeEnd('[DEBUG] Operation duration');
```

### 4. Collect Logs

Gather evidence from all relevant sources:

**Browser console:**
- Run browser automation to capture console logs
- Filter by log level (error, warn, info, debug)
- Look for patterns in timing and sequence

**Network logs:**
- Check request/response payloads
- Verify status codes and headers
- Look for failed or slow requests

**Server logs:**
- Application logs (error, info, debug levels)
- Infrastructure logs (load balancer, database)
- Request tracing (correlation IDs)

**Ask user if needed:**
```
Can you share the server logs from the last error occurrence?
Or run: tail -f /var/log/app.log | grep ERROR
```

### 5. Analyze and Fix

Deeply reflect on collected data:

**Analysis framework:**
1. **Timeline reconstruction:** What happened in what order?
2. **State inspection:** What was the application state at failure point?
3. **Data flow tracing:** How did data transform from source to sink?
4. **Edge case identification:** What input triggered the failure?
5. **Root cause identification:** What's the fundamental issue?

**Produce findings:**
- Root cause explanation
- Why previous code failed
- Fix implementation
- Verification that fix resolves issue

### 6. Iterate if Unclear

If root cause remains uncertain:

- Add more targeted logs at suspected failure points
- Create minimal reproduction case
- Check similar issues in issue trackers
- Review recent commits for changes
- Test hypotheses in isolation

### 7. Clean Up

After fix is verified:

```
The issue is resolved. Should I remove the diagnostic logs I added?
```

**Remove:**
- All `[DEBUG]` console.log statements
- Temporary error handling
- Debug flags or verbose modes

**Keep:**
- Permanent error logging for monitoring
- Performance metrics if valuable
- Comments explaining the fix

---

## Common Debugging Patterns

### Pattern: Data Flow Tracing

Track how data changes through the system:

```javascript
// Before
function processData(data) {
  return transform(save(data));
}

// Debug version
function processData(data) {
  console.log('[DEBUG] Input:', data);
  const transformed = transform(data);
  console.log('[DEBUG] Transformed:', transformed);
  const saved = save(transformed);
  console.log('[DEBUG] Saved:', saved);
  return saved;
}
```

### Pattern: Race Condition Detection

Log timing and sequence:

```javascript
let operationCount = 0;

async function asyncOperation() {
  const id = ++operationCount;
  console.log(`[DEBUG] Operation ${id} started`);
  const result = await fetchData();
  console.log(`[DEBUG] Operation ${id} completed:`, result);
  return result;
}
```

### Pattern: Error Context

Capture full error context:

```javascript
try {
  await riskyOperation();
} catch (error) {
  console.error('[DEBUG] Error caught:', {
    message: error.message,
    stack: error.stack,
    context: { userId, operation, timestamp: Date.now() }
  });
  throw error;
}
```

---

## Output Format

Provide:

1. **Hypotheses:** List of considered causes (5-7 initially, 1-2 prioritized)
2. **Evidence:** Key log entries and observations
3. **Analysis:** Root cause explanation
4. **Fix:** Code changes made
5. **Verification:** Proof issue is resolved

---

## Full Example

**Scenario:** User reports app crashes when loading dashboard

```
**Hypotheses:**
1. API response format changed causing parsing error
2. Race condition between user data and preferences loading
3. Memory leak from unclosed event listeners
4. Null reference when user has no preferences set
5. Large dataset causing render timeout
6. Third-party chart library compatibility issue

**Prioritized:**
Most likely: #1 (API format change) - deployed new API yesterday
Second: #4 (null preferences) - happens for new users

**Evidence gathered:**
- Console shows "Cannot read property 'map' of undefined"
- API response missing 'preferences' field for new users
- Error occurs at Dashboard.tsx:42

**Analysis:**
The API no longer returns empty preferences array for new users;
it omits the field entirely. Dashboard component expects array
and calls .map() without null check.

**Fix:**
Added null check: preferences?.map(...) || []

**Verification:**
Tested with new user account - dashboard loads correctly.
All diagnostic logs removed.
```

---

## Reference

- Debugging methodology: https://en.wikipedia.org/wiki/Debugging
- Chrome DevTools: https://developer.chrome.com/docs/devtools/
- Systematic debugging: "Why Programs Fail" by Andreas Zeller
