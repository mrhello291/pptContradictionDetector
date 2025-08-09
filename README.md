# PowerPoint Contradiction Detector

An AI-powered Python tool that analyzes PowerPoint presentations to detect factual and logical inconsistencies across slides. Using Google's Gemini 2.0 Flash model, this tool identifies various types of contradictions, conflicts, and errors that may exist in presentation content.

## 🔍 Features

### Inconsistency Detection Types

- **Numerical Conflicts**: Conflicting revenue figures, mismatched statistics, inconsistent data points
- **Textual Contradictions**: Contradictory claims or statements (e.g., "highly competitive market" vs "few competitors")
- **Timeline Mismatches**: Conflicting dates, inconsistent forecasts, temporal contradictions
- **Logical Inconsistencies**: Claims that contradict each other logically
- **Data Mismatches**: Charts and tables with conflicting information
- **Percentage Errors**: Percentages that don't sum to 100% when they should
- **Factual Contradictions**: Any factual claims that contradict each other

### Output Formats

- **Console Report**: Formatted, colored terminal output with severity levels
- **JSON Report**: Machine-readable format for integration with other tools
- **Markdown Report**: Human-readable report format for documentation

### Key Capabilities

- **Comprehensive Analysis**: Examines text content, numerical data, tables, and metadata
- **AI-Powered**: Uses Google Gemini 2.0 Flash for intelligent contradiction detection
- **Severity Classification**: Categorizes issues as Low, Medium, High, or Critical
- **Confidence Scoring**: Provides confidence scores for each detected inconsistency
- **Detailed Evidence**: Shows specific slide content that contains contradictions
- **Scalable Processing**: Handles large presentations efficiently

## 📋 Requirements

- Python 3.7 or higher
- Google Gemini API key
- PowerPoint presentation files (.pptx format)

## 🚀 Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd pptContradictionDetector
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Gemini API key**
   
   Create a `.env` file in the project directory:
   ```bash
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```
   
   Or set as an environment variable:
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```

## 🎯 Usage

### Basic Usage

```bash
python ppt_contradiction_detector.py presentation.pptx
```

### Advanced Usage

```bash
# Save JSON and Markdown reports
python ppt_contradiction_detector.py presentation.pptx --json --markdown --output-dir ./reports

# Verbose mode with detailed logging
python ppt_contradiction_detector.py presentation.pptx --verbose

# JSON-only output (useful for automation)
python ppt_contradiction_detector.py presentation.pptx --json-only

# Quick summary for CI/CD pipelines
python ppt_contradiction_detector.py presentation.pptx --quick-summary

# Disable colors for piping output
python ppt_contradiction_detector.py presentation.pptx --no-colors
```

### Command Line Options

- `presentation` - Path to PowerPoint file (required)
- `--output-dir, -o` - Directory for output reports (default: current directory)
- `--json` - Also save JSON report
- `--json-only` - Only output JSON (no console output)
- `--markdown` - Also save Markdown report
- `--no-colors` - Disable colored console output
- `--verbose, -v` - Enable detailed logging
- `--quick-summary` - Show only brief summary

## 📊 Output Examples

### Console Output
```
================================================================================
📊 POWERPOINT CONTRADICTION ANALYSIS REPORT
================================================================================
Presentation: sample_presentation.pptx
Total Slides: 15
Processing Time: 12.34 seconds
Analysis Date: 2024-01-15 10:30:45

📋 SUMMARY
----------------------------------------
Analysis completed for 15 slides.
Found 3 inconsistencies:
Severity breakdown:
  - High: 1
  - Medium: 2

⚠️  INCONSISTENCIES FOUND
----------------------------------------

🔴 HIGH SEVERITY (1 issues)
------------------------------------------------------------

#1 Revenue figures don't match between quarterly summaries
   Type: Numerical Conflict
   Affected Slides: 3, 8
   Confidence: 0.95
   Evidence:
     slide_3: Q1 Revenue: $1.2M
     slide_8: Q1 Revenue reported as $1.5M in summary
   Explanation: Slide 3 shows Q1 revenue as $1.2M while slide 8 shows it as $1.5M - these should be consistent.
```

### Exit Codes

- `0` - No inconsistencies found
- `1` - Inconsistencies found (non-critical)
- `2` - Critical inconsistencies found
- `130` - Interrupted by user

## 🏗️ Architecture

The tool consists of several modular components:

### Core Modules

1. **`pptx_extractor.py`** - Extracts text, numerical data, and metadata from PowerPoint files
2. **`ai_analyzer.py`** - Uses Gemini AI to detect inconsistencies and contradictions
3. **`output_formatter.py`** - Formats and displays results in various formats
4. **`models.py`** - Data models for representing slides and inconsistencies
5. **`config.py`** - Configuration management and API key handling

### Analysis Process

1. **Content Extraction**: Parse PPTX file and extract text, numbers, tables, and metadata
2. **AI Analysis**: Send structured content to Gemini for contradiction detection
3. **Result Processing**: Parse AI response and classify inconsistencies
4. **Output Generation**: Format results for console, JSON, or Markdown output

## 🔧 Configuration

### Environment Variables

- `GEMINI_API_KEY` - Your Google Gemini API key (required)

### Model Configuration

The tool uses Gemini 2.0 Flash with optimized settings:
- **Temperature**: 0.1 (low for consistent analysis)
- **Max Tokens**: 8192
- **Model**: `gemini-2.5-flash`

## 🎨 Customization

### Adding New Inconsistency Types

1. Update the `InconsistencyType` enum in `models.py`
2. Modify the analysis prompt in `ai_analyzer.py`
3. Update the output formatting as needed

### Custom Output Formats

Extend the `OutputFormatter` class to add new output formats like CSV, XML, or custom report templates.

## 🧪 Limitations

### Current Limitations

- **OCR Not Implemented**: Images within slides are detected but text extraction requires additional OCR setup
- **Chart Analysis**: Limited analysis of chart data vs. visual chart content
- **Language Support**: Optimized for English presentations
- **File Formats**: Supports .pptx files primarily (.ppt support limited)

### Future Enhancements

- OCR integration for image text extraction
- Chart and graph content analysis
- Multi-language support
- Integration with presentation creation tools
- Batch processing capabilities
- Web interface option

## 🚨 Error Handling

The tool includes comprehensive error handling for:

- Invalid file formats
- Missing API keys
- Network connectivity issues
- Malformed presentations
- AI service errors
- File permission issues

## 📈 Performance

### Typical Performance

- **Small presentations** (5-10 slides): 5-15 seconds
- **Medium presentations** (10-25 slides): 15-30 seconds  
- **Large presentations** (25+ slides): 30-60 seconds

Performance depends on:
- Slide content complexity
- Amount of text and numerical data
- Network latency to Gemini API
- Hardware specifications

### Optimization Tips

- Use `--json-only` for faster processing in automation
- Enable `--verbose` only when debugging
- Process presentations in batches for multiple files

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

1. OCR integration for image text extraction
2. Additional inconsistency detection patterns
3. Performance optimizations
4. Multi-language support
5. Additional output formats
6. Test coverage improvements

## 📄 License

This project is provided as-is for educational and professional use.

## 🆘 Support

For issues and questions:

1. Check this README for common solutions
2. Review error messages and logs with `--verbose`
3. Verify your Gemini API key is correctly set
4. Ensure your presentation file is valid

## 🏷️ Version

Current version: 1.0.0

Features a robust, production-ready implementation with comprehensive error handling, multiple output formats, and enterprise-grade reliability.