from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import asyncio
from typing import Optional
import sys
import os

# Add the parent directory to path to import utils
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from backend.youtube_service import YouTubeService
from backend.config import settings
from utils.blog_generator import BlogGenerator

app = FastAPI(
    title=settings.APP_NAME, 
    version=settings.VERSION,
    description=settings.DESCRIPTION
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize services with configuration
youtube_service = YouTubeService(api_key=settings.YOUTUBE_API_KEY)
blog_generator = BlogGenerator()

class VideoRequest(BaseModel):
    url: HttpUrl
    template: str = "article"

class VideoResponse(BaseModel):
    title: str
    description: str
    thumbnail: str
    duration: str
    views: str
    published_at: str
    channel_name: str
    video_id: str

class BlogResponse(BaseModel):
    content: str
    template: str
    word_count: int

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": settings.APP_NAME, 
        "status": "active", 
        "version": settings.VERSION,
        "environment": "development" if settings.is_development else "production",
        "youtube_api_configured": settings.has_youtube_api,
        "nebius_api_configured": settings.has_nebius_api,
        "cors_origins": settings.CORS_ORIGINS
    }

@app.options("/{path:path}")
async def options_handler(path: str):
    """Handle CORS preflight requests"""
    return {"message": "OK"}

@app.post("/api/video-info", response_model=VideoResponse)
async def get_video_info(request: VideoRequest):
    """Extract video information from YouTube URL"""
    try:
        video_id = youtube_service.extract_video_id(str(request.url))
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        
        # Simulate API processing delay for better UX
        await asyncio.sleep(1)
        
        video_data = youtube_service.get_video_metadata(video_id)
        return VideoResponse(**video_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

@app.post("/api/generate-blog", response_model=BlogResponse)
async def generate_blog(request: VideoRequest):
    """Generate blog content from video data"""
    if not blog_generator.llm_enabled:
        raise HTTPException(
            status_code=503, 
            detail="LLM Service Unavailable: NEBIUS_API_KEY is not configured on the server."
        )

    try:
        video_id = youtube_service.extract_video_id(str(request.url))
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        
        # Simulate processing delay for better UX
        await asyncio.sleep(2)
        
        # Get video metadata and transcript
        video_data = youtube_service.get_video_metadata(video_id)
        transcript = youtube_service.get_transcript(video_id)
        
        # Generate blog content
        blog_content = blog_generator.generate_blog(video_data, request.template, transcript)
        
        # Calculate word count
        word_count = len(blog_content.split())
        
        return BlogResponse(
            content=blog_content,
            template=request.template,
            word_count=word_count
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating blog: {str(e)}")

@app.get("/api/templates")
async def get_templates():
    """Get available blog templates"""
    return {
        "templates": [
            {
                "id": "article",
                "name": "Article",
                "description": "Standard blog article format with introduction, analysis, and conclusion"
            },
            {
                "id": "tutorial", 
                "name": "Tutorial",
                "description": "Step-by-step guide format with structured learning approach"
            },
            {
                "id": "review",
                "name": "Review", 
                "description": "Comprehensive review format with ratings and detailed analysis"
            },
            {
                "id": "summary",
                "name": "Summary",
                "description": "Concise summary format with key highlights and takeaways"
            }
        ]
    }

@app.get("/api/health")
async def health_check():
    """Detailed health check endpoint"""
    try:
        # Test if services are working
        test_video_id = "dQw4w9WgXcQ"  # Rick Roll video ID for testing
        
        # Test YouTube service
        youtube_working = True
        try:
            youtube_service.get_video_metadata(test_video_id)
        except:
            youtube_working = False
        
        # Test blog generator
        blog_working = True
        try:
            mock_data = {"title": "Test", "description": "Test", "channel_name": "Test", 
                        "duration": "1:00", "views": "100", "published_at": "2024-01-01", "video_id": "test"}
            blog_generator.generate_blog(mock_data, "article", "test transcript")
        except:
            blog_working = False
        
        return {
            "status": "healthy",
            "services": {
                "youtube_service": "operational" if youtube_working else "degraded",
                "blog_generator": "operational" if blog_working else "degraded"
            },
            "api_version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    print(f"🚀 Starting {settings.APP_NAME} v{settings.VERSION}")
    print(f"🌐 Server: http://{settings.HOST}:{settings.PORT}")
    print(f"📖 API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"🔧 Environment: {'Development' if settings.is_development else 'Production'}")
    print(f"🔑 YouTube API: {'✅ Configured' if settings.has_youtube_api else '❌ Not configured (using PyTube fallback)'}")
    
    # Use proper configuration for uvicorn
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.is_development,
        log_level="debug" if settings.is_development else "info"
    )