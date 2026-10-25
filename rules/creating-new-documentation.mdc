---
description: this is used to create new arch docs in the /docs/tech/architecture folder. These docs are there to get new development to use the right patterns.
alwaysApply: false
---
# Creating New Documentation Process

This process enables automatic creation of properly formatted architecture and troubleshooting documentation that integrates seamlessly with the existing documentation system.

## When to Use This Process

**Architecture Documentation**: Proactive guidance for building new features and understanding system design.
- Building new functionality
- Learning system architecture  
- Following established patterns
- Understanding core components and integration patterns

**Troubleshooting Documentation**: Reactive solutions to common development problems and errors.
- Encountering errors or debugging issues
- Solving specific problems
- Resolving configuration issues
- Finding solutions to error messages

## Step 1: Determine Documentation Type

**Choose Documentation Type:**

### Architecture Documentation (`docs/tech/architecture/`)
Use for:
- ✅ **Proactive guidance** - "How should I build this?"
- ✅ **Design patterns** - "What's the recommended approach?"
- ✅ **System understanding** - "How does this work?"
- ✅ **Implementation guidance** - "What should I follow?"
- ✅ Consumer-focused content - How to build WITH the architecture

### Troubleshooting Documentation (`docs/tech/troubleshooting/`)
Use for:
- 🔧 **Reactive problem solving** - "This is broken, how do I fix it?"
- 🔧 **Error resolution** - "I got this error message"
- 🔧 **Debugging guidance** - "Something isn't working"
- 🔧 **Configuration issues** - "My setup is broken"

## Step 2: Create Architecture Documentation

### Architecture File Naming Convention
**Pattern**: `{system}-{pattern}-{purpose}.md`

**Examples**:
- `api-response-patterns.md` - API response architecture
- `error-handling-infrastructure.md` - Error handling system design
- `health-monitoring-architecture.md` - Health check system
- `authentication-flow-design.md` - Auth system architecture
- `database-connection-patterns.md` - Database layer design

### Architecture File Creation Process
1. **Create file with proper naming**:
   ```bash
   touch docs/tech/architecture/{system}-{pattern}-{purpose}.md
   ```

2. **Add required metadata block at top**:
   ```html
   <!--
   KEYWORDS: system, pattern, technology, concept, use-case
   CATEGORY: infrastructure|patterns|design|integration
   COMPLEXITY: simple|moderate|complex
   AUDIENCE: developer|architect|team-lead
   LAST_UPDATED: YYYY-MM-DD
   -->
   ```

3. **Follow architecture content structure**:
   - **System-focused title**: What architecture does this document?
   - **Start with problems**: Identify specific problems developers face
   - **Clear principles**: Why was it designed this way?
   - **Working code examples**: From actual codebase implementation
   - **Integration patterns**: How components work together
   - **Consumer-focused implementation guide**: Step-by-step usage

### Architecture Content Standards

**✅ Include (Consumer-Focused)**:
- How to use components and patterns
- What methods/interfaces to call
- Step-by-step implementation guides
- Integration patterns and examples
- When to use different approaches

**❌ Exclude (Internal Details)**:
- Internal implementation details
- Private methods or internal state
- Complex algorithmic explanations
- Technical details not exposed in the public API

**Architecture Example Structure**:
```markdown
# {System} {Pattern} Architecture

<!--
KEYWORDS: api, response, error-handling, infrastructure, patterns
CATEGORY: infrastructure
COMPLEXITY: moderate
AUDIENCE: developer
LAST_UPDATED: 2025-01-20
-->

## Common {Problem Domain} Scenarios

### Scenario 1: {Specific Problem}
**Problem**: {What pain point developers experience}
**Current Pain**: {What goes wrong without the solution}

## Why {Your Solution} Solves This
{Explain why your architecture addresses these specific problems}

## Integration Patterns
```typescript
// Frontend usage
import { HealthResponse } from '@shared/health'
const health = await fetch('/api/health').json() as HealthResponse

