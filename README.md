# Research Station Template

This is a GitHub Template Repository designed to act as a master "cookie cutter" for spinning up new, fully configured research environments in seconds.

## Directory Structure

*   `USER_SETTINGS.md`: The main config file. Edit this to set your Persona and Format.
*   `workspace/sources/`: Place all source materials (PDFs, docs) here.
*   `workspace/drafts/`: Generated drafts go here.
*   `.github/copilot-instructions.md`: The "Brain" (Protocol) for Copilot. Points to USER_SETTINGS.md.
*   `PROMPTS.md`: The collection of research prompts.
*   `.vscode/research.code-snippets`: Pre-defined prompts accessible via snippets.

## How to Use This Template

1.  **Enable Template Mode (if not already done)**:
    *   Go to the repository Settings on GitHub.
    *   Check the box "Template repository".

2.  **Generate a New Project**:
    *   Click "Use this template" > "Create a new repository".
    *   Name it (e.g., `research-quantum-computing`).
    *   Clone it to VS Code.

## Workflow

1.  **Ingestion**: Upload documents to `workspace/sources/`.
2.  **Configuration**: Edit `USER_SETTINGS.md` to define your desired **Active Persona** (e.g., Executive) and **Active Format** (e.g., Email).
3.  **Prompting**: Open Copilot Chat and type the following snippets to trigger prompts:
    *   `research-ingest`: Analyze documents in `workspace/sources/`.
    *   `research-outline`: Generate an outline.
    *   `research-draft`: Draft content applying the active style.
    *   `research-critique`: Critique the current active draft.
4.  **Drafting**: Output will be generated in `workspace/drafts/`.
