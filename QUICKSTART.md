# Quick Start Guide

Get up and running with the PowerPoint Contradiction Detector in 3 minutes!

## 🚀 Installation

1. **Install dependencies**
   ```bash
   python setup.py
   ```

2. **Set up your Gemini API key**
   - Get your API key from: https://makersuite.google.com/app/apikey
   - Edit the `.env` file that was created:
   ```bash
   nano .env
   # Replace "your_gemini_api_key_here" with your actual API key
   ```

3. **Test the installation**
   ```bash
   python test_system.py
   ```

## 🎯 Usage

### Option 1: Use a sample presentation
```bash
# Create a sample presentation with known inconsistencies
python create_sample_pptx.py

# Analyze it
python ppt_contradiction_detector.py sample_inconsistent_presentation.pptx
```

### Option 2: Analyze your own presentation
```bash
python ppt_contradiction_detector.py your_presentation.pptx
```

## 📋 Expected Output

The tool will show you:
- **Console report** with colored output showing inconsistencies
- **Severity levels**: Critical, High, Medium, Low
- **Evidence** from specific slides
- **Confidence scores** for each issue

## 🔧 Common Options

```bash
# Save JSON report for automation
python ppt_contradiction_detector.py file.pptx --json

# Save multiple formats
python ppt_contradiction_detector.py file.pptx --json --markdown --output-dir reports/

# Quick summary only
python ppt_contradiction_detector.py file.pptx --quick-summary

# Verbose logging for debugging
python ppt_contradiction_detector.py file.pptx --verbose
```

## ❌ Troubleshooting

**"Configuration Error: GEMINI_API_KEY environment variable is required"**
- Make sure you've set your API key in the `.env` file

**"Unable to import 'pptx'"**
- Run: `pip install -r requirements.txt`

**"File not found"**
- Make sure your PowerPoint file exists and ends with `.pptx`

## 🆘 Need Help?

- Run: `python ppt_contradiction_detector.py --help`
- Check the full README.md for detailed documentation
- Run: `python test_system.py` to verify your setup 