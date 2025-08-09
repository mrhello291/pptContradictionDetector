# Conda Environment Setup Guide

This guide shows how to set up and use the PowerPoint Contradiction Detector with conda.

## 🆕 Method 1: Create New Environment from requirements.txt

To create a new environment from scratch:

```bash
# Create a new conda environment with Python 3.9
conda create -n ppt-detector python=3.9 -y

# Activate the environment
conda activate ppt-detector

# Install Python dependencies
pip install -r requirements.txt
````

## 🛠️ Method 2: Install External Tools

This project relies on external command-line tools. You must install them on your host system for the conversion pipeline to work.

  - **On Linux (Debian/Ubuntu):**
    ```bash
    sudo apt-get install libreoffice imagemagick
    ```
  - **On macOS (Homebrew):**
    ```bash
    brew install libreoffice imagemagick
    ```
  - **On Windows:**
    Download and install from the official websites.

## 🔑 API Key Setup

1.  **Get Gemini API Key**:

      - Visit: https://aistudio.google.com/app/apikey
      - Create a new API key
      - Copy the key

2.  **Set API Key**:

    ```bash
    # Edit .env file (assuming you have one)
    nano .env

    # Change this line:
    GEMINI_API_KEY=your_actual_api_key_here
    ```

## 🎯 Usage Examples

```bash
# Activate environment first
conda activate ppt-detector

# Basic analysis
python ppt_contradiction_detector.py presentation.pptx

# With JSON and Markdown output
python ppt_contradiction_detector.py presentation.pptx --json --markdown
```

## 🗂️ Environment Management

```bash
# List conda environments
conda env list

# Activate environment
conda activate ppt-detector

# Deactivate environment
conda deactivate

# Remove environment (if needed)
conda env remove -n ppt-detector
```

## 🚨 Troubleshooting

**Command not found (e.g., `magick` or `libreoffice`)**:

  - Ensure the external tools are installed on your host system (e.g., via `sudo apt-get`).
  - If you're on Windows, make sure the installation directories are in your system's `PATH`.

**API key errors**:

  - Check that your `.env` file is in the project root.
  - Ensure the `GEMINI_API_KEY` is not empty and is correct.

## 🎉 You're Ready\!

Your environment is set up and ready to use. Just add your Gemini API key to the `.env` file and start analyzing PowerPoint presentations for contradictions\!
