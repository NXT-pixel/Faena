---
name: update-context
description: Updates existing project context documentation in tasks/context/ to reflect current project state. Run at the end of development sessions to keep context accurate and current.
agent: /agents/design/project-context-analyst.md
tools: Read, Write, Bash, LS
---

This command updates the project context documentation in `tasks/context/` to reflect the current state of the project. Run this at the end of each development session to keep context accurate.

**Agent Expertise**: This command invokes the **project-context-analyst** agent (see `/agents/design/project-context-analyst.md`) who brings expertise in codebase analysis, technology detection, and context documentation to intelligently update existing context files.

## Output Location

All context files are updated in: `tasks/context/`

## Preflight Checklist

Before proceeding, complete these validation steps silently (don't report progress to user):

### 1. Context Validation
- Run: `ls -la tasks/context/ 2>/dev/null`
- If directory doesn't exist or is empty:
  - Tell user: "❌ No context to update. Please run /create-context first."
  - Exit gracefully
- Count existing files: `ls -1 tasks/context/*.md 2>/dev/null | wc -l`
- Check for import documentation:
  - `test -f tasks/context/common-imports.md || echo "missing"`
  - `test -d tasks/context/imports && [ "$(ls -A tasks/context/imports)" ] || echo "empty or missing"`
- Report: "📁 Found {count} context files to check for updates"

### 2. Change Detection

Gather information about what has changed:

**Git Changes:**
```bash
# Uncommitted changes
git status --short

# Recent commits
git log --oneline -10

# Files changed recently
git diff --stat HEAD~5..HEAD 2>/dev/null

# New untracked files
git ls-files --others --exclude-standard | head -10

# Branch info
git branch --show-current
```

**File Modifications:**
```bash
# Check context file ages
find tasks/context -name "*.md" -type f -exec ls -lt {} + | head -5
```

**Dependency Changes:**

Check package managers used in this repo (Angular/Node, C#/.NET, Python):
```bash
# Node.js (Angular ControlPanel)
git diff HEAD~5..HEAD src/ControlPanel/package.json 2>/dev/null

# Python (Orchestration, Azure Functions)
git diff HEAD~5..HEAD requirements.txt pyproject.toml 2>/dev/null
git diff HEAD~5..HEAD src/Orchestration/requirements.txt 2>/dev/null
git diff HEAD~5..HEAD ../PythonMAFWithAzureFunctions/Orchestration/requirements.txt 2>/dev/null

# C#/.NET (ControlPanel.Api, Services, Contracts)
git diff HEAD~5..HEAD "*.csproj" 2>/dev/null
git diff HEAD~5..HEAD src/ControlPanel.Api/*.csproj src/Contracts/*.csproj src/Services/*/*.csproj 2>/dev/null
```

### 3. Get Current DateTime
- Run: `date -u +"%Y-%m-%dT%H:%M:%SZ"`
- Store for updating `last_updated` field in modified files
- **CRITICAL**: Never use placeholders like [DATE] or [TIMESTAMP]

## Execution Steps

### 1. Systematic Change Analysis

For each context file, determine if updates are needed:

#### `progress.md` - **Always Update**
- **Check**: Recent commits, current branch, uncommitted changes
- **Update**: Latest completed work, current blockers, next steps
- **Commands**: 
  ```bash
  git log --oneline -5
  git status --short
  ```
- Include completion percentages if applicable

#### `project-structure.md` - **Update if Changed**
- **Check**: New files or directories added
  ```bash
  git diff --name-status HEAD~10..HEAD | grep -E '^A'
  ```
- **Update**: New directories, moved files, structural reorganization
- For **PrototypeZero**: if `docker/`, `scripts/` (e.g. `start-dev-environment.*`, `publish-all-docker.sh`), or `etc/docker/` changed meaningfully, refresh how local deployment is described in `project-structure.md` and/or `tech-context.md` (and `progress.md` if the team’s “how to run” story changed)
- Only update if significant structural changes occurred

#### `tech-context.md` - **Update if Dependencies Changed**
- **Check**: Package files for new dependencies or version changes
- **Update**: New libraries, upgraded versions, new dev tools
- Include security updates or breaking changes

#### `system-patterns.md` - **Update if Architecture Changed**
- **Check**: New design patterns, architectural decisions
- **Update**: New patterns adopted, refactoring done
- Only update for significant architectural changes

#### `product-context.md` - **Update if Requirements Changed**
- **Check**: New features implemented, user feedback incorporated
- **Update**: New user stories, changed requirements
- Include any pivot in product direction

#### `project-brief.md` - **Rarely Update**
- **Check**: Only if fundamental project goals changed
- **Update**: Major scope changes, new objectives
- Usually remains stable

#### `project-overview.md` - **Update for Major Milestones**
- **Check**: Major features completed, significant progress
- **Update**: Feature status, capability changes
- Update when reaching project milestones

#### `project-vision.md` - **Rarely Update**
- **Check**: Strategic direction changes
- **Update**: Only for major vision shifts
- Usually remains stable

#### `project-style-guide.md` - **Update if Conventions Changed**
- **Check**: New linting rules, style decisions
- **Update**: Convention changes, new patterns adopted
- Include examples of new patterns

#### `common-imports.md` - **Update if Imports Changed**

Regenerate import reference if import patterns have changed significantly.

- **Pre-Check**: Verify import documentation exists
  ```bash
  # Check if common-imports.md exists
  if [ ! -f "tasks/context/common-imports.md" ]; then
    echo "⚠️ Import documentation not found"
  fi
  
  # Check if imports directory has content
  if [ -d "tasks/context/imports" ] && [ -z "$(ls -A tasks/context/imports)" ]; then
    echo "⚠️ Import reference directory is empty"
  fi
  ```
  
- **If Missing**: Import documentation doesn't exist yet
  - Notify user: "⚠️ Import reference documentation not found. I can create it now by running the import analysis."
  - **Execute** import analysis (from repo root: `bash AngularWithMCPServers/scripts/analyze-imports.sh --full` or on Windows: `.\AngularWithMCPServers\.cursor\scripts\analyze-imports.ps1` or `run-analyze-imports.ps1` if quote errors occur)
  - **Read** `src/ControlPanel/tsconfig.json` and `tsconfig.app.json` for path mappings (Angular)
  - **Interpret** the script output (Angular external/internal imports, C# namespaces and project refs, Python imports)
  - **Write** `tasks/context/common-imports.md` with cross-stack import reference (Angular, C#, Python)
  - **Write** `tasks/context/imports/control-panel-imports.md`, `imports/csharp-imports.md`, `imports/python-imports.md` as appropriate (internal imports per stack)
  - Note in summary that import docs were created
  
- **If Exists - Check**: Count TypeScript and C# and Python files modified recently
  ```bash
  git diff --name-status HEAD~10..HEAD | grep -E '\.(ts|tsx)$' | wc -l
  git diff --name-status HEAD~10..HEAD | grep -E '\.cs$' | wc -l
  git diff --name-status HEAD~10..HEAD | grep -E '\.py$' | wc -l
  ```

- **Threshold**: If >20 TS/CS/PY files changed (combined or per stack), regenerate:
  1. **Execute** the analysis script from repo root to collect current import data:
     ```bash
     bash AngularWithMCPServers/scripts/analyze-imports.sh --full
     ```
     (On Windows without Bash, use `.\AngularWithMCPServers\.cursor\scripts\analyze-imports.ps1` or `run-analyze-imports.ps1`.)
  2. **Interpret** the raw output: Angular external/internal packages, C# project references and `using` namespaces, Python import counts and requirements.
  3. **Read** Angular path config: `src/ControlPanel/tsconfig.json`, `src/ControlPanel/tsconfig.app.json` (extract `compilerOptions.paths` if present).
  4. **Write** updated `common-imports.md` to `tasks/context/common-imports.md` (cross-stack and key packages).
  5. **Write** stack-specific files under `tasks/context/imports/`: e.g. `control-panel-imports.md`, `csharp-imports.md`, `python-imports.md` (internal imports per stack).
  6. Preserve format but update usage counts and import lists.
  7. Update `last_updated` timestamp in frontmatter.

  **Agent Responsibility**: Execute the script, read tsconfig/csproj/requirements as needed, analyze output, and create/update the markdown documentation. Use path mappings from tsconfig where available. Stack-specific files should focus on internal imports for that stack only.
  
- **Skip**: If few TypeScript files changed or patterns appear stable

**Rationale:** Import patterns change when:
- New Angular packages or C# project references added
- Major refactoring moves code (Angular, .NET, or Python)
- New shared utilities or contracts created
- Cross-stack or cross-project dependencies change

**Update Strategy:**
- Surgical updates: only change sections with actual differences
- Keep historical high-value imports even if usage decreased
- Add new commonly-used imports discovered
- Remove imports that no longer exist in codebase
- **Use path mappings**: Read `src/ControlPanel/tsconfig*.json` for Angular path mappings where present
- **Separate concerns**: Cross-stack and key packages in `common-imports.md`; internal imports only in stack-specific files (`control-panel-imports.md`, `csharp-imports.md`, `python-imports.md`)

### 2. Smart Update Strategy

**For each file that needs updating:**

1. **Read existing file** to understand current content
2. **Identify specific sections** that need updates
3. **Preserve frontmatter** but update `last_updated` field:
   ```yaml
   ---
   created: [preserve original]
   last_updated: [Use REAL datetime from step 3]
   version: [increment if major update, e.g., 1.0 → 1.1]
   author: Cursor Agent System
   ---
   ```
4. **Make targeted updates** - don't rewrite entire file
5. **Add update notes** at the bottom if significant:
   ```markdown
   ## Update History
   - {date}: {summary of what changed}
   ```

### 3. Update Validation

After updating each file:
- Verify file still has valid frontmatter
- Check file size is reasonable (not corrupted)
- Ensure markdown formatting is preserved
- Confirm updates accurately reflect changes

### 4. Skip Optimization

**Skip files that don't need updates:**
- If no relevant changes detected, skip the file
- Report skipped files in summary
- Don't update timestamp if content unchanged
- This preserves accurate "last modified" information

### 5. Error Handling

**Common Issues:**
- **File locked:** "❌ Cannot update {file} - may be open in editor"
- **Permission denied:** "❌ Cannot write to {file} - check permissions"
- **Corrupted file:** "⚠️ {file} appears corrupted - skipping update"
- **Disk space:** "❌ Insufficient disk space for updates"

If update fails:
- Report which files were successfully updated
- Note which files failed and why
- Preserve original files (don't leave corrupted state)

### 6. Update Summary

Provide detailed summary of updates:

```
🔄 Context Update Complete

📊 Update Statistics:
  - Files Scanned: {total_count}
  - Files Updated: {updated_count}
  - Files Skipped: {skipped_count} (no changes needed)
  - Errors: {error_count}

📝 Updated Files:
  ✅ progress.md - Updated recent commits, current status
  ✅ tech-context.md - Added 3 new dependencies (React Query, Zod, date-fns)
  ✅ project-structure.md - Noted new /utils directory
  ✅ common-imports.md - Regenerated (import patterns updated)

⏭️ Skipped Files (no changes):
  - project-brief.md (last updated: 5 days ago)
  - project-vision.md (last updated: 2 weeks ago)
  - system-patterns.md (last updated: 3 days ago)
  - product-context.md (last updated: 1 week ago)
  - project-overview.md (last updated: 4 days ago)
  - project-style-guide.md (last updated: 1 week ago)

⚠️ Issues:
  {any warnings or errors if applicable}

💬 Notes:
  - Import reference documentation not found in tasks/context/. Consider creating it.
  {other notes if applicable}

⏰ Last Update: {timestamp}
💡 Tip: Major changes? Consider running /create-context for full refresh
💡 Next: Run this command regularly after development sessions
```

### 7. Incremental Update Tracking

**Track what was updated:**
- Note which sections of each file were modified
- Keep changes focused and surgical
- Don't regenerate unchanged content
- Preserve formatting and structure

### 8. Performance Optimization

For large projects:
- Process files in parallel when possible
- Show progress: "Updating context files... {current}/{total}"
- Skip very large files with warning
- Use git diff to quickly identify changed areas

## Change Detection Commands

Use these commands to detect changes:

```bash
# Context directory
ls -la tasks/context/ 2>/dev/null

# Current git status
git status --short

# Recent commits
git log --oneline -10

# Changed files
git diff --name-only HEAD~5..HEAD 2>/dev/null

# Branch info
git branch --show-current

# Uncommitted changes stats
git diff --stat

# New untracked files
git ls-files --others --exclude-standard | head -10

# Files added/modified/deleted
git diff --name-status HEAD~5..HEAD 2>/dev/null

# Commit activity by file
git log --pretty=format: --name-only --since="5 days ago" | sort | uniq -c | sort -rg | head -10
```

## Content Quality Standards

Each updated context file must:
- Maintain minimum 10 lines of meaningful content
- Preserve structured markdown with clear headings
- Add specific information based on actual changes
- Be evidence-based from real codebase analysis
- Update timestamps only when content changes
- Use precise technical terminology
- Include examples from actual code when relevant
- Keep focused on their specific domain

## Update Philosophy

**Surgical Updates:**
- Only update what has changed
- Preserve historical information that's still relevant
- Don't regenerate entire files unnecessarily
- Keep original creation timestamp
- Update version only for significant changes

**Evidence-Based:**
- Base updates on git history and file changes
- Reference specific commits when relevant
- Cite new files, directories, or dependencies
- Don't assume - verify with commands

**Timestamp Accuracy:**
- Only update `last_updated` when content actually changes
- This makes timestamps meaningful for tracking
- Skipped files retain their original update time
- Helps identify stale context files

## Important Notes

- **Only update files with actual changes** - preserve accurate timestamps
- **Always use real datetime** from system clock for `last_updated`
- **Make surgical updates** - don't regenerate entire files
- **Validate each update** - ensure files remain valid
- **Provide detailed summary** - show what changed and what didn't
- **Handle errors gracefully** - don't corrupt existing context
- **Base updates on evidence** - use git diff and actual file analysis
- **Keep changes focused** - update specific sections, not entire files


