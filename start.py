#!/usr/bin/env python3
"""
Production startup script for YouTube to Blog Converter
"""

import os
import sys
import uvicorn
from pathlib import Path

def main():
    """Start the FastAPI server in production mode"""
    
    # Get port from environment (Railway sets this)
    port = int(os.environ.get("PORT", 8000))
    
    # Keep working directory at project root for proper imports
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Add the project root to Python path for imports
    sys.path.insert(0, str(project_root))
    
    print(f"🚀 Starting YouTube to Blog Converter API Server on port {port}...")
    
    # Start the server in production mode
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=port,
        workers=1,  # Single worker for hobby plans
        log_level="info"
    )

if __name__ == "__main__":
    main() 