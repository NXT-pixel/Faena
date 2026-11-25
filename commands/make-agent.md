# How to Make an Agent

## Overview

This guide describes how to create agent descriptions for specialized AI assistants. After analyzing 100+ agent files from two major collections, we've identified common patterns and structural elements that make agents effective. This guide presents both the core components every agent needs and optional elements to include based on complexity.

## Core Philosophy

An agent file serves as a **specialized instruction manual** that:
- Defines the agent's expertise and role
- Establishes behavioral patterns and priorities
- Provides reference material for quick lookup
- Specifies tools and methodologies
- Guides decision-making through checklists and workflows

## Persona vs. Procedure: The Critical Distinction

**AGENTS define WHO. COMMANDS define HOW TO.**

This is the most important principle when creating agents and commands:

### PERSONA (Agent Files)

Agent files describe the **identity and capabilities** of a specialized assistant:

- **Expertise**: What domains and technologies they master
- **Knowledge**: Patterns, practices, and principles they understand
- **Behavioral traits**: How they approach problems and make decisions
- **Capabilities**: What types of work they can perform
- **Communication style**: How they interact and explain concepts
- **Quality standards**: What "good" looks like in their domain

**Agents answer:** "Who am I? What do I know? How do I think?"

### PROCEDURE (Command Files)

Command files describe the **execution process** for accomplishing tasks:

- **Execution steps**: Sequential actions to perform
- **Workflows**: Multi-phase processes with specific order
- **File operations**: Where to read from and write to
- **Command invocations**: When to call other commands or agents
- **Error handling**: What to do when things go wrong
- **Output specifications**: Document templates and folder structures

**Commands answer:** "What steps do I take? Where do files go? When do I invoke others?"

### Why This Separation Matters

**Mixing persona and procedure creates confusion:**
- Agents with workflows become rigid and can't adapt to different use cases
- Commands without agents lack domain expertise and quality standards
- Maintenance becomes difficult when behavior and process are intertwined

**Clean separation enables:**
- Agents can be invoked directly or via commands
- Same agent can be used in multiple commands with different workflows
- Procedures can evolve without changing core expertise
- Clear responsibility boundaries

### The Rule

When writing agent files:
- ❌ NEVER include step-by-step workflows
- ❌ NEVER specify file paths or folder structures
- ❌ NEVER describe initialization sequences
- ❌ NEVER include "When invoked:" sections with actions
- ✅ DO describe what they know and how they think
- ✅ DO establish quality standards and principles
- ✅ DO define their domain expertise

When writing command files:
- ✅ DO include all execution workflows
- ✅ DO specify file paths and output locations
- ✅ DO describe when to invoke agents/commands
- ✅ DO include initialization and cleanup steps
- ❌ DON'T repeat the agent's domain knowledge
- ❌ DON'T redefine behavioral traits

## Two Main Styles

### Style 1: Structured Reference (Best for Complex Domains)
- **Highly consistent structure** with fixed sections
- **Checklist-heavy** with 8-item lists throughout
- **Formal workflows** with JSON communication protocols
- **Minimal prose**, maximum reference density
- **Inter-agent integration** explicitly defined
- **Length**: 250-300 lines
- **Example sources**: awesome-claude-code-subagents collection

### Style 2: Flexible Narrative (Best for Varied Complexity)
- **Adaptable structure** that scales with complexity
- **More explanatory prose** with complete sentences
- **Markdown section headings** for clear organization
- **Behavioral traits** and principles explicitly stated
- **Example interactions** showing typical requests
- **Length**: 30-170 lines depending on complexity
- **Example sources**: agents-main collection

Both styles are valid. Choose based on:
- **Structured** → Complex domain with many patterns, formal team collaboration
- **Flexible** → Varied complexity levels, more explanatory context needed

---

## Universal Components (Required for All Agents)

### 1. YAML Frontmatter

**Every agent must have:**
```yaml
---
name: agent-name-in-kebab-case
description: One or more sentences describing the agent's expertise and focus areas
---
```

**Optional frontmatter fields:**
```yaml
model: sonnet|opus  # Specify model if needed (opus for complex tasks)
tools: tool1, tool2, tool3  # List of tools/technologies used
```

**Description guidelines:**
- First sentence: Core expertise and specialization
- Optional: Add "Use PROACTIVELY for [scenarios]" to guide when to invoke
- Include key technologies, frameworks, or domains
- Keep under 2-3 sentences

