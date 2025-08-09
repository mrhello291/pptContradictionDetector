#!/usr/bin/env python3
"""
Test script for PowerPoint Contradiction Detector
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import utils.models as models
        print("  ✅ models")
        
        import utils.config as config  
        print("  ✅ config")
        
        import agents.pptx_extractor as pptx_extractor
        print("  ✅ pptx_extractor")
        
        import agents.ai_analyzer as ai_analyzer
        print("  ✅ ai_analyzer")
        
        import agents.output_formatter as output_formatter
        print("  ✅ output_formatter")
        
        print("✅ All core modules imported successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_dependencies():
    """Test that all required dependencies are available."""
    print("\n🧪 Testing dependencies...")
    
    dependencies = [
        ('pptx', 'python-pptx'),
        ('PIL', 'Pillow'),
        ('google.generativeai', 'google-generativeai'),
        ('dotenv', 'python-dotenv')
    ]
    
    missing = []
    
    for import_name, package_name in dependencies:
        try:
            __import__(import_name)
            print(f"  ✅ {package_name}")
        except ImportError:
            print(f"  ❌ {package_name}")
            missing.append(package_name)
    
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies available")
        return True

def test_configuration():
    """Test configuration setup."""
    print("\n🧪 Testing configuration...")
    
    try:
        from utils.config import Config
        
        # Check if .env file exists
        env_file = Path('.env')
        if env_file.exists():
            print("  ✅ .env file found")
        else:
            print("  ⚠️  .env file not found (will check environment variables)")
        
        # Check API key
        if Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != "your_gemini_api_key_here":
            print("  ✅ Gemini API key configured")
            return True
        else:
            print("  ❌ Gemini API key not configured")
            print("     Please set GEMINI_API_KEY in .env file or environment variable")
            return False
            
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False

def test_models():
    """Test data models."""
    print("\n🧪 Testing data models...")
    
    try:
        from utils.models import SlideContent, Inconsistency, InconsistencyType, SeverityLevel, AnalysisResult
        
        # Test SlideContent
        slide = SlideContent(
            slide_number=1,
            title="Test Slide",
            text_content=["Test content"],
            numerical_data=[{"value": "100", "type": "number"}],
            images_text=[],
            raw_content="Test content"
        )
        print("  ✅ SlideContent model")
        
        # Test Inconsistency
        inconsistency = Inconsistency(
            type=InconsistencyType.NUMERICAL_CONFLICT,
            severity=SeverityLevel.HIGH,
            description="Test inconsistency",
            affected_slides=[1, 2],
            evidence={"slide_1": "test", "slide_2": "test"},
            confidence_score=0.9,
            explanation="Test explanation"
        )
        print("  ✅ Inconsistency model")
        
        # Test AnalysisResult
        result = AnalysisResult(
            presentation_name="test.pptx",
            total_slides=1,
            inconsistencies=[inconsistency],
            processing_time=1.0,
            summary="Test summary"
        )
        print("  ✅ AnalysisResult model")
        
        print("✅ All data models working")
        return True
        
    except Exception as e:
        print(f"❌ Model error: {e}")
        return False

def test_file_access():
    """Test file access permissions."""
    print("\n🧪 Testing file access...")
    
    try:
        # Test write access
        test_file = Path("test_write.tmp")
        test_file.write_text("test")
        test_file.unlink()
        print("  ✅ Write access")
        
        # Test requirements.txt exists
        if Path("requirements.txt").exists():
            print("  ✅ requirements.txt found")
        else:
            print("  ❌ requirements.txt not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ File access error: {e}")
        return False

def main():
    """Run all tests."""
    print("🔍 PowerPoint Contradiction Detector - System Test")
    print("=" * 60)
    
    tests = [
        test_file_access,
        test_dependencies,
        test_imports,
        test_models,
        test_configuration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\nTo get started:")
        print("1. Make sure you have a .pptx file to analyze")
        print("2. Run: python ppt_contradiction_detector.py your_file.pptx")
        return True
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 