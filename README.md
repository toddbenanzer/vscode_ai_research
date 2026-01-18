# Research Station Template

This is a GitHub Template Repository designed to act as a master "cookie cutter" for spinning up new, fully configured research environments in seconds, optimized for GitHub Copilot.

## Features

*   **Zero-Config Start:** Ready to use immediately with sensible defaults.
*   **Data Hygiene:** Strict separation of `sources` (inputs) and `drafts` (outputs) to prevent AI hallucination loops.
*   **Persona-Based Writing:** Configurable personas (Strategic Partner, Data Scientist, Marketing Ops) controlled via `USER_SETTINGS.md`.
*   **Enterprise Governance:** Built-in PII/CSI scrubbing, mandatory citations, and "Internal Use Only" classification.
*   **Automated Workflow:** VS Code snippets (`research-start`, `research-synthesize`) automate context management and file naming.
*   **Safety Guards:** Strict Anti-Hallucination protocols and Chain-of-Thought reasoning enforcement.

## Prerequisites

Before using this template, ensure you have:
1.  **Visual Studio Code** installed.
2.  **GitHub Copilot Chat** extension installed and active.
3.  (Optional) **Markdown All in One** extension for better writing experience.

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

```mermaid
graph TD
    A[1. Plan: research-start] --> B[2. Ingest Sources: research-ingest]
    B --> C[3. Outline: research-outline]
    C --> D[4. Draft: research-draft]
    D --> E[5. Critique: research-critique]
    E -->|Refine| D
    D --> F[6. Synthesize: research-synthesize]
    B -->|Visualize| G[7. Diagram: research-diagram]
```

1.  **Initialization**: Open **Copilot Chat**. Type `research-start` to generate a structured `[Date]-Research-Plan-[Topic].md`.
2.  **Ingestion**: Upload **internal** documents to `workspace/sources/`. *Strictly NO PII.*
3.  **Configuration**: Open `USER_SETTINGS.md`. Uncomment your desired **Active Persona** (e.g., Strategic Partner) and **Active Format** (e.g., Email).
4.  **Analysis**: Type `research-ingest` to perform a Data Quality Assessment and identify key themes.
5.  **Drafting**:
    *   Type `research-outline` to structure your output.
    *   Type `research-draft` to write content. The AI will apply "Chain of Thought" reasoning before generating text.
6.  **Refinement**:
    *   Type `research-critique` to check Governance compliance and Logic.
    *   Type `research-synthesize` to generate a Decision-First Executive Summary.

## Quick Start Example

**Goal:** Write a Market Analysis for a new Deposit Product.

1.  **Setup:** Clone repo. Drop `market-data-Q3.pdf` into `workspace/sources/`.
2.  **Config:** In `USER_SETTINGS.md`, enable **Option 1: Strategic Partner** and **Option 1: Email**.
3.  **Chat:** Type `research-start`. Define your hypothesis.
4.  **Chat:** Type `research-ingest`. Review data quality flags.
5.  **Chat:** Type `research-synthesize`. Copilot generates a "Decision -> Rationale -> Impact" summary table.

## Configuration Options

You can toggle between these pre-defined styles in `USER_SETTINGS.md`:

*   **Personas:** Strategic Partner (Exec), Analytics Peer (Data Scientist), Marketing Operations.
*   **Formats:** Email (Action-Oriented), Scenario Analysis, PowerPoint JSON, A/B Test Plan, SQL/Python Code.

## Best Practices

*   **One Topic Per Repo:** Keep repositories scoped to a single research topic to maintain context clarity.
*   **Source Limits:** For best performance, keep individual source files under 10MB.
*   **Review Settings:** Before starting a new draft, always double-check `USER_SETTINGS.md` to ensure the correct Persona is active.

## Extending the Template

To add your own custom Personas:
1.  Open `USER_SETTINGS.md`.
2.  Copy an existing block (e.g., the Executive block).
3.  Modify the **Role**, **Tone**, and **Constraints**.
4.  (Advanced) To modify core logic (e.g., citation rules), edit `.github/copilot-instructions.md`.

## Troubleshooting

*   **AI is Hallucinating:** Check `workspace/sources/`. Are your source files there? The AI strictly adheres to the "Citation Rule" and will not invent facts if sources are missing.
*   **Context Amnesia:** If the AI "forgets" your Outline or Plan, ensure the file is **open** in your editor. While the system can read the workspace, having the file open guarantees it is in the immediate context window.
*   **Wrong Tone:** Check `USER_SETTINGS.md`. Did you accidentally leave two personas uncommented? Ensure only one is active.
*   **"System Integrity" Error:** You tried to ask the AI to modify `PROMPTS.md` or `USER_SETTINGS.md`. The protocol strictly forbids this to prevent accidental breakage. Edit these files manually.

## License

MIT
