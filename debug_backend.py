#!/usr/bin/env python3
"""
Debug script to test backend imports and identify issues
"""

import sys
import traceback
from pathlib import Path

# Add backend to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

def test_imports():
    """Test all backend imports"""
    print("🔍 Testing backend imports...")
    
    try:
        print("1. Testing config import...")
        from backend.config import settings
        print(f"   ✅ Config loaded: {settings.APP_NAME}")
        print(f"   🔑 Nebius API: {settings.has_nebius_api}")
        print(f"   🔑 YouTube API: {settings.has_youtube_api}")
        
        print("2. Testing YouTube service import...")
        from backend.youtube_service import YouTubeService
        youtube_service = YouTubeService()
        print("   ✅ YouTube service initialized")
        
        print("3. Testing LLM service import...")
        from backend.llm_service import LLMService
        if settings.has_nebius_api:
            llm_service = LLMService()
            print("   ✅ LLM service initialized")
        else:
            print("   ⚠️ Nebius API key not configured - skipping LLM service")
        
        print("4. Testing blog generator import...")
        from utils.blog_generator import BlogGenerator
        blog_generator = BlogGenerator()
        print("   ✅ Blog generator initialized")
        
        print("5. Testing FastAPI app import...")
        from backend.main import app
        print("   ✅ FastAPI app imported")
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        print(f"📍 Error type: {type(e).__name__}")
        print(f"📍 Error details: {str(e)}")
        traceback.print_exc()
        return False

def test_environment():
    """Test environment configuration"""
    print("\n🔍 Testing environment...")
    
    import os
    from backend.config import settings
    
    print(f"PORT: {os.getenv('PORT', 'Not set')}")
    print(f"NEBIUS_API_KEY: {'Set' if settings.NEBIUS_API_KEY else 'Not set'}")
    print(f"YOUTUBE_API_KEY: {'Set' if settings.YOUTUBE_API_KEY else 'Not set'}")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"CORS_ORIGINS: {settings.CORS_ORIGINS}")

if __name__ == "__main__":
    print("🚀 Backend Debug Test\n")
    
    # Test environment first
    test_environment()
    
    # Test imports
    if test_imports():
        print("\n✅ Backend should start successfully!")
    else:
        print("\n❌ Backend has startup issues!") 