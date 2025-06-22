#!/usr/bin/env python3
"""
Start Upload Server
===================

Simple script to start the FastAPI file upload server.
"""

import uvicorn
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Starting Resume Upload Server...")
    print("📋 Server will be available at: http://localhost:8080")
    print("📋 Health check: http://localhost:8080/health")
    print("📋 Upload endpoint: http://localhost:8080/upload-resume")
    print("📋 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    uvicorn.run(
        "file_upload_server:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    ) 