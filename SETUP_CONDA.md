# Conda Environment Setup Guide

This guide shows how to set up and use the PowerPoint Contradiction Detector with conda.

## 🐍 Method 1: Use Existing Environment (Already Created)

If you already have the `ppt-detector` environment:

```bash
# Activate the environment
conda activate ppt-detector

# Verify installation
python test_system.py

# Set your API key (edit .env file)
nano .env
# Change: GEMINI_API_KEY=your_actual_api_key_here

# Test with sample presentation
python create_sample_pptx.py
python ppt_contradiction_detector.py sample_inconsistent_presentation.pptx
```

## 🆕 Method 2: Create New Environment from environment.yml

To recreate the environment from scratch:

```bash
# Create environment from yml file
conda env create -f environment.yml

# Activate the environment
conda activate ppt-detector

# Run setup
python setup.py

# Edit .env file with your API key
nano .env
```

## 📋 Current Environment Status

Your current environment `ppt-detector` includes:
- ✅ Python 3.9
- ✅ python-pptx==0.6.23
- ✅ Pillow==10.1.0  
- ✅ google-generativeai==0.3.2
- ✅ python-dotenv==1.0.0
- ✅ All dependencies installed

## 🔑 API Key Setup

1. **Get Gemini API Key**:
   - Visit: https://makersuite.google.com/app/apikey
   - Create a new API key
   - Copy the key

2. **Set API Key**:
   ```bash
   # Edit .env file
   nano .env
   
   # Change this line:
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. **Verify Setup**:
   ```bash
   python test_system.py
   ```

## 🎯 Usage Examples

```bash
# Activate environment first
conda activate ppt-detector

# Basic analysis
python ppt_contradiction_detector.py presentation.pptx

# With JSON output
python ppt_contradiction_detector.py presentation.pptx --json

# Quick summary
python ppt_contradiction_detector.py presentation.pptx --quick-summary

# Save to specific directory
python ppt_contradiction_detector.py presentation.pptx --output-dir ./reports --json --markdown
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

# Export environment for sharing
conda env export > environment.yml
```

## 🧪 Testing

Test everything is working:

```bash
# Activate environment
conda activate ppt-detector

# Run system tests
python test_system.py

# Create sample presentation
python create_sample_pptx.py

# Test analysis (requires API key)
python ppt_contradiction_detector.py sample_inconsistent_presentation.pptx --quick-summary
```

## 🚨 Troubleshooting

**Environment not found**:
```bash
conda env create -f environment.yml
conda activate ppt-detector
```

**Import errors**:
```bash
conda activate ppt-detector
pip install -r requirements.txt
```

**API key errors**:
```bash
# Check .env file
cat .env
# Edit and set proper API key
nano .env
```

**Permission errors**:
```bash
chmod +x *.py
```

## 🎉 You're Ready!

Your environment is set up and ready to use. Just add your Gemini API key to the `.env` file and start analyzing PowerPoint presentations for contradictions! 