# Design Specification: The Lenny Growth Assistant

## 1. UI/UX Principles
- **Clarity over Clutter:** The interface should prioritize the conversation and the resulting artifacts. Navigation and settings should be accessible but out of the way.
- **Responsive Dual-Pane:** The core experience revolves around a split view. On desktop, this is a 50/50 or 40/60 split between Chat and Artifacts. On mobile, the Artifact view should overlay or stack below the chat.
- **Immediate Feedback:** Streaming text generation is crucial. The user must see the tokens appearing instantly to perceive the local model as fast.
- **Trust via Transparency:** The provider (Local vs. Cloud) and the retrieved sources should be explicitly visible in the UI.

## 2. Information Architecture
### Global Layout
- **Sidebar (Collapsible):** Chat history/sessions.
- **Main Content Area:**
  - **Left Column:** The Chat Interface.
  - **Right Column:** The Artifact Viewer (appears conditionally when an artifact is generated).

### Key Interaction States
- **Empty State:** Greeting message, brief explanation of capabilities (e.g., "Ask about growth loops, or ask for a Ship 30 for 30 essay"), and a clear model selector toggle (Ollama vs. Claude).
- **Retrieving State:** While waiting for the DB vector search, a small loading indicator (e.g., "Searching Lenny's Transcripts...") appears in the chat bubble.
- **Streaming State:** Text appears progressively. If an artifact tag (`<artifact>`) is detected in the stream, the right pane slides open and a loading skeleton appears until the artifact generation is complete.
- **Artifact Viewing State:** The right pane is fully open, displaying either styled Markdown or a rendered HTML page.

## 3. The Artifact Viewer (Claude-Style)
The Artifact Viewer is a dedicated space for complex outputs that would clutter a standard chat feed.

- **Trigger:** The LLM generates specific XML-like tags, e.g., `<artifact type="html" title="Growth Loop Framework">...content...</artifact>`.
- **Parsing:** The frontend intercepts these tags during the stream. It extracts the content and prevents the raw XML tags from displaying in the chat bubble. Instead, it replaces them in the chat with a clickable "View Artifact: [Title]" button.
- **Rendering:**
  - If `type="markdown"`, render using `react-markdown`.
  - If `type="html"`, sanitize with `DOMPurify` and render inside the sandboxed `<iframe srcDoc={content}>`.

## 4. Accessibility (a11y) Considerations
- **Contrast:** Ensure text contrast meets WCAG AA standards (especially for code syntax highlighting).
- **Keyboard Navigation:** The chat input should be auto-focused. Users should be able to submit with `Enter` (and `Shift+Enter` for newlines). The Artifact viewer toggle must be reachable via `Tab`.
- **Screen Readers:** Use `aria-live="polite"` on the streaming chat bubble so screen readers announce the response updates without aggressively interrupting.

## 5. Visual Design (Tailwind CSS)
- **Typography:** Inter or system sans-serif for clean, modern readability.
- **Color Palette:**
  - Backgrounds: Very light gray (`bg-gray-50`) for the app background, white (`bg-white`) for chat bubbles and the artifact pane.
  - Accents: A subtle primary color (e.g., Indigo `text-indigo-600` or Emerald `text-emerald-600` to signify growth).
  - Borders: Soft borders (`border-gray-200`) to separate the panes.
- **Animations:** Smooth slide-in transitions when the Artifact Viewer opens (`transition-all duration-300 ease-in-out`).