**Examples:**
```yaml
# Minimal
description: Expert debugger specializing in root cause analysis. Use proactively when encountering any issues.

# Detailed
description: Expert C# developer specializing in modern .NET development, ASP.NET Core, and cloud-native applications. Masters C# 12 features, Blazor, and cross-platform development with emphasis on performance and clean architecture.

# With proactive guidance
description: Master TDD orchestrator specializing in red-green-refactor discipline, multi-agent workflow coordination, and comprehensive test-driven development practices. Use PROACTIVELY for TDD implementation and governance.
```

### 2. Opening Role Statement

**Format:** 
```markdown
You are [a/an] [expertise level] [role] [additional context about specialization and focus].
```

**Guidelines:**
- Always starts with "You are"
- Include expertise level: expert, senior, elite, master
- Define the core role clearly
- Add 1-2 phrases about specialization
- Can be one sentence (simple agents) or one paragraph (complex agents)

**Examples:**

Simple:
```markdown
You are an expert debugger specializing in root cause analysis.
```

Moderate:
```markdown
You are a senior Python developer with mastery of Python 3.11+ and its ecosystem, specializing in writing idiomatic, type-safe, and performant Python code. Your expertise spans web development, data science, automation, and system programming with a focus on modern best practices and production-ready solutions.
```

Complex:
```markdown
You are an elite content marketing strategist specializing in AI-powered content creation, omnichannel marketing, and data-driven content optimization.

## Expert Purpose
Master content marketer focused on creating high-converting, SEO-optimized content across all digital channels using cutting-edge AI tools and data-driven strategies. Combines deep understanding of audience psychology, content optimization techniques, and modern marketing automation to drive engagement, leads, and revenue through strategic content initiatives.
```

### 3. Core Knowledge Sections

**Every agent needs 3-8 sections** covering their domain knowledge. These can be:
- Patterns and practices
- Technologies and tools
- Methodologies and frameworks
- Common tasks and workflows
- Quality criteria and standards

**Format options:**

**Option A: Simple list with heading** (for simpler agents)
```markdown
Key responsibilities:
- Task one
- Task two
- Task three
```

**Option B: Multiple categorized sections** (for complex agents)
```markdown
Modern C# patterns:
- Record types for immutability
- Pattern matching expressions
- Nullable reference types discipline
- Async/await best practices

ASP.NET Core mastery:
- Minimal APIs for microservices
- Middleware pipeline optimization
- Dependency injection patterns
- Configuration and options
```

**Guidelines for lists:**
- Use 4-8 items per section (8 is most common in structured style)
- Be terse: avoid unnecessary articles (a, an, the)
- Use action phrases or noun phrases
- Include specific technologies/versions when relevant
- Prioritize practical, actionable items

---

## Optional Components (Include Based on Complexity)

The following components are organized into two categories: PERSONA elements (for agent files) and PROCEDURAL elements (for command files). **Be very careful to keep these separated.**

---

## PERSONA Components (For Agent Files)

These sections define the agent's identity, capabilities, and expertise. Include them in agent files based on complexity.

### 4. Tool Suite Description

**Purpose:** Document tools the agent knows and uses

**Format Option A: Simple frontmatter list**
```yaml
tools: Read, Write, Bash, pytest, black, mypy
```

**Format Option B: Detailed MCP Tool Suite section**
```markdown
## MCP Tool Suite
- **tool-name**: Description of what it does and when to use it
- **another-tool**: Its purpose and capabilities
- [5-10 tools typically]
```

**Include when:**
- Tools need explanation beyond their names
- Specific tool configurations or flags are important
- Agent uses specialized or custom tools

**Example:**
```markdown
## MCP Tool Suite
- **pytest**: Test execution, coverage reporting, fixture management
- **black**: Code formatting, style consistency, import sorting
- **mypy**: Static type checking, type coverage reporting
- **poetry**: Dependency resolution, virtual env management, package building
```

### 5. Capabilities Section (Flexible Style)

**Purpose:** Comprehensive breakdown of what the agent can do

**Format:**
```markdown
## Capabilities

### Major Capability Area 1
- 6-8 bulleted items
- More detailed than simple knowledge lists
- Can include specific technologies and versions
- May have sub-bullets for complex items

### Major Capability Area 2
[Continue with 8-12 subsections total]
```

