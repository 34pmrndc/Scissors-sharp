---
name: "Scissors#"
description: "Reviews, refactors, and optimizes source code files to reduce token size and suggest software quality enhancements."
---

# Scissors# Agent Skill Guide

This skill equips agentic coders (such as Claude Code, Codex, and Gemini) with guidelines and automated tools to review, refactor, and compress source code files. By eliminating redundant spacing, comments, docstrings, and dead imports, the agent dramatically decreases context window token usage while providing suggestions to improve structural quality.

---

## 🛠️ Triggers & Activation

Activate this skill when the user asks to:
*   *"Reduce the token size of this code/file"*
*   *"Optimize this file/folder for tokens"*
*   *"Review this codebase and suggest improvements"*
*   *"Run Scissors# on <file_path>"*
*   *"Prune dead code and comments"*

---

## 📋 Instructions for the Executing Agent

When this skill is triggered, you must perform the following actions on the targeted source code files:

### 1. Programmatic Optimization (Token Pruning)
For maximum efficiency, you can run the automated optimization script located in `scripts/optimize.py`:
```bash
python .agents/skills/scissors-sharp/scripts/optimize.py --file <path_to_file>
```
If executing manually or on languages not fully covered by the script, follow these pruning rules:
*   **Remove Code Comments:** Strip out single-line comments (`#` in Python, `//` in JS) and block comments (`/* ... */` in JS/CSS) unless they contain critical license/copyright info.
*   **Strip Docstrings:** For Python, remove multi-line string literals used as docstrings.
*   **Compress Whitespace:** Collapse multiple consecutive empty lines to a single blank line, and strip trailing whitespaces.
*   **Clean Unused Imports:** Identify and remove imports that are declared but never referenced in the active scope.

> [!WARNING]
> **Functional Integrity:** Never rename variables, modify business logic, or change API signatures unless explicitly asked. The code's behavior must remain identical.

### 2. Contextual Quality Audit
Analyze the code structure and provide a concise, bulleted markdown report detailing:
1.  **Complexity Analysis:** Identify areas of deep nesting or high cyclomatic complexity.
2.  **SOLID & DRY Adherence:** Point out duplicated logic or violations of single responsibility.
3.  **Actionable Suggestions:** Write concrete refactoring suggestions showing *before* and *after* snippets.
4.  **Token Savings:** Report the original file size, the optimized file size, and the percentage of token space saved.
