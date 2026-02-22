---
name: ios-development
description: Senior mobile standards for Swift iOS, React Native, and Expo.
---

# iOS / Mobile Development (Senior)

Use this skill for native Swift iOS, React Native, and Expo projects.

## Core Defaults

1. Prefer correctness and predictability over clever abstractions.
2. Keep architecture explicit and testable (DI over hidden globals).
3. Enforce strict async boundaries and thread safety.
4. Keep mobile UX responsive and crash-resistant.

## Native iOS (Swift)

### Architecture
- Feature-first modules; avoid monolithic MVC files.
- MVVM is the default for app features.
- Inject services via protocols; avoid global singletons for app logic.

### Concurrency and State
- Use `async/await` for one-shot async work.
- Use `actor` or safe isolation for shared mutable state.
- Mark UI state updates with `@MainActor`.
- Avoid force unwraps in production paths.

### SwiftUI Standards
- Keep views small and composable.
- Use `#Preview` macro for previews.
- Use the correct property wrapper for ownership (`@State`, `@Binding`, `@Environment`).
- Move complex state transitions to view models/services.

### Security
- Store credentials/tokens in Keychain, never `UserDefaults`.
- Avoid logging sensitive data in release paths.
- Validate deeplink inputs and external payloads.

## React Native / Expo

### Rendering and Safety
- Never use falsy `&&` patterns that can render `0`/`""` unexpectedly.
- Wrap all strings in `Text` components.
- Prefer `Pressable` and native-feeling interactions.

### Lists and Performance
- Use FlashList/LegendList for medium/large lists.
- Memoize list items and stabilize callbacks.
- Avoid expensive inline allocations inside render loops.

### Animation and Gestures
- Animate transform/opacity for smooth performance.
- Use Reanimated shared/derived values for high-frequency updates.
- Avoid pushing gesture/animation state through React state when not needed.

### Expo and Native Integration
- Keep config plugins aligned with actual native capabilities.
- Run `expo-doctor` and address warnings relevant to production.
- Verify permissions and Info.plist/Android manifest entries for used features.

## Testing and Verification

### Swift
- Prefer unit tests on view models/services.
- Add integration/UI tests for critical flows.

### RN/Expo
- Add tests for data and navigation-critical flows.
- Verify build/export paths before release.

Suggested commands when available:
```bash
npm run lint --if-present
npm run typecheck --if-present
npm run test --if-present
npx expo-doctor
npx expo export --platform all
```

## Review Checklist

Flag high-confidence issues first:
- crash risks (force unwraps, invalid casts, unsafe threading)
- auth/session/secret handling issues
- list/animation performance regressions
- platform permission or config mismatches
- missing tests around changed behavior
