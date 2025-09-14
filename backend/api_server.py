from fastapi import (
    FastAPI,
    File,
    UploadFile,
    Form,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from typing import List
from main import run_hiring_system
from hiring_agents.pdf_parser import PDFParser
import time
from websockets.exceptions import ConnectionClosedError

app = FastAPI(
    title="Hiring Agent System API",
    description="API to interact with the uAgents-based hiring system.",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global WebSocket connections manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: dict):
        if not self.active_connections:
            return  # No connections to send to

        dead_connections = []
        for connection in self.active_connections[
            :
        ]:  # Use slice to avoid modification during iteration
            try:
                await connection.send_text(json.dumps(message))
            except asyncio.CancelledError:
                # Connection cancelled - mark for removal but don't re-raise
                dead_connections.append(connection)
            except (ConnectionClosedError, Exception) as e:
                # Mark dead connections for removal
                dead_connections.append(connection)
                print(f"🔌 WebSocket connection closed or failed: {type(e).__name__}")

        # Remove dead connections safely
        for connection in dead_connections:
            try:
                if connection in self.active_connections:
                    self.active_connections.remove(connection)
            except:
                pass  # Ignore removal errors


manager = ConnectionManager()


@app.get("/test")
async def test_endpoint():
    """Simple test endpoint to verify server is working"""
    print("🧪 TEST ENDPOINT HIT!")
    return {
        "status": "Server is working!",
        "message": "API server is running correctly",
    }


@app.websocket("/ws/progress")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive but handle cancellation gracefully
            try:
                await websocket.receive_text()
            except asyncio.CancelledError:
                # WebSocket was cancelled, exit gracefully
                break
            except ConnectionClosedError:
                # Client disconnected
                break
    except WebSocketDisconnect:
        pass  # Normal disconnection
    except asyncio.CancelledError:
        # Handle server shutdown gracefully
        pass
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        try:
            manager.disconnect(websocket)
        except:
            pass  # Ignore cleanup errors


@app.post("/evaluate-candidate")
async def evaluate_candidate(
    candidate_name: str = Form(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    resume_file: UploadFile = File(...),
):
    """Evaluate a candidate using the hiring agent system"""
    print("=" * 60)
    print("🚨 EVALUATE-CANDIDATE ENDPOINT HIT!")
    print("=" * 60)
    try:
        print(f"📄 Received request for candidate: {candidate_name}")
        print(f"📄 Job title: {job_title}")
        print(f"📄 Parsing PDF file: {resume_file.filename}")

        # Parse the uploaded PDF
        resume_content = PDFParser.extract_text_from_pdf(await resume_file.read())

        if not resume_content or len(resume_content.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PDF or file is too short",
            )

        print(f"📄 Successfully extracted {len(resume_content)} characters from PDF")

        print("🚀 Kicking off the hiring agent pipeline and awaiting results...")

        # Send initial connection event
        await manager.send_message(
            {
                "type": "agent_message",
                "agent_name": "System",
                "message": "Starting hiring evaluation process...",
                "step": "initialization",
                "position": "info",
                "timestamp": time.time(),
            }
        )

        # Create event emitter for this request
        async def emit_event(
            agent_name: str, message: str, step: str, position: str = "info"
        ):
            event = {
                "type": "agent_message",
                "agent_name": agent_name,
                "message": message,
                "step": step,
                "position": position,
                "timestamp": time.time(),
            }
            await manager.send_message(event)
            print(f"📡 Sent WebSocket event: {agent_name} - {message[:50]}...")

        # Run the hiring system with fresh agents
        try:
            result = await run_hiring_system(
                resume_content=resume_content,
                job_description=job_description,
                candidate_name=candidate_name,
                job_title=job_title,
                event_emitter=emit_event,
            )

            if result:
                # Send completion event
                await emit_event(
                    "System", "Analysis completed successfully!", "completed"
                )
                # Return the result directly (not wrapped) to match frontend expectations
                return result.model_dump()
            else:
                # Send error event
                await emit_event("System", "Analysis failed to complete", "error")
                return {
                    "status": "error",
                    "message": "Failed to complete candidate evaluation",
                }
        except asyncio.CancelledError:
            # Handle asyncio cancellation gracefully - shield should prevent this
            print("⚠️ Hiring system execution was cancelled despite shield")
            try:
                await emit_event("System", "Analysis was cancelled", "error")
            except:
                pass
            return {
                "status": "error",
                "message": "Analysis was cancelled or interrupted",
            }

    except asyncio.CancelledError:
        # Handle top-level cancellation
        print("⚠️ Request was cancelled")
        return {"status": "error", "message": "Request was cancelled"}
    except Exception as e:
        print(f"❌ Error in evaluation: {str(e)}")
        # Send error event
        try:
            await emit_event("System", f"Error: {str(e)}", "error")
        except:
            pass  # Don't fail if event emission fails

        return {"status": "error", "message": f"Error during evaluation: {str(e)}"}


if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting HireSense API Server on port 8081...")
    print("   The server will continue running after each hiring evaluation")
    print("   Press Ctrl+C to stop the server")
    print()

    try:
        # Use simple uvicorn run - no complex restart logic
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8081,
            log_level="info",
            access_log=False,
            reload=False,  # Don't use reload to avoid complications
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