// Backend implementation  
import { HealthResponse } from '@shared/health'
router.get('/health', async (req, res: Response<HealthResponse>) => {
  // Implementation
})
```

## Implementation Guide
1. {Step-by-step usage instructions}
2. {Integration requirements}
3. {Example implementations}
```

## Step 3: Create Troubleshooting Documentation

### Troubleshooting File Naming Convention
**Pattern**: `{topic}-{technology}-{purpose}.md`

**Examples**:
- `testing-drizzle-orm-issues.md` - Testing patterns for Drizzle ORM
- `monorepo-typescript-jest-config-errors.md` - TypeScript/Jest configuration
- `deployment-docker-production-issues.md` - Production Docker deployment
- `module-resolution-path-mapping-errors.md` - Path mapping issues

### Troubleshooting File Creation Process
1. **Create file with proper naming**:
   ```bash
   touch docs/tech/troubleshooting/{topic}-{technology}-{purpose}.md
   ```

2. **Add required metadata block**:
   ```html
   <!--
   KEYWORDS: primary, secondary, technology, use-case
   ISSUES: "specific error message", "problem description"
   RELATED: other topics, cross-references
   DIFFICULTY: beginner|intermediate|advanced
   LAST_UPDATED: YYYY-MM-DD
   -->
   ```

3. **Follow troubleshooting content structure**:
   - **Problem-focused title**: What does this solve?
   - **Clear introduction**: When to use this guide
   - **Exact error messages**: Include verbatim error text
   - **Working code examples**: From actual codebase
   - **Step-by-step solutions**: Tested fixes that work
   - **Common issues section**: Multiple error scenarios + solutions

### Troubleshooting Content Standards

**Error Documentation Requirements**:
- **Exact error messages in quotes**: `"Cannot find module '@shared'"`
- **Complete error context**: Full stack trace when relevant
- **Exact solutions**: Working code that fixes the issue
- **Tested examples**: Real implementations from this codebase

**Troubleshooting Example Structure**:
```markdown
# {Topic} {Technology} Issues

<!--
KEYWORDS: testing, drizzle, orm, database, mocking
ISSUES: "Cannot find module '@shared'", "Jest module resolution errors"
RELATED: path mapping, monorepo configuration, testing setup
DIFFICULTY: intermediate
LAST_UPDATED: 2025-01-20
-->

## When to Use This Guide
{Description of when developers encounter these issues}

## Common Error Scenarios

### Error 1: Module Resolution
```
Error: Cannot find module '@shared/health'
  at Object.<anonymous> (src/routes/health.test.ts:7:31)
```

**Solution**:
```javascript
// Fix: Update Jest moduleNameMapping
moduleNameMapping: {
  '^@shared/(.*)$': '<rootDir>/../shared/src/$1',
}
```

### Error 2: {Another Common Issue}
{Exact error message}
{Step-by-step solution}
```

## Step 4: Metadata Guidelines

### Architecture Metadata
- **KEYWORDS**: system names, pattern types, technologies, concepts
- **CATEGORY**: 
  - `infrastructure` - Core system components
  - `patterns` - Reusable design patterns
  - `design` - Overall system architecture
  - `integration` - How systems work together
- **COMPLEXITY**: 
  - `simple` - Single component/straightforward pattern
  - `moderate` - Multiple components working together
  - `complex` - System-wide architecture with many integration points
- **AUDIENCE**: `developer|architect|team-lead`

### Troubleshooting Metadata
- **KEYWORDS**: primary technology, secondary tools, use cases, concepts
- **ISSUES**: Exact error messages in quotes, problem descriptions
- **RELATED**: Cross-references to other topics/guides
- **DIFFICULTY**: `beginner|intermediate|advanced`

## Step 5: Update Documentation Index