**Include when:**
- Using flexible narrative style
- Agent has diverse, complex capabilities
- Need to organize knowledge by major domains

**Example:**
```markdown
## Capabilities

### Modern Analytics Platforms and Tools
- Advanced dashboard creation with Tableau, Power BI, Looker, and Qlik Sense
- Cloud-native analytics with Snowflake, BigQuery, and Databricks
- Real-time analytics and streaming data visualization
- Self-service BI implementation and user adoption strategies
```

### 6. Behavioral Traits

**Purpose:** Define how the agent approaches problems and makes decisions

**Format:**
```markdown
## Behavioral Traits
- Describes approach to work with verbs like "Prioritizes", "Emphasizes", "Focuses on"
- Explains decision-making principles
- Defines communication style
- States values and priorities
[8-10 items typical]
```

**Include when:**
- Using flexible narrative style
- Agent's approach and methodology matter
- Need to establish decision-making principles

**Example:**
```markdown
## Behavioral Traits
- Prioritizes production reliability and scalability over proof-of-concept implementations
- Implements comprehensive error handling and graceful degradation
- Focuses on cost optimization and efficient resource utilization
- Emphasizes observability and monitoring from day one
- Considers AI safety and responsible AI practices in all implementations
```

### 7. Knowledge Base

**Purpose:** List areas of deep expertise

**Format:**
```markdown
## Knowledge Base
- Area of expertise one
- Framework or methodology two
- Technology ecosystem three
[8-10 items typical]
```

**Include when:**
- Using flexible narrative style
- Important to establish credibility
- References specific methodologies or frameworks

### 8. Example Interactions

**Purpose:** Show what requests the agent handles well

**Format:**
```markdown
## Example Interactions
- "Specific request example with details and context"
- "Another example showing a different use case"
- "Third example demonstrating a key capability"
[6-8 examples typical]
```

**Include when:**
- Using flexible narrative style
- Agent's scope might be unclear
- Want to show breadth of capabilities

**Example:**
```markdown
## Example Interactions
- "Build a production RAG system for enterprise knowledge base with hybrid search"
- "Implement a multi-agent customer service system with escalation workflows"
- "Design a cost-optimized LLM inference pipeline with caching and load balancing"
```

### 9. Quality Standards Checklist

**Purpose:** Define quality criteria the agent applies (NOT execution steps)

**Format:**
```markdown
[Domain] quality standards:
- Quality criterion one with metric if applicable
- Standard two with specific threshold
- Principle three to uphold
- [4-8 total items]
```

**Include when:**
- Agent produces deliverables that need quality gates
- Specific metrics or standards must be met
- Defining "what good looks like" in the domain

**Examples:**

Quality standards (PERSONA - belongs in agent):
```markdown
Python code quality standards:
- Type hints for all function signatures and class attributes
- PEP 8 compliance with black formatting
- Comprehensive docstrings (Google style)
- Test coverage exceeding 90% with pytest
- Error handling with custom exceptions
```

**Note:** If your checklist contains execution steps or "do this then do that," it's PROCEDURAL and belongs in a command file, not an agent file.

### 10. Closing Statement

**Purpose:** Reinforce core priorities

**Format:**
```markdown
Always prioritize [value1], [value2], and [value3] while [additional context or constraint].
```

**Include when:**
- Using structured reference style
- Want to emphasize key principles
- Need to state critical priorities

**Examples:**
```markdown
Always prioritize performance, security, and maintainability while leveraging the latest C# language features and .NET platform capabilities.

Always prioritize code readability, type safety, and Pythonic idioms while delivering performant and secure solutions.

Always prioritize defect prevention, comprehensive coverage, and user satisfaction while maintaining efficient testing processes and continuous quality improvement.
```

---

## PROCEDURAL Components (For Command Files ONLY)

**WARNING:** These sections define execution workflows and should NEVER appear in agent files. They belong exclusively in command files.

### 11. "When invoked:" Section

**Purpose:** Defines initialization sequence with actions

**⚠️ COMMAND ONLY - Do NOT include in agent files**

**Format:**
```markdown
When invoked:
1. First action with specific details
2. Second action describing what to review
3. Third action about analysis needed
4. Fourth action about implementation approach
5. Optional fifth action
```

**Use in commands when:**
- Command has a clear startup sequence
- Multiple context-gathering steps are needed
- Workflow has dependencies that must execute in order

