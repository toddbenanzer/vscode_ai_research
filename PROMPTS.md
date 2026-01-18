# Research Assistant Prompt Library
**IMPORTANT:** Resolve all bracketed placeholders (e.g., `[TOPIC]`, `[YYYY-MM-DD]`) with actual values from the context before generating output.

## Plan
Create a new file named "[YYYY-MM-DD]-Research-Plan-[TOPIC].md" in the output directory. Use the following structure (adhering to the Enterprise Metadata standard):

**Metadata:** Date: [YYYY-MM-DD] | Confidence: High | Status: Plan

# Research Plan: [TOPIC]
## 1. Objectives
- [ ] Define the primary goal.
## 2. Key Questions
- [ ] Question 1?
- [ ] Question 2?
## 3. Hypotheses
- Hypothesis A...
## 4. Risk Assessment
- [ ] Risk 1: (e.g., Data Gaps, Regulatory concerns)
## 5. Source Material Checklist
- [ ] Document 1...

## Ingest
Analyze the uploaded documents in the source materials.
1.  **Data Quality Assessment**: Explicitly flag any missing data, ambiguous definitions, or conflicting reports.
2.  **Key Findings**: Identify key themes and significant data points regarding the topic.

## Outline
Create a detailed outline for a new output titled "[INSERT TITLE]" based on the key themes in the source materials. Ensure the structure aligns with the Active Format in `USER_SETTINGS.md`.

## Draft
**Chain of Thought**: Briefly reason about the Active Persona's constraints and the source data availability before writing.
**Task**: Write the "[INSERT SECTION NAME]" section. If an active file is provided, append to it; otherwise, suggest a new file in the output directory. Apply the active Persona and Format defined in `USER_SETTINGS.md`.

## Critique
Act as a 'Devil's Advocate'. Critique the provided draft context:
1.  **Logic & Evidence**: Identify fallacies, missing evidence, or ignored alternative interpretations.
2.  **Governance Compliance**: Verify strict adherence to PII/CSI scrubbing and Citation rules.
3.  **Persona Fidelity**: Ensure the tone and structure match `USER_SETTINGS.md`.

## Diagram
Create a Mermaid.js diagram (e.g., Mindmap, Flowchart, or Sequence) to visualize the relationship between key concepts based on the source materials. Ensure the output is wrapped in a markdown code block tagged `mermaid`.

## Synthesize
Create an Executive Summary based on the provided context.
1.  **Structure**: Strictly follow the pattern: **Decision Required** -> **Strategic Rationale** -> **Impact**.
2.  **Constraint**: Limit to 3 paragraphs max.
3.  **Governance**: Ensure strict PII scrubbing and citations.
