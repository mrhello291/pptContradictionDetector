# PowerPoint Contradiction Detector – Architecture & Data Flow

This document provides a **visual overview** of the PowerPoint Contradiction Detector's architecture and data flow.  
The tool is designed with a **modular pipeline** to handle document processing, AI analysis, and report generation in distinct stages.

---

## 1. High-Level Architecture Overview

```mermaid
flowchart LR
    A["ppt_contradiction_detector.py (Main)"] -->|1. Load| B["pptx_extractor.py (Process & Extract)"]
    B -->|3. Analyze| C["ai_analyzer.py"]
    C -->|4. Generate Report| D["output_formatter.py"]
    D -->|Save| E["reports (JSON, MD)"]
    C --> F["Google Gemini API (gemini-2.5-flash)"]
````

---

## 2. Detailed Data Flow

```mermaid
flowchart TD
    subgraph main["ppt_contradiction_detector.py"]
        A1["Receives presentation.pptx"]
    end

    subgraph extractor["pptx_extractor.py"]
        B1["1. Convert PPTX → PDF — Tool: libreoffice — Output: /tmp/presentation.pdf"]
        B2["2. Convert PDF → Images — Tool: magick — Output: /tmp/slide-*.jpg"]
        B3["3. Extract Raw Text — Output: raw text strings"]
        B4["4. Bundle into List (SlideContent) — (text + image bytes)"]
    end

    subgraph analyzer["ai_analyzer.py"]
        C1["1. Construct multimodal prompt — Inputs: text, images, raw text"]
        C2["2. Send to Gemini API — Model: gemini-2.5-flash"]
        C3["3. Parse JSON response — Output: List (Inconsistency)"]
    end

    subgraph formatter["output_formatter.py"]
        D1["1. Generate report formats — Text, JSON, Markdown"]
        D2["2. Save files — reports/report.json, reports/report.md"]
    end

    main --> extractor
    extractor --> analyzer
    analyzer --> formatter
    analyzer --> F["Google Gemini API"]
```

---

**Legend:**

* **ppt\_contradiction\_detector.py** → Orchestrates the full process.
* **pptx\_extractor.py** → Handles PPTX → PDF, PDF → images, and text extraction.
* **ai\_analyzer.py** → Builds prompts, calls Gemini API, and parses inconsistencies.
* **output\_formatter.py** → Formats and saves reports (console / JSON / Markdown).

