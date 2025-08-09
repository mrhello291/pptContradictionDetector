# PowerPoint Contradiction Detector – Architecture & Data Flow

This document provides a **visual overview** of the PowerPoint Contradiction Detector's architecture and data flow.  
The tool is designed with a **modular pipeline** to handle document processing, AI analysis, and report generation in distinct stages.

---

## 1. High-Level Architecture Overview

```mermaid
flowchart LR
    A[ppt_contradiction_detector.py<br>(Main)] -->|1. Load| B[pptx_extractor.py<br>(Process & Extract)]
    B -->|3. Analyze| C[ai_analyzer.py]
    C -->|4. Generate Report| D[output_formatter.py]
    D -->|Save| E[reports/<br>.json, .md]
    C --> F[Google Gemini API<br>(gemini-2.5-flash)]
````

---

## 2. Detailed Data Flow

```mermaid
flowchart TD
    subgraph main[ppt_contradiction_detector.py]
        A1[Receives presentation.pptx]
    end

    subgraph extractor[pptx_extractor.py]
        B1[1. Convert PPTX → PDF<br>Tool: libreoffice<br>Output: /tmp/presentation.pdf]
        B2[2. Convert PDF → Images<br>Tool: magick<br>Output: /tmp/slide-*.jpg]
        B3[3. Extract Raw Text<br>Output: Raw text strings]
        B4[4. Bundle into List[SlideContent]<br>(text + image bytes)]
    end

    subgraph analyzer[ai_analyzer.py]
        C1[1. Construct Multimodal Prompt<br>Inputs: text, images, raw text]
        C2[2. Send to Gemini API<br>Model: gemini-2.5-flash]
        C3[3. Parse JSON Response<br>Output: List[Inconsistency]]
    end

    subgraph formatter[output_formatter.py]
        D1[1. Generate Report Formats<br>Text, JSON, Markdown]
        D2[2. Save to reports/<br>report.json, report.md]
    end

    main --> extractor
    extractor --> analyzer
    analyzer --> formatter
    analyzer --> F[Google Gemini API]
```

---

**Legend:**

* **ppt\_contradiction\_detector.py** → Orchestrates the full process.
* **pptx\_extractor.py** → Handles PPTX to PDF, PDF to images, and text extraction.
* **ai\_analyzer.py** → Builds prompts, calls Gemini API, and parses inconsistencies.
* **output\_formatter.py** → Generates and saves reports.