### After Creating Architecture Documentation
1. **Verify file appears in architecture README**: The guide should be discoverable through `docs/tech/architecture/README.md`
2. **Check system name indexing**: File follows `{system}-{pattern}-{purpose}.md` naming
3. **Validate metadata keywords**: Include all relevant search terms
4. **Test integration examples**: Ensure code examples work with current codebase

### After Creating Troubleshooting Documentation  
1. **Verify file appears in troubleshooting README**: The guide should be discoverable through `docs/tech/troubleshooting/README.md`
2. **Check error message indexing**: ISSUES metadata includes exact error text
3. **Validate solution testing**: Ensure all solutions work with current setup
4. **Cross-reference related guides**: Link to architecture docs when relevant

## Step 6: Content Quality Standards

### Working Code Examples (Both Types)
```typescript
// ✅ GOOD: Real, implemented code from this codebase
export const DatabaseService = () => {
  return connection.testConnection() // Actual working implementation
}
```

```typescript
// ❌ BAD: Pseudo-code or theoretical examples  
export const SomeService = () => {
  // ... imaginary implementation
}
```

### Integration Documentation (Architecture)
Always show **how components work together**:
```typescript
// Frontend usage
import { HealthResponse } from '@shared/health'

// Backend implementation
import { HealthResponse } from '@shared/health'
router.get('/health', async (req, res: Response<HealthResponse>) => {
  // Implementation that matches the frontend expectation
})
```

### Error + Solution Pairs (Troubleshooting)
Always pair **exact errors with tested solutions**:
```
// Error (exactly as seen)
Error: Cannot find module '@shared/health'
  at Object.<anonymous> (src/routes/health.test.ts:7:31)

// Solution (tested and working)
moduleNameMapping: {
  '^@shared/(.*)$': '<rootDir>/../shared/src/$1',
}
```

## Step 7: Validation Checklist

### Architecture Documentation Checklist
- [ ] File uses `{system}-{pattern}-{purpose}.md` naming
- [ ] Metadata includes KEYWORDS, CATEGORY, COMPLEXITY, AUDIENCE, LAST_UPDATED
- [ ] Content starts with problem identification
- [ ] Examples use real code from this codebase
- [ ] Focus is on consumer usage, not internal implementation
- [ ] Integration patterns show frontend/backend coordination
- [ ] Step-by-step implementation guide included

### Troubleshooting Documentation Checklist
- [ ] File uses `{topic}-{technology}-{purpose}.md` naming
- [ ] Metadata includes KEYWORDS, ISSUES, RELATED, DIFFICULTY, LAST_UPDATED
- [ ] Error messages are exact/verbatim from actual errors
- [ ] Solutions are tested and working
- [ ] Multiple error scenarios covered when relevant
- [ ] Cross-references to architecture docs when helpful

## Discovery Integration

### How This Makes Documentation Discoverable

**Architecture Documents**:
1. **System naming** - Cursor searches `{system}-{pattern}.md` when working on that system
2. **Keyword metadata** - Matches KEYWORDS to current development context
3. **Category filtering** - Finds infrastructure vs patterns vs design docs
4. **Semantic search** - Finds architecture by content relevance

**Troubleshooting Documents**:
1. **File naming patterns** - Cursor searches `{topic}-{technology}-{purpose}.md`
2. **Error message matching** - ISSUES metadata connects exact errors to solutions
3. **Keyword context** - KEYWORDS match current development technologies
4. **Cross-reference navigation** - RELATED guides provide solution paths

### Making Documentation Automatically Findable
- ✅ **Use system/topic names** in filenames
- ✅ **Include exact error messages** in ISSUES metadata
- ✅ **Add all relevant technologies** in KEYWORDS
- ✅ **Cross-reference related docs** in metadata
- ✅ **Follow established naming patterns**

## Process Complete

Following this process ensures that:
1. **Architecture docs** provide proactive guidance for building features
2. **Troubleshooting docs** provide reactive solutions to specific problems
3. **All documentation** is automatically discoverable through naming and metadata
4. **Content quality** meets standards for real, working examples
5. **Integration** with existing documentation system is seamless

