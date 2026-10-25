---
name: load-context
description: Loads and synthesizes project context from tasks/context/ for design discussions. Reads all context files in priority order and provides a comprehensive project understanding summary.
agent: /agents/design/project-context-analyst.md
tools: Read, Bash, LS
---

This command loads existing project context documentation from `tasks/context/` to prime an AI session with comprehensive project understanding. Optimized for design discussions and strategic planning.

**Agent Expertise**: This command invokes the **project-context-analyst** agent (see `/agents/design/project-context-analyst.md`) who brings expertise in codebase analysis and context synthesis for effective design discussions.

## Purpose

Use this command at the start of design discussions to:
- Load complete project understanding into AI context
- Understand current state before proposing changes
- Ensure design decisions align with existing patterns
- Access technical constraints and product vision

## Preflight Checklist

Complete these validation steps silently (don't report individual checks to user):

### 1. Context Availability Check
- Run: `ls -la tasks/context/ 2>/dev/null`
- If directory doesn't exist or is empty:
  - Tell user: "❌ No context found. Please run /create-context first to establish project context."
  - Exit gracefully
- Count available context files: `ls -1 tasks/context/*.md 2>/dev/null | wc -l`
- Expected: 10 context files (9 core + common-imports.md)
- Minimum: 5 for partial context

### 2. File Integrity Check
For each expected context file:
- Verify file is readable: `test -r "tasks/context/{file}" && echo "readable"`
- Check file has content: `test -s "tasks/context/{file}" && echo "has content"`
- Check for valid frontmatter (should start with `---`)

Report any issues:
- Empty files: "⚠️ {filename} is empty (skipping)"
- Unreadable files: "⚠️ Cannot read {filename} (permission issue)"
- Missing frontmatter: "⚠️ {filename} missing frontmatter (may be corrupted)"

### 3. Project State Check
- Run: `git status --short 2>/dev/null` to see current state
- Run: `git branch --show-current 2>/dev/null` to get current branch
- Run: `date -u +"%Y-%m-%dT%H:%M:%SZ"` to capture load time
- Note if not in git repository (context may be less complete)

## Execution Steps

### 1. Context Loading Sequence

Load context files in priority order optimized for design discussions:

**Priority 1 - Team & Vision (load first):**
1. `team-context.md` - Team hierarchy, Tech Lead, QA, DevOps, colleagues and delegation protocol
2. `project-vision.md` - Long-term direction and strategic goals
3. `project-brief.md` - Core purpose and project scope
4. `product-context.md` - User needs, personas, and requirements

**Priority 2 - Current State & Memory (load second):**
5. `progress.md` - Current status, recent work, and immediate focus
6. `learnings.md` - Continuous memory, gotchas, conventions and previous ticket insights
7. `project-overview.md` - Feature list, maturity, and capabilities

**Priority 3 - Technical Foundation (load third):**
8. `tech-context.md` - Technology stack, dependencies, and tools
9. `system-patterns.md` - Architecture patterns and design principles
10. `project-structure.md` - Directory organization, repos in Proyecto/, and file layout

**Priority 4 - Standards (load last):**
11. `project-style-guide.md` - Coding conventions and company standards
12. `common-imports.md` - Import patterns and public APIs

### 2. Validation During Loading

For each file loaded:
- **Parse Frontmatter**:
  - Extract `created` date (should be valid ISO 8601)
  - Extract `last_updated` date (should be ≥ created date)
  - Extract `version` (should be present)
  - Track age: calculate days since last_updated
- **Content Validation**:
  - Verify file has meaningful content (minimum 10 lines)
  - Check for markdown structure (headers present)
- **Track Loading Status**:
  - Success: File loaded and validated
  - Warning: File loaded but has issues
  - Failed: Could not load file

### 3. Context Age Analysis

After loading frontmatter from all files:
- Calculate staleness for each file
- Flag files not updated in >30 days: "⚠️ {file} last updated {days} days ago"
- Identify newest file: "📅 Most recent: {file} updated {date}"
- Identify oldest file: "📅 Stalest: {file} updated {date}"

If any file is >90 days old:
- Suggest: "💡 Consider running /update-context to refresh stale context"

### 4. Supplementary Information

After loading context files, gather additional current state:

**Recent Activity:**
```bash
# Last 5 commits for context
git log --oneline -5 2>/dev/null

# Current branch
git branch --show-current 2>/dev/null

# Any uncommitted changes
git status --short 2>/dev/null
```

**Project Structure & Repositories in Proyecto/:**
- Inspect `Proyecto/` to list all cloned client repositories (e.g. `Proyecto/backend-api`, `Proyecto/frontend-web`)
- Check for `.env.example`, `docker-compose.yml` or container definitions inside `Proyecto/<repo>`
- Read `README.md` in `Proyecto/<repo>` if available for local execution instructions

### 5. Error Recovery

**If critical files are missing:**

- `project-brief.md` OR `project-vision.md` missing:
  - Attempt to understand from README.md
  - Note limitation: "⚠️ Project goals unclear - missing brief/vision"
  
- `progress.md` missing:
  - Fall back to recent git commits for status
  - Note limitation: "⚠️ Current status uncertain - missing progress file"
  
- `tech-context.md` missing:
  - Analyze project configuration files directly (package.json, requirements.txt, etc.)
  - Note limitation: "⚠️ Technology stack may be incomplete"

**If context is incomplete:**
- Inform user which files are missing or problematic
- Suggest: "💡 Run /update-context to refresh problematic files"
- Continue with partial context but clearly note limitations
- DO NOT fail completely - work with what's available

### 6. Context Synthesis

After loading all files, synthesize key information:

**Extract Key Facts:**
- Project name and type
- Primary language and framework
- Current development phase/maturity
- Active feature areas
- Known limitations or technical debt
- User personas and primary use cases
- Architectural patterns in use

**Identify Patterns:**
- Consistent design approaches
- Testing strategies
- Code organization principles
- Technology choices and rationale

**Note Tensions:**
- Competing priorities
- Technical constraints vs product goals
- Areas of active change vs stable foundations

### 7. Loading Summary

Provide comprehensive summary optimized for design discussions:

```
🧠 Context Loaded Successfully

📚 Context Files Loaded:
  ✅ Vision & Product: {count}/3 files
  ✅ Current State: {count}/2 files
  ✅ Technical Foundation: {count}/3 files
  ✅ Standards: {count}/2 files (style guide + imports)

🎯 Project Understanding:
  - Name: {project_name}
  - Type: {project_type} ({language})
  - Status: {current_status from progress.md}
  - Branch: {git_branch}
  - Maturity: {development_phase}

👥 Product Context:
  - Primary Users: {user_personas}
  - Core Purpose: {one_sentence_summary}
  - Key Features: {count} implemented, {count} in development

🏗️ Technical Context:
  - Architecture: {architectural_style}
  - Framework: {primary_framework} {version}
  - Database: {database}
  - Deployment: {deployment_model}

📊 Context Health:
  - Total Files: {loaded}/{expected} loaded successfully
  - Freshness: Last updated {most_recent_date}
  - Staleness: {count} files >30 days old
  - Warnings: {warning_count}

⚠️ Warnings (if any):
  {list any missing files, stale files, or integrity issues}

🎨 Design Discussion Ready:
  ✅ Product vision loaded
  ✅ Current state understood
  ✅ Technical constraints known
  ✅ Architectural patterns identified
  ✅ Ready for design discussion

💬 Project Summary:
  {3-4 sentence summary combining project purpose, current state, 
   and what makes this project unique or interesting}

💡 Next Steps:
  - Proceed with design discussion
  - Reference loaded context for decisions
  - Suggest running /update-context after session
```

### 8. Partial Context Handling

If some files fail to load or are missing:

**Minimum Viable Context** (can proceed):
- Have at least 5/10 files
- Must have: progress.md, project-overview.md, tech-context.md
- Nice to have: common-imports.md (prevents import hallucination)
- Can work around missing vision/style guide files

**Insufficient Context** (should warn):
- Fewer than 5/10 files loaded
- Missing critical files: progress.md or project-overview.md
- Tell user: "⚠️ Context is incomplete. Design decisions may not align with project goals."
- Suggest: "Run /create-context to rebuild all context files"

**For each missing/failed file:**
- Note what information is unavailable
- Suggest remediation steps
- Explain impact on design discussions:
  - Missing `project-vision.md`: "Cannot assess long-term alignment"
  - Missing `product-context.md`: "User needs unclear"
  - Missing `system-patterns.md`: "Architectural patterns unknown"
  - Missing `project-style-guide.md`: "Coding conventions unclear"

### 9. Context Summary for AI

After presenting the user-facing summary, internally synthesize a mental model:

**What I Know:**
- List key facts about the project
- Technical constraints and capabilities
- Product vision and user needs
- Current priorities and active work

**What I Don't Know:**
- Note any gaps in loaded context
- Identify areas needing clarification
- Flag uncertain assumptions

**How to Help:**
- Optimize design suggestions based on context
- Respect existing patterns and conventions
- Align proposals with product vision
- Consider current priorities and constraints

## Performance Optimization

For large contexts:
- Load files sequentially in priority order (ensures essential context loads first)
- Show progress: "Loading context files... {current}/{total}" (only if >3 seconds)
- Skip extremely large files (>10,000 lines) with warning
- Cache parsed frontmatter data

## Content Quality Assessment

While loading, assess quality of each file:

**Good Indicators:**
- Specific information (not generic templates)
- Recent last_updated date (<30 days)
- Substantial content (>50 lines typically)
- Clear structure with headers
- Code examples or specific references

**Quality Issues:**
- Generic placeholder text
- Very short (<20 lines)
- No updates in >90 days
- Missing key sections
- Vague or template language

Report quality concerns:
```
📊 Context Quality Assessment:
  ✅ High Quality: {count} files (specific, recent, detailed)
  ⚠️ Needs Refresh: {count} files (stale or thin content)
  ❌ Problematic: {count} files (missing or corrupted)
```

## Important Notes

- **Always validate** files before attempting to read
- **Load in priority order** to get essential context first (especially for design discussions)
- **Handle missing files gracefully** - don't fail completely
- **Provide clear summary** of what was loaded and project state
- **Note any issues** that might affect design work
- **Synthesize information** - don't just list what was loaded
- **Optimize for design** - emphasize vision, patterns, and constraints
- **Track context age** - warn if context is stale
- **Work with partial context** - some context is better than none

## Exit Conditions

**Success**: Context loaded successfully (proceed with design discussion)
**Partial Success**: Some context loaded (proceed with warnings)
**Failure**: No context directory or all files failed to load (exit gracefully)

## Usage Pattern

Typical workflow:
1. User runs `/load-context` at start of design discussion
2. Agent loads and synthesizes all context
3. Agent provides comprehensive summary
4. Agent is now primed for design discussion with full project understanding
5. At end of session, user runs `/update-context` to capture any decisions made


