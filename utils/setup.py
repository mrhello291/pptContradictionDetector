#!/usr/bin/env python3
"""
Setup script for PowerPoint Contradiction Detector
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_file = Path('.env')
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    env_content = """# PowerPoint Contradiction Detector Configuration
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Optional Configuration (uncomment to override defaults)
# GEMINI_MODEL=gemini-2.0-flash-exp
# MAX_TOKENS=8192
# TEMPERATURE=0.1
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file - please edit it with your API key")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
        else:
            print("❌ Error installing dependencies:")
            print(result.stderr)
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")

def make_executable():
    """Make the main script executable."""
    try:
        os.chmod('ppt_contradiction_detector.py', 0o755)
        print("✅ Made script executable")
    except Exception as e:
        print(f"⚠️  Could not make script executable: {e}")

def main():
    """Run setup process."""
    print("🚀 Setting up PowerPoint Contradiction Detector...")
    print()
    
    # Install dependencies
    install_dependencies()
    print()
    
    # Create .env file
    create_env_file()
    print()
    
    # Make script executable
    make_executable()
    print()
    
    print("🎉 Setup complete!")
    print()
    print("Next steps:")
    print("1. Edit .env file with your Gemini API key")
    print("2. Run: python ppt_contradiction_detector.py your_presentation.pptx")
    print()
    print("For help: python ppt_contradiction_detector.py --help")

if __name__ == "__main__":
    main() 