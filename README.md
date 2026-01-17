# Research Station Template

This is a GitHub Template Repository designed to act as a master "cookie cutter" for spinning up new, fully configured research environments in seconds.

## Directory Structure

*   `.github/copilot-instructions.md`: The "Brain" (Config) for Copilot.
*   `.vscode/research.code-snippets`: Pre-defined prompts accessible via snippets.
*   `workspace/inputs/`: Place source materials here.
*   `workspace/outputs/`: Generated drafts go here.
*   `PROJECT_CONFIG.md`: Central configuration for Styles (Personas/Formats) and Rules.

## How to Use This Template

1.  **Enable Template Mode (if not already done)**:
    *   Go to the repository Settings on GitHub.
    *   Check the box "Template repository".

2.  **Generate a New Project**:
    *   Click "Use this template" > "Create a new repository".
    *   Name it (e.g., `research-quantum-computing`).
    *   Clone it to VS Code.

## Workflow

1.  **Ingestion**: Upload documents to `workspace/inputs/`.
2.  **Configuration**: Edit `PROJECT_CONFIG.md` to define your desired **Persona** (e.g., Executive, Casual) and **Format** (e.g., Email, PowerPoint).
3.  **Prompting**: Open Copilot Chat and type the following snippets to trigger prompts:
    *   `research-ingest`: Analyze documents.
    *   `research-outline`: Generate an outline.
    *   `research-draft`: Draft content applying the active style from `PROJECT_CONFIG.md`.
4.  **Drafting**: Output goes into `workspace/outputs/`.
