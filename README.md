# Research Station Template

This is a GitHub Template Repository designed to act as a master "cookie cutter" for spinning up new, fully configured research environments in seconds.

## Directory Structure

*   `.github/copilot-instructions.md`: The "Brain" (Config) for Copilot.
*   `.vscode/settings.json`: Editor settings.
*   `research/`: Keeps folder empty but strictly for source material.
*   `drafts/`: Where you write new docs.
*   `PROMPTS.md`: Reusable command center for Copilot prompts.

## How to Use This Template

1.  **Enable Template Mode (if not already done)**:
    *   Go to the repository Settings on GitHub.
    *   Check the box "Template repository" (usually near the top of the General settings).

2.  **Generate a New Project**:
    *   Whenever you start a new topic, go to this repository on GitHub.
    *   Click the green "Use this template" button > "Create a new repository".
    *   Name it (e.g., `research-quantum-computing`).
    *   Clone it to VS Code. The folders and Copilot instructions are already there.

## Workflow

1.  **Ingestion**: Upload documents to the `research/` folder.
2.  **Prompting**: Use commands from `PROMPTS.md` in Copilot Chat to analyze, outline, and draft content based on your research.
3.  **Drafting**: Output goes into `drafts/`.

## VS Code Profile (Optional)

If you use specific extensions for research (like Markdown All in One or Paste Image), you can save them as a VS Code Profile.

1.  Click the Gear Icon (Manage) > Profiles > Create Profile.
2.  Name it "Research".
3.  Install your preferred writing extensions.
4.  When you open a research repo, switch to this profile.