The documentation becomes automatically findable through system names, error messages, keywords, and semantic search without requiring explicit prompt references.# Creating New Documentation Process

This process enables automatic creation of properly formatted architecture and troubleshooting documentation that integrates seamlessly with the existing documentation system.

## When to Use This Process

**Architecture Documentation**: Proactive guidance for building new features and understanding system design.
- Building new functionality
- Learning system architecture  
- Following established patterns
- Understanding core components and integration patterns

**Troubleshooting Documentation**: Reactive solutions to common development problems and errors.
- Encountering errors or debugging issues
- Solving specific problems
- Resolving configuration issues
- Finding solutions to error messages

## Step 1: Determine Documentation Type

**Choose Documentation Type:**

### Architecture Documentation (`docs/tech/architecture/`)
Use for:
- ✅ **Proactive guidance** - "How should I build this?"
- ✅ **Design patterns** - "What's the recommended approach?"
- ✅ **System understanding** - "How does this work?"
- ✅ **Implementation guidance** - "What should I follow?"
- ✅ Consumer-focused content - How to build WITH the architecture

### Troubleshooting Documentation (`docs/tech/troubleshooting/`)
Use for:
- 🔧 **Reactive problem solving** - "This is broken, how do I fix it?"
- 🔧 **Error resolution** - "I got this error message"
- 🔧 **Debugging guidance** - "Something isn't working"
- 🔧 **Configuration issues** - "My setup is broken"

## Step 2: Create Architecture Documentation

### Architecture File Naming Convention
**Pattern**: `{system}-{pattern}-{purpose}.md`

**Examples**:
- `api-response-patterns.md` - API response architecture
- `error-handling-infrastructure.md` - Error handling system design
- `health-monitoring-architecture.md` - Health check system
- `authentication-flow-design.md` - Auth system architecture
- `database-connection-patterns.md` - Database layer design

### Architecture File Creation Process
1. **Create file with proper naming**:
   ```bash
   touch docs/tech/architecture/{system}-{pattern}-{purpose}.md
   ```

2. **Add required metadata block at top**:
   ```html
   <!--
   KEYWORDS: system, pattern, technology, concept, use-case
   CATEGORY: infrastructure|patterns|design|integration
   COMPLEXITY: simple|moderate|complex
   AUDIENCE: developer|architect|team-lead
   LAST_UPDATED: YYYY-MM-DD
   -->
   ```

3. **Follow architecture content structure**:
   - **System-focused title**: What architecture does this document?
   - **Start with problems**: Identify specific problems developers face
   - **Clear principles**: Why was it designed this way?
   - **Working code examples**: From actual codebase implementation
   - **Integration patterns**: How components work together
   - **Consumer-focused implementation guide**: Step-by-step usage

### Architecture Content Standards

**✅ Include (Consumer-Focused)**:
- How to use components and patterns
- What methods/interfaces to call
- Step-by-step implementation guides
- Integration patterns and examples
- When to use different approaches

**❌ Exclude (Internal Details)**:
- Internal implementation details
- Private methods or internal state
- Complex algorithmic explanations
- Technical details not exposed in the public API

**Architecture Example Structure**:
```markdown
# {System} {Pattern} Architecture

<!--
KEYWORDS: api, response, error-handling, infrastructure, patterns
CATEGORY: infrastructure
COMPLEXITY: moderate
AUDIENCE: developer
LAST_UPDATED: 2025-01-20
-->

## Common {Problem Domain} Scenarios

### Scenario 1: {Specific Problem}
**Problem**: {What pain point developers experience}
**Current Pain**: {What goes wrong without the solution}

## Why {Your Solution} Solves This
{Explain why your architecture addresses these specific problems}

## Integration Patterns
```typescript
// Frontend usage
import { HealthResponse } from '@shared/health'
const health = await fetch('/api/health').json() as HealthResponse