**Example (in a command file):**
```markdown
When invoked:
1. Load project context via `@commands/load-context.md`
2. Review project structure and package configuration
3. Analyze code style and testing conventions
4. Execute solution following established patterns
```

### 12. Execution Workflow

**Purpose:** Define step-by-step process for accomplishing tasks

**⚠️ COMMAND ONLY - Do NOT include in agent files**

**Format Option A: Structured workflow** (for complex processes)
```markdown
## Execution Workflow

Execute [task] through systematic phases:

### 1. [Phase Name]

[Description of what happens in this phase]

Steps:
- Specific action one
- Specific action two
- Specific action three

### 2. [Next Phase Name]

[Continue pattern]

### 3. [Final Phase Name]

[Completion criteria]
```

**Format Option B: Simple numbered steps** (for simpler processes)
```markdown
## Execution Steps

1. **First step** - Load context from project
2. **Second step** - Analyze requirements
3. **Third step** - Generate output
4. **Fourth step** - Write to tasks/ folder
[6-8 numbered steps typical]
```

**Use in commands when:**
- Task requires multiple sequential steps
- Actions must be performed in specific order
- File operations are involved

### 13. Primary Execution Checklist

**Purpose:** Define procedural steps to complete (NOT quality standards)

**⚠️ COMMAND ONLY - Do NOT include in agent files**

**Format:**
```markdown
[Task] execution checklist:
- [ ] Step one to perform
- [ ] Action two to complete
- [ ] Verification three to run
- [4-8 total items]
```

**Use in commands when:**
- Defining a "definition of done" with actions
- Listing procedural gates and verifications
- Creating execution checklists

**Examples:**

Execution checklist (PROCEDURAL - belongs in command):
```markdown
Design documentation checklist:
- [ ] Load project context via `@commands/load-context.md`
- [ ] Ask clarifying questions (3-5 initial)
- [ ] Create design document with diagrams
- [ ] Write output to tasks/design-{name}.md
- [ ] Show summary to user
```

### 14. Communication Protocol (Structured Style)

**Purpose:** Define how to invoke other agents or commands

**⚠️ COMMAND ONLY - Do NOT include in agent files**

**Format:**
```markdown
## Communication Protocol

### [Domain] Assessment

Initialize [process] by understanding [what's needed].

[Type] query:
```json
{
  "requesting_agent": "agent-name",
  "request_type": "get_[domain]_context",
  "payload": {
    "query": "Context needed: [specific information required]."
  }
}
```
```

**Use in commands when:**
- Formal communication protocols are needed
- Multi-agent collaboration is defined
- Structured reference style commands

### 15. Integration Steps with Other Agents

**Purpose:** Define collaboration workflow steps

**⚠️ COMMAND ONLY - Do NOT include in agent files**

**Format:**
```markdown
Integration workflow:
1. Invoke [agent-name] to [action]
2. Use output from [agent-name] for [purpose]
3. Call [command-name] to [action]
4. Coordinate with [agent-name] on [topic]
[6-8 items typical]
```

**Use in commands when:**
- Multi-agent workflows are needed
- Clear handoff points exist
- Orchestration is required

**Action verbs used:** Invoke, Call, Use, Coordinate, Pass to, Receive from, Collaborate with

---

## What NOT to Include in Agent Files

**CRITICAL: These elements are PROCEDURAL and belong in command files, NEVER in agent files.**

Agent files should define persona, not procedure. If you find yourself writing any of these in an agent file, STOP and move it to a command file instead:

### Procedural Elements to AVOID in Agents:

**❌ Step-by-step execution workflows**
```markdown
<!-- DON'T put this in an agent file -->
When invoked:
1. First load the context
2. Then ask questions
3. Finally write the output
```
Why: These are action sequences, not capabilities

**❌ File path specifications**
```markdown
<!-- DON'T put this in an agent file -->
Write output to tasks/design-{name}.md
Create files in the src/ directory
```
Why: Agents don't need to know where files go

**❌ Commands to invoke other agents/commands**
```markdown
<!-- DON'T put this in an agent file -->
Integration with other agents:
1. Call `@commands/load-context.md` first
2. Then invoke design-agent
3. Finally run `@commands/4-update-context.md`
```
Why: These are orchestration steps for commands

**❌ Initialization sequences that perform actions**
```markdown
<!-- DON'T put this in an agent file -->
When invoked:
1. Query context manager
2. Load project files
3. Analyze codebase
```
Why: These describe a workflow, not expertise

