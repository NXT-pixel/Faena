# System Patterns & Architecture
**Created**: 2026-10-25T03:19:55.675128+00:00

## Core Design Principles
1. **Persona vs Procedure**: Agents define WHO; Commands define HOW TO; Faena runs THE FLOW.
2. **TDD Discipline**: Tests written first (RED), code implemented (GREEN), quality gates verified (VERIFY).
3. **Multi-Provider Agnostic**: Code execution works identically with Claude, ChatGPT, Gemini, Ollama, etc.
4. **Clean Artifact Lifecycle**: Transient task files drive autonomous execution; results are committed cleanly.
