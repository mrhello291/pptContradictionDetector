#!/usr/bin/env python3
"""
PowerPoint Contradiction Detector - Main Script

An AI-enabled tool that processes PowerPoint presentations and detects
factual or logical inconsistencies across slides.

Usage:
    python ppt_contradiction_detector.py <presentation.pptx> [options]
"""

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import Optional

# Import our modules
from config import Config
from models import AnalysisResult
from pptx_extractor import PPTXExtractor
from ai_analyzer import AIAnalyzer
from output_formatter import OutputFormatter

def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format=Config.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Reduce noise from external libraries
    logging.getLogger('google').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

def validate_input_file(file_path: Path) -> bool:
    """Validate the input PowerPoint file."""
    if not file_path.exists():
        print(f"❌ Error: File not found: {file_path}")
        return False
    
    if not file_path.suffix.lower() in ['.pptx', '.ppt']:
        print(f"❌ Error: File must be a PowerPoint presentation (.pptx or .ppt)")
        return False
    
    return True

def main():
    """Main function to run the PowerPoint contradiction detector."""
    parser = argparse.ArgumentParser(
        description="AI-enabled PowerPoint Contradiction Detector",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ppt_contradiction_detector.py presentation.pptx
  python ppt_contradiction_detector.py presentation.pptx --output-dir ./reports
  python ppt_contradiction_detector.py presentation.pptx --json-only --verbose
  
Features:
  - Detects numerical conflicts (revenue figures, percentages, statistics)
  - Identifies textual contradictions (conflicting claims)
  - Finds timeline mismatches (dates, forecasts)
  - Discovers logical inconsistencies
  - Flags data mismatches and percentage errors
  
Output formats:
  - Colored console report (default)
  - JSON report (--json or --json-only)
  - Markdown report (--markdown)
        """
    )
    
    # Required arguments
    parser.add_argument(
        'presentation',
        type=str,
        help='Path to the PowerPoint presentation file (.pptx or .ppt)'
    )
    
    # Output options
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default='.',
        help='Directory to save output reports (default: current directory)'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Also save results as JSON report'
    )
    
    parser.add_argument(
        '--json-only',
        action='store_true',
        help='Only output JSON report (no console output)'
    )
    
    parser.add_argument(
        '--markdown',
        action='store_true',
        help='Also save results as Markdown report'
    )
    
    parser.add_argument(
        '--no-colors',
        action='store_true',
        help='Disable colored console output'
    )
    
    # Processing options
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--quick-summary',
        action='store_true',
        help='Show only a quick summary (useful for automation)'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # Validate input
    presentation_path = Path(args.presentation)
    if not validate_input_file(presentation_path):
        sys.exit(1)
    
    # Validate output directory
    output_dir = Path(args.output_dir)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"❌ Error creating output directory: {e}")
        sys.exit(1)
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nPlease ensure you have set your GEMINI_API_KEY:")
        print("1. Create a .env file in this directory with: GEMINI_API_KEY=your_api_key_here")
        print("2. Or set the environment variable: export GEMINI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    # Start processing
    start_time = time.time()
    
    if not args.json_only:
        print("🔍 Starting PowerPoint Contradiction Analysis...")
        print(f"📁 Processing: {presentation_path.name}")
        print()
    
    try:
        # Initialize components
        extractor = PPTXExtractor()
        analyzer = AIAnalyzer()
        formatter = OutputFormatter()
        
        # Extract content from presentation
        if not args.json_only:
            print("📄 Extracting content from slides...")
        
        slides = extractor.extract_presentation(presentation_path)
        
        if not slides:
            print("❌ No slides found in the presentation.")
            sys.exit(1)
        
        if not args.json_only:
            print(f"✅ Extracted content from {len(slides)} slides")
            print("🤖 Analyzing for inconsistencies using AI...")
        
        # Analyze for inconsistencies
        inconsistencies = analyzer.analyze_inconsistencies(slides)
        
        # Generate summary
        summary = analyzer.generate_summary(inconsistencies, len(slides))
        
        # Create analysis result
        processing_time = time.time() - start_time
        result = AnalysisResult(
            presentation_name=presentation_path.name,
            total_slides=len(slides),
            inconsistencies=inconsistencies,
            processing_time=processing_time,
            summary=summary
        )
        
        # Output results
        if args.quick_summary:
            formatter.print_quick_summary(result)
        elif not args.json_only:
            formatter.print_console_report(result, use_colors=not args.no_colors)
        
        # Save additional formats
        if args.json or args.json_only:
            json_path = output_dir / f"{presentation_path.stem}_analysis.json"
            formatter.save_json_report(result, json_path)
        
        if args.markdown:
            md_path = output_dir / f"{presentation_path.stem}_analysis.md"
            formatter.save_markdown_report(result, md_path)
        
        # Final status
        if not args.json_only and not args.quick_summary:
            print(f"\n✅ Analysis completed in {processing_time:.2f} seconds")
            
            if result.inconsistencies:
                critical_count = sum(1 for i in result.inconsistencies 
                                   if i.severity.value == 'critical')
                if critical_count > 0:
                    print(f"🚨 ATTENTION: {critical_count} critical issues found!")
                    sys.exit(2)  # Exit code 2 for critical issues
                else:
                    sys.exit(1)  # Exit code 1 for other issues
            else:
                print("🎉 No inconsistencies detected!")
                sys.exit(0)  # Exit code 0 for success
        
    except KeyboardInterrupt:
        print("\n❌ Analysis interrupted by user")
        sys.exit(130)
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        print(f"❌ Analysis failed: {e}")
        
        if args.verbose:
            import traceback
            traceback.print_exc()
        
        sys.exit(1)

if __name__ == "__main__":
    main() 