**❌ Document structure templates**
```markdown
<!-- DON'T put this in an agent file -->
Document format:
# Title
## Section 1
## Section 2
Write to: tasks/output.md
```
Why: Output format belongs in commands

**❌ Error handling procedures**
```markdown
<!-- DON'T put this in an agent file -->
If file not found:
1. Create the directory
2. Write a default file
3. Notify the user
```
Why: Error handling workflow is procedural

**❌ Status tracking and progress updates**
```markdown
<!-- DON'T put this in an agent file -->
Progress tracking:
{
  "status": "in_progress",
  "step": 3
}
```
Why: Workflow state is procedural

### What SHOULD Be in Agent Files:

**✅ Expertise and knowledge domains**
```markdown
<!-- This belongs in an agent file -->
Design expertise:
- System architecture patterns
- API design principles
- Data modeling approaches
```

**✅ Behavioral traits and approach**
```markdown
<!-- This belongs in an agent file -->
## Behavioral Traits
- Asks clarifying questions before assuming
- Considers multiple approaches
- Explains trade-offs clearly
```

**✅ Quality standards and principles**
```markdown
<!-- This belongs in an agent file -->
Design quality standards:
- Comprehensive problem statement
- Multiple alternatives considered
- Clear rationale documented
```

**✅ Communication style**
```markdown
<!-- This belongs in an agent file -->
## Communication Style
- Conversational and accessible
- Uses diagrams to clarify concepts
- Explains technical decisions in plain language
```

### The Test

Ask yourself: "Does this describe WHO the agent is, or WHAT STEPS to take?"

- WHO = Persona → Belongs in agent file
- WHAT STEPS = Procedure → Belongs in command file

---

## When You Need a Command File

Not every agent needs a companion command file. Here's how to decide:

### Agent File ONLY (No Command Needed)

Use just an agent file when:
- User invokes agent directly for their work
- No specific workflow or file operations required
- Agent provides expertise and assistance on-demand
- Examples: code review agents, debuggers, language specialists

**Example scenario:** User says "debug this error" → agent analyzes and suggests fixes (no command needed)

### Agent File + Command File (Both Needed)

Create both when:
- Multi-step procedural workflow is required
- Specific file operations (reading from/writing to locations)
- Must invoke other commands or agents
- Produces structured output in specific locations
- Has initialization or cleanup steps

**Example scenario:** User says "`@commands/1b-design.md` for payment system" → command orchestrates: load context, agent facilitates design, write to tasks/

### Signals You Need a Command File:

1. **File paths mentioned**: "Write output to tasks/" → needs command
2. **Workflow steps**: "First load context, then..." → needs command
3. **Invokes others**: "Call `@commands/load-context.md` before..." → needs command
4. **Specific output structure**: "Create file with template..." → needs command
5. **Error recovery procedures**: "If X fails, do Y..." → needs command

### Decision Tree

```
Is there a specific workflow with steps?
├─ NO → Agent file only
└─ YES → Does it involve file operations or invoking others?
    ├─ NO → Consider if workflow is simple enough for agent
    └─ YES → Agent file + Command file
```

---

## Decision Tree: What to Include

### For a Simple Agent (30-50 lines)

**PERSONA ONLY - No command file needed**

**Include:**
1. ✅ YAML frontmatter (minimal)
2. ✅ Opening role statement (1 sentence)
3. ✅ 1-2 knowledge sections
4. ✅ One quality standards checklist (optional)
5. ✅ Closing statement (optional)

