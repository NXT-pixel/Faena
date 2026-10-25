---
name: create-context
description: Generates comprehensive project context documentation in tasks/context/ by analyzing the codebase, detecting technologies, and creating 9 context files with real timestamps.
agent: /agents/design/project-context-analyst.md
tools: Read, Write, Bash, LS
---

This command creates initial project context documentation in `tasks/context/` by analyzing the current project state and establishing comprehensive baseline documentation.

**Agent Expertise**: This command invokes the **project-context-analyst** agent (see `/agents/design/project-context-analyst.md`) who brings expertise in codebase analysis, technology detection, and context documentation generation.

## Output Location

All context files are created in: `tasks/context/`

## Preflight Checklist

Before proceeding, complete these validation steps silently (don't report progress to user):

### 1. Context Directory Check
- Run: `ls -la tasks/context/ 2>/dev/null`
- If directory exists and has files:
  - Count existing files: `ls -1 tasks/context/*.md 2>/dev/null | wc -l`
  - Ask user: "⚠️ Found {count} existing context files. Overwrite all context? (yes/no)"
  - Only proceed with explicit 'yes' confirmation
  - **CRITICAL**: Never overwrite or delete `tasks/context/team-context.md` or `tasks/context/learnings.md` as they store essential team hierarchy and accumulated organizational memory.
  - If user says no, suggest: "Back up existing files or update them individually"

### 2. Project Type Detection in Proyecto/
- In Faena, the client code lives in `Proyecto/`.
- Inspect `Proyecto/` to detect cloned repositories:
  - Node.js / Angular / React / Vue: `package.json` inside `Proyecto/`
  - .NET / C#: `*.csproj` or `*.sln` inside `Proyecto/`
  - Python: `requirements.txt` or `pyproject.toml` inside `Proyecto/`
  - Rust: `Cargo.toml` inside `Proyecto/`
  - Go: `go.mod` inside `Proyecto/`


### 3. Directory Creation
- If `tasks/` doesn't exist, create it: `mkdir -p tasks/context/`
- Verify write permissions: `touch tasks/context/.test && rm tasks/context/.test`
- If permission denied, tell user: "❌ Cannot create context directory. Check permissions."

### 4. Get Current DateTime
- Run: `date -u +"%Y-%m-%dT%H:%M:%SZ"`
- Store this value for use in all context file frontmatter
- **CRITICAL**: Never use placeholders like [DATE] or [TIMESTAMP]

## Execution Steps

### 1. Pre-Analysis Validation
- Confirm project root directory is correct (presence of .git, package.json, etc.)
- Check for existing documentation that can inform context (README.md, docs/)
- If README.md doesn't exist, ask user for brief project description

### 2. Systematic Project Analysis

Gather information in this order:

**Project Detection:**
```bash
# Find project files
find . -maxdepth 2 \( -name 'package.json' -o -name 'requirements.txt' \
  -o -name 'pyproject.toml' -o -name 'pom.xml' -o -name 'build.gradle' \
  -o -name 'build.gradle.kts' -o -name '*.sln' -o -name '*.csproj' \
  -o -name 'Gemfile' -o -name 'Cargo.toml' -o -name 'go.mod' \
  -o -name 'composer.json' -o -name 'pubspec.yaml' -o -name 'CMakeLists.txt' \
  -o -name 'Dockerfile' -o -name 'docker-compose.yml' -o -name 'docker-compose*.yml' -o -name 'docker-compose*.yaml' -o -name 'Package.swift' \
  -o -type d -name '*.xcodeproj' -o -type d -name '*.xcworkspace' \) 2>/dev/null

# Git information
git remote -v 2>/dev/null
git branch --show-current 2>/dev/null
git log --oneline -10 2>/dev/null
git status --short 2>/dev/null
```

**Codebase Analysis:**
```bash
# Find source files
find . -type f \( -name '*.js' -o -name '*.ts' -o -name '*.jsx' -o -name '*.tsx' \
  -o -name '*.py' -o -name '*.rs' -o -name '*.go' -o -name '*.php' \
  -o -name '*.swift' -o -name '*.java' -o -name '*.kt' -o -name '*.kts' \
  -o -name '*.cs' -o -name '*.rb' -o -name '*.dart' -o -name '*.c' -o -name '*.h' \
  -o -name '*.cpp' -o -name '*.hpp' -o -name '*.sh' \) 2>/dev/null | head -20

# Root directory structure
ls -la

# Test detection
find . \( -path '*/.*' -prune \) -o \( -type d \( -name 'test' -o -name 'tests' \
  -o -name '__tests__' -o -name 'spec' \) -o -type f \( -name '*[._]test.*' \
  -o -name '*[._]spec.*' -o -name 'test_*.*' -o -name '*_test.*' \) \) 2>/dev/null | head -10

# Documentation discovery
find . -type f -name '*.md' -path '*/docs/*' 2>/dev/null | head -10
```

- Read README.md if it exists
- Check package files for dependencies and versions

### 3. Context File Creation

Generate the following 9 context files with frontmatter:

#### Frontmatter Template (use in ALL files)
```yaml
---
created: [Use REAL datetime from step 4]
last_updated: [Use REAL datetime from step 4]
version: 1.0
author: Cursor Agent System
---
```

#### Required Files

1. **tasks/context/progress.md**
   - Current project status and branch
   - Recent commits (last 10)
   - Outstanding changes
   - Immediate next steps
   - Current development focus

2. **tasks/context/project-structure.md**
   - Directory structure and organization
   - Key directories explained
   - File naming patterns
   - Module organization
   - Source vs. generated code

3. **tasks/context/tech-context.md**
   - Language and version
   - Framework versions
   - Development dependencies
   - Production dependencies
   - Build tools and scripts
   - Dev environment requirements

4. **tasks/context/system-patterns.md**
   - Architectural style (monolith, microservices, etc.)
   - Design patterns observed in code
   - Data flow patterns
   - State management approach
   - Error handling patterns
   - Testing patterns

5. **tasks/context/product-context.md**
   - Target users/personas
   - Core features and functionality
   - Primary use cases
   - User workflows
   - Business domain

6. **tasks/context/project-brief.md**
   - What the project does
   - Why it exists
   - Project scope
   - Key objectives
   - Success criteria

7. **tasks/context/project-overview.md**
   - Feature list
   - Current state/maturity
   - Integration points
   - External dependencies
   - Deployment model

8. **tasks/context/project-vision.md**
   - Long-term goals
   - Potential expansions
   - Strategic priorities
   - Future roadmap ideas
   - Technical evolution plans

9. **tasks/context/project-style-guide.md**
   - Coding conventions
   - Naming conventions
   - File structure patterns
   - Comment style
   - Code organization preferences
   - Testing conventions

10. **tasks/context/common-imports.md**
   - Cross-workspace import patterns (@pipe-flo/*)
   - Internal workspace imports (top 30 per workspace)
   - Public API references
   - Import style guidelines

### 3b. Import Reference Generation

After creating the 9 core context files, generate import reference documentation:

**Step 1: Execute Import Analysis Script**
```bash
bash scripts/analyze-imports.sh --full
```

**Agent Responsibility**: You must execute this script and capture its output. The script outputs raw import analysis data to stdout including:
- Cross-workspace `@pipe-flo/*` imports with usage counts
- Imported symbols per package (top 20)
- Internal imports per workspace (top 30)
- Sample import statements for context

**Step 2: Interpret Data and Write Documentation Files**

**Agent Responsibility**: Analyze the script's raw output and transform it into well-organized markdown documentation. You must create:

1. **`tasks/context/common-imports.md`** - Main reference file with:
   - Purpose and usage guidelines
   - **Cross-workspace imports section** (grouped by package with symbol lists)
   - Focus on `@pipe-flo/*` imports between workspaces
   - Links to internal workspace detail files
   - Import style guide reference
   - Analysis metadata

2. **`tasks/context/imports/{workspace}-imports.md`** files for each workspace:
   - **Focus**: Internal imports only (within the same workspace)
   - Exclude cross-workspace imports (those are in common-imports.md)
   - Top 30 most common internal imports
   - Usage notes and recommendations

**Content Guidelines:**
- **Use tsconfig path mappings**: Read each workspace's `tsconfig.json` to find path mappings (e.g., `@/*`, `@/services/*`) and use those in documentation instead of relative paths
- Include actual usage counts to show importance
- Group related imports by architecture (e.g., services, components, utilities, middleware)
- Add links to source files using mapped paths
- Include code examples showing proper import syntax with path mappings
- Note architectural patterns (e.g., hooks, components, utilities)
- Use proper frontmatter with generation timestamp
- **Internal only**: Do not document `@pipe-flo/*` imports in workspace-specific files

**Validation:**
- Verify all 5 files created (1 main + 4 workspace detail files)
- Check frontmatter is valid in all files
- Ensure markdown formatting is correct
- Validate links to source files work

**Error Handling:**
If import analysis script fails:
- Report error details from the script execution
- Continue with 9 core context files
- Note import reference unavailable in summary
- Do NOT skip this step without attempting to run the script

**Critical**: The agent executing this command is responsible for:
1. Running `bash scripts/analyze-imports.sh --full`
2. Parsing and interpreting the console output
3. **Reading each workspace's `tsconfig.json`** to extract path mappings (e.g., `@/*`, `@/services/*`)
4. Creating well-structured markdown files from the raw data using path mappings
5. Writing files to `tasks/context/common-imports.md` and `tasks/context/imports/*.md`
6. Ensuring workspace-specific files focus on **internal imports only**

**Path Mapping Strategy**:
- For each workspace (frontend, backend, shared, calc-engine):
  - Read `{workspace}/tsconfig.json`
  - Extract the `compilerOptions.paths` section
  - Use these mapped paths in documentation (e.g., `import { ModelService } from '@/services/ModelService'`)
  - Do NOT use relative paths like `../../services/ModelService`

Do not delegate this to the user or suggest manual steps. Execute, interpret, and document.

### 4. Quality Validation

After creating each file:
- Verify file was created successfully: `test -f tasks/context/{filename}.md && echo "✅"`
- Check file is not empty: `wc -l tasks/context/{filename}.md` (minimum 10 lines)
- Ensure frontmatter is present and valid
- Validate markdown formatting is correct

### 5. Error Handling

**Common Issues:**
- **No write permissions:** "❌ Cannot write to tasks/context/. Check permissions."
- **Disk space:** "❌ Insufficient disk space for context files."
- **File creation failed:** "❌ Failed to create {filename}. Error: {error}"
- **Invalid datetime:** "❌ Could not retrieve system datetime. Check date command."

If any file fails to create:
- Report which files were successfully created
- Provide option to continue with partial context
- Never leave corrupted or incomplete files
- Clean up failed attempts if needed

### 6. Post-Creation Summary

Provide comprehensive summary:

```
📋 Context Creation Complete

📁 Created context in: tasks/context/
✅ Files created: {count}/10 (9 context + import reference)

📊 Context Summary:
  - Project Type: {detected_type}
  - Language: {primary_language}
  - Git Status: {clean/changes}
  - Dependencies: {count} packages
  - Files analyzed: {count}

📝 File Details:
  ✅ progress.md ({lines} lines) - Current status and recent work
  ✅ project-structure.md ({lines} lines) - Directory organization
  ✅ tech-context.md ({lines} lines) - Technology stack
  ✅ system-patterns.md ({lines} lines) - Architecture patterns
  ✅ product-context.md ({lines} lines) - Product requirements
  ✅ project-brief.md ({lines} lines) - Project scope
  ✅ project-overview.md ({lines} lines) - Feature overview
  ✅ project-vision.md ({lines} lines) - Strategic direction
  ✅ project-style-guide.md ({lines} lines) - Coding standards
  ✅ common-imports.md ({lines} lines) - Import patterns
    └─ imports/frontend-imports.md ({lines} lines)
    └─ imports/backend-imports.md ({lines} lines)
    └─ imports/shared-imports.md ({lines} lines)
    └─ imports/calc-engine-imports.md ({lines} lines)

⏰ Created: {timestamp}
💡 Next: Attach tasks/context/ to your prompts for AI-ready project understanding
💡 Tip: Re-run this command periodically to keep context current
```

## Content Quality Standards

Each context file must:
- Have minimum 10 lines of meaningful content
- Use structured markdown with clear headings
- Contain specific information, not generic templates
- Be evidence-based from actual codebase analysis
- Provide actionable information for developers
- Accurately reflect current state
- Use precise technical terminology
- Include examples from actual code when relevant

## Important Notes

- **Always use real datetime** from system clock, never placeholders
- **Ask for confirmation** before overwriting existing context
- **Validate each file** is created successfully
- **Provide detailed summary** of what was created
- **Handle errors gracefully** with specific guidance
- **Base content on actual analysis** not assumptions
- **Keep files focused** on their specific domain


