# Research Station Template

This is a GitHub Template Repository designed to act as a master "cookie cutter" for spinning up new, fully configured research environments in seconds, optimized for GitHub Copilot.

## Features

*   **Zero-Config Start:** Ready to use immediately with sensible defaults.
*   **Data Hygiene:** Strict separation of `sources` (inputs) and `drafts` (outputs) to prevent AI hallucination loops.
*   **Persona-Based Writing:** Configurable personas (Executive, Academic, etc.) controlled via `USER_SETTINGS.md`.
*   **Automated Workflow:** VS Code snippets (`research-start`, `research-draft`) automate context management and file naming.
*   **Safety Guards:** Built-in protocols prevent code generation, enforce citation rules, and protect system configuration files.

## Directory Structure

*   `USER_SETTINGS.md`: The main config file. Edit this to set your Active Persona and Format.
*   `PROMPTS.md`: The centralized library of research prompts (Ingest, Outline, Draft, Critique).
*   `workspace/`: The main work area.
    *   `sources/`: Place all source materials (PDFs, docs) here. Includes a guidance `README.md`.
    *   `drafts/`: Generated drafts go here. Includes a hygiene warning `README.md`.
*   `.github/copilot-instructions.md`: The "Brain" (Protocol) for Copilot. Enforces rules like "No Code" and "System Integrity".
*   `.vscode/research.code-snippets`: Pre-defined prompts accessible via snippets.
*   `.gitignore`: Prevents binary source files (PDF, DOCX) from bloating the repo.

## How to Use This Template

1.  **Enable Template Mode (if not already done)**:
    *   Go to the repository Settings on GitHub.
    *   Check the box "Template repository".

2.  **Generate a New Project**:
    *   Click "Use this template" > "Create a new repository".
    *   Name it (e.g., `research-quantum-computing`).
    *   Clone it to VS Code.

## Workflow

1.  **Initialization**: Open Copilot Chat and type `research-start` to generate a structured `RESEARCH_PLAN.md`.
2.  **Ingestion**: Upload documents to `workspace/sources/`.
3.  **Configuration**: Edit `USER_SETTINGS.md` to define your desired **Active Persona** (e.g., Executive) and **Active Format** (e.g., Email).
4.  **Analysis**: Use `research-ingest` to identify key themes and conflicts in your sources.
5.  **Drafting**:
    *   Use `research-outline` to structure your thoughts.
    *   Use `research-draft` to write content. The AI will apply your active style and append to your open file.
6.  **Refinement**:
    *   Use `research-critique` to stress-test your draft against the sources.
    *   Use `research-diagram` to visualize complex relationships.
