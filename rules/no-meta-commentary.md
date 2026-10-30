---
description: Prevent meta-commentary in code and documentation - focus on what developers need to know
alwaysApply: true
---

# No Meta-Commentary

## Principle: Focus on User Value, Not Creation History

**Documentation and code should focus on what developers need to know, not the history of how files came to be.**

## ❌ Forbidden Meta-Commentary Patterns

### Status Announcements
```markdown
❌ BAD: Meta-commentary about changes
> **✅ ABSTRACTION SUCCESS**: All direct usage has been abstracted
> **🎉 MIGRATION COMPLETE**: Updated to new patterns  
> **✅ FIXED**: Resolved the issue with X
> **📝 UPDATED**: Changed approach based on feedback
> **🔧 REVISED**: Updated based on codebase reality

❌ BAD: Status badges in content
- **Status**: ✅ Created and implemented
- **Updated**: Fixed rule to match codebase reality
```

### Creation History Comments  
```typescript
// ❌ BAD: Creation/modification history
// Added by [person] on [date] to fix the environment issue
// Updated after discovering the abstraction pattern worked better
// This function was created following the new guidelines

// ❌ BAD: Change justification in comments
// Changed from process.env to getEnvVar() abstraction
// Refactored based on code review feedback
```

### Implementation Success Commentary
```markdown
❌ BAD: Commentary about implementation success
"This successfully replaces the old pattern"
"After implementing this change, the tests pass"
"Following this pattern resolved the original issue"
```

## ✅ Correct: Focus on User Value

### Clear, Forward-Looking Guidance
```markdown
✅ GOOD: Direct guidance without meta-commentary
## Environment Variable Access

**ALWAYS use the `@/utils/env` abstraction:**

```typescript
import { getEnvVar, isDevMode } from '@/utils/env'
```

**Reason:** Provides testable, centralized environment access.
```

### Purpose-Driven Comments
```typescript
// ✅ GOOD: Explains purpose and usage
/**
 * Gets environment variables with fallback handling
 * @param key - Environment variable key
 * @returns Value or undefined if not set
 */
export const getEnvVar = (key: string): string | undefined => {
  return import.meta.env[key]
}

// ✅ GOOD: Explains why, not when/who
// Centralized to enable consistent mocking in tests
const mockableEnvAccess = () => { ... }
```

## Guidelines for Content Creation

### 1. Write for Future Consumers
- **Ask**: "What does a new developer need to know?"
- **Not**: "How did this come to exist?"

### 2. Document Intent, Not History
```markdown
✅ GOOD: Intent-focused
"Use abstraction for testability and consistency"

❌ BAD: History-focused  
"Updated to use abstraction after discovering testing issues"
```

### 3. Remove Implementation Timeline
```markdown
✅ GOOD: Direct instruction
"Configure Jest with these settings:"

❌ BAD: Timeline commentary
"After implementing these Jest changes, the tests work:"
```

### 4. Focus on "What" and "Why", Not "When"
```typescript
// ✅ GOOD: What and why
/**
 * Validates user input using Zod schema
 * Prevents injection attacks and ensures data integrity
 */
const validateInput = (data: unknown) => { ... }

// ❌ BAD: When and who
/**
 * Added validation after security review
 * Updated by team to fix vulnerability found in testing
 */
```

## Special Cases: When Context Is Valuable

### Architecture Decision Records (ADRs)
```markdown
✅ ACCEPTABLE: In dedicated ADR files only
# ADR-001: Environment Variable Abstraction

## Status: Accepted

## Context: [Historical context for decision]
## Decision: [What we decided]  
## Consequences: [Impact of decision]
```

### Migration Guides
```markdown
✅ ACCEPTABLE: In migration documentation only
# Migration Guide: Old Pattern → New Pattern

## Before (deprecated):
```old code```

## After (current):
```new code```

## Reason: [Why the change was needed]
```

### Changelog Files
```markdown
✅ ACCEPTABLE: In CHANGELOG.md only
## [1.2.0] - 2023-12-01
### Changed
- Environment variable access now uses @/utils/env abstraction
```

## Enforcement

### Code Review Checklist
- [ ] Does documentation focus on user needs?
- [ ] Are comments about purpose, not history?
- [ ] Is meta-commentary removed from rules/docs?
- [ ] Would a new team member understand without context?

### File Review Questions
1. **"If I removed all history, would this still be useful?"**
2. **"Does this explain what to do, not what was done?"**
3. **"Would a new developer find value without knowing the backstory?"**

## Summary

**Write for the future developer who needs to understand and use the code, not for documenting the journey of how it came to be.**

- ✅ **Focus**: What developers need to know
- ✅ **Value**: Clear guidance and purpose  
- ✅ **Clarity**: Direct instructions without backstory
- ❌ **Avoid**: Change history, implementation success stories, creation commentary