// Backend implementation  
import { HealthResponse } from '@shared/health'
router.get('/health', async (req, res: Response<HealthResponse>) => {
  // Implementation
})
```

## Implementation Guide
1. {Step-by-step usage instructions}
2. {Integration requirements}
3. {Example implementations}
```

## Step 3: Create Troubleshooting Documentation

### Troubleshooting File Naming Convention
**Pattern**: `{topic}-{technology}-{purpose}.md`

**Examples**:
- `testing-drizzle-orm-issues.md` - Testing patterns for Drizzle ORM
- `monorepo-typescript-jest-config-errors.md` - TypeScript/Jest configuration
- `deployment-docker-production-issues.md` - Production Docker deployment
- `module-resolution-path-mapping-errors.md` - Path mapping issues

### Troubleshooting File Creation Process
1. **Create file with proper naming**:
   ```bash
   touch docs/tech/troubleshooting/{topic}-{technology}-{purpose}.md
   ```

2. **Add required metadata block**:
   ```html
   <!--
   KEYWORDS: primary, secondary, technology, use-case
   ISSUES: "specific error message", "problem description"
   RELATED: other topics, cross-references
   DIFFICULTY: beginner|intermediate|advanced
   LAST_UPDATED: YYYY-MM-DD
   -->
   ```

3. **Follow troubleshooting content structure**:
   - **Problem-focused title**: What does this solve?
   - **Clear introduction**: When to use this guide
   - **Exact error messages**: Include verbatim error text
   - **Working code examples**: From actual codebase
   - **Step-by-step solutions**: Tested fixes that work
   - **Common issues section**: Multiple error scenarios + solutions

### Troubleshooting Content Standards

**Error Documentation Requirements**:
- **Exact error messages in quotes**: `"Cannot find module '@shared'"`
- **Complete error context**: Full stack trace when relevant
- **Exact solutions**: Working code that fixes the issue
- **Tested examples**: Real implementations from this codebase

**Troubleshooting Example Structure**:
```markdown
# {Topic} {Technology} Issues

<!--
KEYWORDS: testing, drizzle, orm, database, mocking
ISSUES: "Cannot find module '@shared'", "Jest module resolution errors"
RELATED: path mapping, monorepo configuration, testing setup
DIFFICULTY: intermediate
LAST_UPDATED: 2025-01-20
-->

## When to Use This Guide
{Description of when developers encounter these issues}

## Common Error Scenarios

### Error 1: Module Resolution
```
Error: Cannot find module '@shared/health'
  at Object.<anonymous> (src/routes/health.test.ts:7:31)
```

**Solution**:
```javascript
// Fix: Update Jest moduleNameMapping
moduleNameMapping: {
  '^@shared/(.*)$': '<rootDir>/../shared/src/$1',
}
```

### Error 2: {Another Common Issue}
{Exact error message}
{Step-by-step solution}
```

## Step 4: Metadata Guidelines

### Architecture Metadata
- **KEYWORDS**: system names, pattern types, technologies, concepts
- **CATEGORY**: 
  - `infrastructure` - Core system components
  - `patterns` - Reusable design patterns
  - `design` - Overall system architecture
  - `integration` - How systems work together
- **COMPLEXITY**: 
  - `simple` - Single component/straightforward pattern
  - `moderate` - Multiple components working together
  - `complex` - System-wide architecture with many integration points
- **AUDIENCE**: `developer|architect|team-lead`

### Troubleshooting Metadata
- **KEYWORDS**: primary technology, secondary tools, use cases, concepts
- **ISSUES**: Exact error messages in quotes, problem descriptions
- **RELATED**: Cross-references to other topics/guides
- **DIFFICULTY**: `beginner|intermediate|advanced`

## Step 5: Update Documentation Index

### After Creating Architecture Documentation
1. **Verify file appears in architecture README**: The guide should be discoverable through `docs/tech/architecture/README.md`
2. **Check system name indexing**: File follows `{system}-{pattern}-{purpose}.md` naming
3. **Validate metadata keywords**: Include all relevant search terms
4. **Test integration examples**: Ensure code examples work with current codebase

