---
name: "Scissors#"
description: "Reviews, refactors, and optimizes source code files to reduce token size and suggest software quality enhancements."
---

# Scissors# Agent Skill Guide (v1.2.0)

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

When this skill is triggered, you must perform the refactoring strictly following these sequential stages:

### Stage 1: Token Shield & Ignored Directories (CRITICAL)
1.  **DO NOT** read or scan files inside dependency, packaging, or auto-generated directories. These include: `node_modules/`, `.next/`, `.venv/`, `dist/`, `build/`, `.git/`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`.
2.  **Verify Exclusions:** Check if a `.claudeignore` file exists in the project root. If it is missing, proactively create it containing the above exclusions to protect the user's API token budget.
3.  **Token Budget Limit:** If a single target file exceeds **100 KB** (or approx. **1,500 lines**), warn the user and request confirmation before loading its contents into the context window.
4.  **Batch Processing:** When optimizing multiple files, process them in batches of **maximum 5 files at a time** and ask the user for permission before proceeding to the next batch.

### Stage 2: Local Execution Mandate (0 API Token Cleaning)
To save API tokens, **NEVER** rewrite or clean comments directly in the chat interface. You must use the local execution script:
1.  Run the automated optimization script locally on the user's machine:
    ```bash
    python .agents/skills/scissors-sharp/scripts/optimize.py --file <path_to_file> --overwrite
    ```
2.  Since the script runs directly on the local CPU, this process consumes **0 API tokens** for the cleaning itself.

### Stage 3: Quality Audit & Concise Reporting
After the local script runs, read only the console output and provide a highly concise markdown report in the chat:
1.  **Summary Table:** Show only the original size, optimized size, estimated tokens saved, and the percentage of token space saved.
2.  **Contextual Suggestions:** List up to 4 high-value code quality suggestions (e.g. cyclomatic complexity, hardcoded secrets, SOLID/DRY violations) without printing the entire file code in the chat.
3.  **No Code Dumping:** Never dump the full original or optimized code in your response unless explicitly requested by the user.
