# Product Requirements Document (PRD): The Lenny Growth Assistant

## 1. Overview
The Lenny Growth Assistant is a full-stack, enterprise-grade, retrieval-augmented generation (RAG) web application designed to unlock operational knowledge from Lenny’s Podcast transcripts.

## 2. User & Problem
**Primary User:** Growth Product Managers and Growth Leaders.
**Job to be Done:** Extracting actionable growth tactics, mental models, and operational frameworks from over 200+ hours of podcast audio.
**Pain Point:** Listening to hours of podcasts or reading hundreds of pages of unstructured transcripts to find a specific framework or piece of advice is extremely time-consuming and inefficient. Users need instant, actionable insights grounded in trusted material.

## 3. Success Metrics
- **Retrieval Citation Accuracy:** $\ge 90\%$ of generated claims must be directly attributable to a retrieved transcript chunk.
- **Local Inference Latency:** $< 4$ seconds to the first generated token when using the local Ollama model.
- **Artifact Render Safety:** 0 Cross-Site Scripting (XSS) vulnerabilities or sandbox escapes when rendering generated HTML/CSS artifacts.

## 4. Scope
### In Scope
- Text-based chat interface.
- Dual-pane layout with chat on the left and an artifact viewer on the right.
- Grounding answers strictly in Lenny's Podcast transcripts.
- Generating "Ship 30 for 30" style essays based on transcript insights.
- Rendering safe Markdown and HTML/CSS artifacts in a sandboxed iframe.
- Support for dual models: Local (Ollama) and Cloud (Anthropic/OpenAI) with seamless switching.
- Single command deployment via `docker-compose`.

### Out of Scope
- User authentication/authorization (single tenant assumed for this phase).
- Audio transcription (we are assuming text transcripts are pre-provided).
- Managing or interacting with external APIs (other than the configured LLMs).
- Advanced analytics or dashboarding of user queries.

## 5. Assumptions
- The user is deploying this on a machine with at least 4 cores and 16 GB RAM (M1/M2/M3/M4 Apple Silicon or equivalent Windows/Linux with CUDA).
- The transcripts repository provided contains standard Markdown or TXT files.
- The evaluator has Docker and Docker Compose installed.
- For cloud evaluation, the evaluator possesses a valid Anthropic or OpenAI API key.

## 6. Risks and Trade-offs
- **Hallucination vs. Grounding:** We prioritize grounding over conversational fluency. If the context does not contain the answer, the model is strictly instructed to state it does not have sufficient information.
- **Local Model Quality vs. Privacy/Cost:** Local models (like Llama 3.2 3B) are fast and private but may struggle with highly complex reasoning compared to Claude 3.5 Sonnet. We mitigate this by clearly separating the "Ship 30 for 30" prompt skill, forcing a strong structural framework on the local model.
- **Latency vs. Context Size:** We limit chunk retrieval to top $K=4-6$ to ensure the context window remains small enough for fast local inference latency.
- **Artifact Security:** Generating HTML introduces XSS risks. We trade off complex interactivity (like calling external APIs from within the artifact) for security by using `DOMPurify` and a strict iframe `sandbox="allow-scripts"` (without `allow-same-origin`).

## 7. Core Flows
1. **Chat:** User inputs query -> Backend embeds query -> pgvector retrieves top chunks -> Prompt constructed -> LLM streams response.
2. **Ship 30 for 30 Skill:** User selects "Ship 30" mode -> System uses standard retrieval -> Backend wraps context in the Ship 30 for 30 instruction prompt -> LLM streams essay.
3. **Artifact Rendering:** LLM generates `<artifact type="html">...content...</artifact>` -> Frontend parses tag -> Cleans content -> Mounts in sandboxed iframe in the right pane.
