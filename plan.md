# TiaRa: Multi-Modal Agentic Desktop Assistant

## Goal Description
Build a multi-modal, agentic desktop assistant ("TiaRa") that evolves through 7 phases, starting from a basic voice assistant to a fully autonomous, multi-agent system with screen understanding, long-term memory, and full computer control. The system will use Python for the core logic, React/Electron for the UI, and integrate various ML models for speech, vision, and reasoning.

---

## Phase-Wise Execution Plan

### Phase 1: Voice Assistant (Currently Implementing)
* Wake word detection ("TiaRa")
* Speech-to-text
* Natural conversation
* Text-to-speech with a realistic voice

**Example Interaction:**
- You: "TiaRa" -> Assistant wakes.
- You: "Open VS Code." -> VS Code launches.
- You: "Search for cybersecurity internships." -> Browser opens with the search.

**Phase 1 Tech Stack (Optimized for Apple Silicon M2):**
- **LLM Engine**: Ollama (running a model like Llama 3 locally).
- **Speech-to-Text**: Whisper (runs locally).
- **Text-to-Speech**: macOS Built-in `say` command (extremely fast).

### Phase 2: Full Computer Control
Your assistant can:
* Open any application, close apps, type text, move the mouse, click buttons.
* Read the screen, create folders, rename files, download files.
* Control music, adjust brightness/volume, take screenshots, manage emails, use browsers automatically.
* **Tech**: Desktop automation frameworks and accessibility APIs (e.g., PyAutoGUI, macOS AppKit).

### Phase 3: Vision (Camera)
* Captures a camera frame and responds to visual questions.
* E.g., "TiaRa, look at my desk. What do you see?" or "Is someone behind me?"
* *Note: This will always require explicit permission to access the camera.*
* **Tech**: OpenCV, Vision-capable LLMs (e.g., LLaVA, GPT-4o).

### Phase 4: Screen Understanding
Instead of only controlling the computer blindly, it understands what’s on the screen.
* E.g., "Fill this form." It sees the webpage and completes it.
* E.g., "Click the green button." It identifies the button visually and clicks it.

### Phase 5: Long-Term Memory
TiaRa remembers things like:
* Your projects, coding style, frequently used apps.
* Daily routine, preferred browser, files you work on.
* Over time it becomes more personalized.
* **Tech**: Vector database (e.g., ChromaDB, FAISS) + SQLite.

### Phase 6: Autonomous Agents
You could say: "Find the best laptop under ₹80,000, compare five options, make an Excel sheet, and email it to me."
TiaRa would:
1. Search online.
2. Compare products.
3. Create a spreadsheet.
4. Write a summary.
5. Send the email.

### Phase 7: Multi-Agent System
Instead of one AI, have specialized agents coordinated by a Planning Agent:
* **Coding Agent**: Writes and debugs code.
* **Research Agent**: Browses and summarizes information.
* **Security Agent**: Monitors your system.
* **Automation Agent**: Performs desktop tasks.
* **Vision Agent**: Handles camera and screen analysis.
* **Planning Agent**: Manages your schedule, reminders, and delegates to other agents.

---

## Overall Technologies
* **Programming language**: Python (primary)
* **Frontend**: React or Electron for a desktop UI
* **Desktop control**: Accessibility APIs and automation libraries
* **LLM**: Local model via Ollama (or GPT if API preferred later)
* **Speech**: Whisper (STT) + macOS say (TTS)
* **Vision**: Camera input + vision models
* **Memory**: Vector database + SQLite
* **Operating systems**: macOS (optimized for M2) and Windows compatibility planned.