**NEVER include:**
- ❌ "When invoked:" section (that's procedural)
- ❌ Execution workflows (that's procedural)
- ❌ File paths or locations (that's procedural)

**Example:** debugger, simple language specialists

### For a Moderate Agent (80-120 lines)

**PERSONA ONLY - Command file optional**

**Include:**
1. ✅ YAML frontmatter with tools
2. ✅ Opening role statement (1 paragraph)
3. ✅ 5-8 knowledge sections
4. ✅ Tool suite section OR capabilities section
5. ✅ Behavioral traits (optional)
6. ✅ Quality standards checklist (optional)
7. ✅ Closing statement

**NEVER include:**
- ❌ "When invoked:" workflows
- ❌ Communication protocols
- ❌ Integration steps
- ❌ Execution sequences

**When to add a command file:**
- If the agent needs to follow specific workflows
- If file operations or output locations are involved
- If it must invoke other commands/agents

**Example:** Most language specialists, domain-specific experts

### For a Complex Agent (140-300 lines)

**PERSONA + COMMAND SEPARATION REQUIRED**

Complex agents almost always need a companion command file to handle workflows. Keep the agent file focused on expertise and capabilities.

**Agent File (PERSONA) includes:**
1. ✅ YAML frontmatter with tools/model
2. ✅ Opening role statement + Purpose section
3. ✅ Capabilities section (8-12 subsections)
4. ✅ Behavioral Traits section
5. ✅ Knowledge Base section
6. ✅ Example Interactions section
7. ✅ Quality standards checklist
8. ✅ Closing statement

**Command File (PROCEDURE) includes:**
1. ✅ YAML frontmatter (name, description, agent reference, tools)
2. ✅ Purpose and usage section
3. ✅ Execution steps (numbered workflow)
4. ✅ "When invoked:" initialization sequence
5. ✅ File path specifications
6. ✅ Output templates and structures
7. ✅ Error handling procedures
8. ✅ Integration with other commands/agents

**CRITICAL: NO procedural elements in agent file**
- ❌ No "When invoked:" sections
- ❌ No execution workflows
- ❌ No file paths (tasks/, src/, etc.)
- ❌ No command invocation sequences
- ❌ No step-by-step procedures

**Example:** AI engineer (agent) + build-rag-system (command), TDD orchestrator (agent) + run-tdd-cycle (command)

---

## Writing Guidelines

### Language and Tone

**Be Terse:**
- ✅ "Code coverage exceeding 80%"
- ❌ "You should ensure that the code coverage is exceeding 80%"

**Use Active Voice:**
- ✅ "Implement type-safe patterns"
- ❌ "Type-safe patterns should be implemented"

**Minimize Articles:**
- ✅ "Review configuration, analyze patterns, implement solutions"
- ❌ "Review the configuration, analyze the patterns, implement the solutions"

**Use Present Tense:**
- ✅ "Analyzes performance bottlenecks"
- ❌ "Will analyze performance bottlenecks"

**Be Specific:**
- ✅ "TypeScript 5.0+ with strict mode enabled"
- ❌ "Modern TypeScript with type safety"

### List Structure

**Consistent Sizing:**
- Most lists should have 8 items (structured style)
- Minimum 4 items, maximum 10 items
- Use 6-8 items for capabilities (flexible style)

**Parallel Construction:**
- All items in a list should follow the same grammatical pattern
- ✅ All start with verbs: "Design, Implement, Optimize"
- ✅ All are noun phrases: "Type safety, Error handling, Performance"

**Progressive Specificity:**
- Start with broader items
- Move to more specific details
- End with edge cases or advanced topics

### Formatting Conventions

**Markdown Headings:**
- Structured style: Use ## for major sections, ### for subsections
- Flexible style: Use ## for all major sections, ### for capability areas
- Don't mix: Choose one pattern

**Bold vs. Italics:**
- **Bold**: Tool names, important terms, section labels
- *Italics*: Rarely used, mostly for emphasis in prose

**Code Blocks:**
- Use for JSON examples, command examples, code snippets
- Always specify language: ```json, ```markdown, ```python
- Keep examples realistic and useful

**Lists:**
- Use `-` for all bullet points (not `*` or `1.`)
- Indent sub-bullets with 2 spaces
- No blank lines between list items unless separating major groups

---

## Complete Examples

### Example 1: Simple Agent (Persona Only)

**Pure persona with no procedural elements**

```markdown
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
model: sonnet
---

You are an expert debugger specializing in root cause analysis.

## Debugging Expertise
- Error message and stack trace analysis
- Systematic hypothesis formation and testing
- Code inspection and state examination
- Root cause identification techniques
- Prevention strategy development

## Quality Standards
For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not just symptoms.
```

**Note:** This agent has NO "When invoked:" section, NO execution steps, NO file paths. Pure persona. The user invokes it directly for debugging help.

### Example 2: Complex Agent (Flexible Style - Persona Only)

**Comprehensive capabilities without procedures**

```markdown
---
name: ai-engineer
description: Build production-ready LLM applications, advanced RAG systems, and intelligent agents. Use PROACTIVELY for LLM features, chatbots, AI agents, or AI-powered applications.
model: opus
---

You are an AI engineer specializing in production-grade LLM applications, generative AI systems, and intelligent agent architectures.

## Purpose
Expert AI engineer specializing in LLM application development, RAG systems, and AI agent architectures. Masters both traditional and cutting-edge generative AI patterns, with deep knowledge of the modern AI stack.

## Capabilities

### LLM Integration & Model Management
- OpenAI GPT-4o/4o-mini, o1-preview with function calling
- Anthropic Claude 3.5 Sonnet with tool use
- Open-source models: Llama 3.1/3.2, Mixtral
- Local deployment with Ollama, vLLM
- Model serving with TorchServe, MLflow
- Multi-model orchestration strategies

### Advanced RAG Systems
- Production RAG architectures with multi-stage retrieval
- Vector databases: Pinecone, Qdrant, Weaviate, Chroma
- Embedding models: OpenAI, Cohere, BGE-large
- Hybrid search with vector and keyword matching
- Reranking with Cohere rerank-3
- Query decomposition and routing

[... additional capability sections ...]

## Behavioral Traits
- Prioritizes production reliability over proof-of-concept
- Implements comprehensive error handling
- Focuses on cost optimization
- Emphasizes observability from day one
- Considers AI safety in all implementations

## Knowledge Base
- Latest LLM developments and model capabilities
- Modern vector database architectures
- Production AI system design patterns
- AI safety and security considerations

Always prioritize production reliability, cost optimization, and responsible AI practices while delivering scalable LLM solutions.
```

**Note:** This agent defines WHAT it knows and HOW it thinks, but NO execution workflows, NO file paths, NO "when invoked" steps. Pure persona.

### Example 3: Agent + Command Pair (Proper Separation)

**Agent File: design-facilitator.md (PERSONA ONLY)**

```markdown
---
name: design-facilitator
description: Collaborative design expert specializing in facilitating exploratory design conversations, asking clarifying questions, and creating comprehensive design documentation.
tools: Read, mermaid
---

You are a senior design facilitator with expertise in collaborative design thinking, system architecture, and technical documentation.

## Design Expertise

### Broad Design Scope
- Feature design and user workflows
- System architecture and component design
- API design and integration patterns
- Data models and persistence strategies

### Collaborative Design Approach
- Exploratory questioning to understand intent
- Assumption surfacing and validation
- Constraint identification and documentation
- Trade-off analysis and decision capture

## Behavioral Traits

### Questioning Mindset
- Asks clarifying questions before jumping to solutions
- Probes for edge cases and error scenarios
- Seeks to understand user needs and business context
- Validates assumptions explicitly

### Contextual Awareness
- Considers existing project architecture and patterns
- Aligns designs with team conventions
- Respects technical constraints and dependencies
- Leverages established infrastructure

## Communication Style

### Exploratory Phase
- Ask open-ended questions to understand scope
- Probe for requirements and constraints
- Surface assumptions early
- Validate understanding frequently

### Design Phase
- Present design thinking transparently
- Explain rationale for architectural choices
- Offer alternatives with trade-offs
- Use diagrams to clarify complex interactions

Always approach design as a collaborative discovery process, recognizing that the best designs emerge from deep understanding of the problem space, thoughtful questioning, and alignment with existing project context.
```

**Command File: create-design.md (PROCEDURE ONLY)**

```markdown
---
name: create-design
description: Facilitates collaborative design conversations through clarifying questions, then creates comprehensive design documentation.
agent: agents/design/design-facilitator.md
tools: Read, Write, Bash, LS
---

This command enables collaborative design sessions that progress from initial concept to comprehensive documentation.

## Purpose

Use this command when you need to:
- Design new features or capabilities
- Plan system architecture changes
- Document technical approaches

## Execution Steps

### 1. Load Project Context

Invoke `@commands/load-context.md` to prime the session:
```bash
@commands/load-context.md
```

### 2. Understand Design Request

Analyze the user's prompt to identify:
- Design type (feature, system, API, data model)
- Design scope (new vs. modification)
- Design maturity (exploration vs. specification)

### 3. Clarifying Questions Phase

Engage in dialogue to uncover requirements.

Ask questions in categories:
- Core Requirements (3-5 questions)
- Context & Constraints (3-5 questions)
- Integration & Dependencies (3-5 questions)
- Edge Cases & Error Handling (3-5 questions)

### 4. Design Synthesis Phase

Create the design covering:
- Problem Statement
- Solution Overview
- Detailed Design (with diagrams)
- Implementation Considerations
- Alternatives Considered

### 5. Design Documentation Output

Write the design document to the tasks/ folder:

Filename: `tasks/design-{brief-descriptive-name}.md`

Document structure:
```markdown
# Design: {Title}

**Status**: Draft
**Created**: {YYYY-MM-DD}

## Overview
[Summary]

## Problem Statement
[Clear articulation]

## Solution Design
[Detailed approach]

## Implementation Guidance
[How to build]
```

Show completion message:
```
✅ Design document created: tasks/design-{name}.md
📋 Document includes: [sections]
💡 Next steps: Review and share with team
```

### 6. Iteration Support

Support multiple rounds of refinement until design is ready.

## Important Notes

- Always load context first
- Ask before assuming
- Document rationale
- Use diagrams
- Write to tasks/
```

**The Separation:**
- ✅ Agent: Expertise in design, questioning approach, communication style
- ✅ Command: Load context step, file paths (tasks/), workflow sequence, output template
- ❌ Agent does NOT say "write to tasks/"
- ❌ Command does NOT redefine design expertise

---

## Quality Checklist for Your Agent

Before finalizing an agent description, verify:

**Structure:**
- [ ] YAML frontmatter is complete and valid
- [ ] Opening role statement clearly defines expertise
- [ ] Sections are consistently formatted
- [ ] Lists are properly structured with 4-8 items
- [ ] One style (structured or flexible) is used consistently

**Persona vs. Procedure Separation:**
- [ ] Agent file contains ONLY persona elements (no procedures)
- [ ] NO "When invoked:" or workflow steps in agent
- [ ] NO file paths or output specifications in agent (tasks/, src/, etc.)
- [ ] NO command invocation sequences in agent
- [ ] Procedural elements moved to command file if needed
- [ ] Agent describes WHO they are, not WHAT STEPS to take

**Content:**
- [ ] Agent's scope and specialization are clear
- [ ] Key technologies and tools are mentioned
- [ ] Practical, actionable information is provided
- [ ] Specific versions or standards are included where relevant
- [ ] Domain expertise is evident
- [ ] Quality standards defined (not execution steps)

**Language:**
- [ ] Terse, action-oriented phrases used
- [ ] Present tense and active voice throughout
- [ ] Minimal use of articles (a, an, the)
- [ ] Parallel construction in lists
- [ ] Technical terminology is accurate

**Completeness:**
- [ ] All required sections for chosen complexity level
- [ ] Enough detail for effective agent behavior
- [ ] Not overly verbose or repetitive
- [ ] Examples or specifics where helpful

**Usability:**
- [ ] Easy to scan and find information quickly
- [ ] Clear organization with logical flow
- [ ] Reference material accessible
- [ ] Behavioral guidance is actionable

---

## Final Recommendations

1. **Separate Concerns**: Keep persona in agents, procedures in commands. This is THE most important rule.
2. **Start Simple**: Begin with minimal agent, expand as needed
3. **Be Consistent**: Choose a style and commit to it
4. **Be Specific**: Include versions, metrics, concrete examples
5. **Be Practical**: Focus on actionable information
6. **Be Scannable**: Use lists and clear structure
7. **Be Current**: Reference modern tools and practices
8. **Test It**: Use the agent and refine based on real usage
9. **Question Everything**: If it looks like a procedure, it probably doesn't belong in the agent

### The Golden Rule

**Agents describe WHO. Commands describe HOW TO.**

If you find yourself writing "First do X, then do Y" in an agent file, STOP. That's a procedure and belongs in a command file.

### When in Doubt

Ask yourself:
- "Am I describing expertise or execution?" → Expertise = agent, Execution = command
- "Am I listing capabilities or steps?" → Capabilities = agent, Steps = command
- "Am I defining quality standards or workflows?" → Standards = agent, Workflows = command
- "Am I explaining how to think or what to do?" → How to think = agent, What to do = command

An effective agent description serves as a **persona definition** that establishes expertise, approach, and quality standards. An effective command file provides the **procedural roadmap** that orchestrates workflows, file operations, and integrations. Keep them separate, and both become more powerful and reusable.

### Reference Well-Separated Examples

See these examples of proper persona/procedure separation:
- `design-facilitator.md` (agent) + `create-design.md` (command)
- Pure persona agents: `debugger.md`, language specialists

Learn from these examples and maintain the same discipline in your own agent and command files.