### After Creating Troubleshooting Documentation  
1. **Verify file appears in troubleshooting README**: The guide should be discoverable through `docs/tech/troubleshooting/README.md`
2. **Check error message indexing**: ISSUES metadata includes exact error text
3. **Validate solution testing**: Ensure all solutions work with current setup
4. **Cross-reference related guides**: Link to architecture docs when relevant

## Step 6: Content Quality Standards

### Working Code Examples (Both Types)
```typescript
// ✅ GOOD: Real, implemented code from this codebase
export const DatabaseService = () => {
  return connection.testConnection() // Actual working implementation
}
```

```typescript
// ❌ BAD: Pseudo-code or theoretical examples  
export const SomeService = () => {
  // ... imaginary implementation
}
```

### Integration Documentation (Architecture)
Always show **how components work together**:
```typescript
// Frontend usage
import { HealthResponse } from '@shared/health'

// Backend implementation
import { HealthResponse } from '@shared/health'
router.get('/health', async (req, res: Response<HealthResponse>) => {
  // Implementation that matches the frontend expectation
})
```

### Error + Solution Pairs (Troubleshooting)
Always pair **exact errors with tested solutions**:
```
// Error (exactly as seen)
Error: Cannot find module '@shared/health'
  at Object.<anonymous> (src/routes/health.test.ts:7:31)

// Solution (tested and working)
moduleNameMapping: {
  '^@shared/(.*)$': '<rootDir>/../shared/src/$1',
}
```

## Step 7: Validation Checklist

### Architecture Documentation Checklist
- [ ] File uses `{system}-{pattern}-{purpose}.md` naming
- [ ] Metadata includes KEYWORDS, CATEGORY, COMPLEXITY, AUDIENCE, LAST_UPDATED
- [ ] Content starts with problem identification
- [ ] Examples use real code from this codebase
- [ ] Focus is on consumer usage, not internal implementation
- [ ] Integration patterns show frontend/backend coordination
- [ ] Step-by-step implementation guide included

### Troubleshooting Documentation Checklist
- [ ] File uses `{topic}-{technology}-{purpose}.md` naming
- [ ] Metadata includes KEYWORDS, ISSUES, RELATED, DIFFICULTY, LAST_UPDATED
- [ ] Error messages are exact/verbatim from actual errors
- [ ] Solutions are tested and working
- [ ] Multiple error scenarios covered when relevant
- [ ] Cross-references to architecture docs when helpful

## Discovery Integration

### How This Makes Documentation Discoverable

**Architecture Documents**:
1. **System naming** - Cursor searches `{system}-{pattern}.md` when working on that system
2. **Keyword metadata** - Matches KEYWORDS to current development context
3. **Category filtering** - Finds infrastructure vs patterns vs design docs
4. **Semantic search** - Finds architecture by content relevance

**Troubleshooting Documents**:
1. **File naming patterns** - Cursor searches `{topic}-{technology}-{purpose}.md`
2. **Error message matching** - ISSUES metadata connects exact errors to solutions
3. **Keyword context** - KEYWORDS match current development technologies
4. **Cross-reference navigation** - RELATED guides provide solution paths

### Making Documentation Automatically Findable
- ✅ **Use system/topic names** in filenames
- ✅ **Include exact error messages** in ISSUES metadata
- ✅ **Add all relevant technologies** in KEYWORDS
- ✅ **Cross-reference related docs** in metadata
- ✅ **Follow established naming patterns**

## Process Complete

Following this process ensures that:
1. **Architecture docs** provide proactive guidance for building features
2. **Troubleshooting docs** provide reactive solutions to specific problems
3. **All documentation** is automatically discoverable through naming and metadata
4. **Content quality** meets standards for real, working examples
5. **Integration** with existing documentation system is seamless

The documentation becomes automatically findable through system names, error messages, keywords, and semantic search without requiring explicit prompt references.