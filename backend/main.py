"""
AI Tanács - FastAPI Backend
Real-time multi-agent AI council with WebSocket support
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, List
import asyncio
import json
from datetime import datetime

from config import settings
from agents import create_council
from voting import get_voting_system
from api_client import api_client

# FastAPI app
app = FastAPI(
    title="AI Tanács API",
    description="Voting-Based Multi-Agent AI System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
council = create_council()
active_connections: List[WebSocket] = []


# Pydantic models
class QuestionRequest(BaseModel):
    question: str
    weights: Optional[Dict[str, float]] = None
    voting_method: Optional[str] = "borda"


class AgentResponse(BaseModel):
    agent: str
    short_name: str
    text: str
    confidence: float
    score: float
    elapsed_seconds: float
    color: str
    bio: str


class CouncilResponse(BaseModel):
    question: str
    winner: str
    winner_score: float
    all_responses: List[AgentResponse]
    voting_scores: Dict[str, float]
    voting_method: str
    total_time_seconds: float
    timestamp: str


# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to client: {e}")


manager = ConnectionManager()


# API Routes
@app.get("/")
async def root():
    """API root - health check"""
    return {
        "service": "AI Tanács API",
        "status": "running",
        "agents": len(council),
        "version": "1.0.0"
    }


@app.get("/api/agents")
async def get_agents():
    """Get list of all agents and their info"""
    return {
        "agents": [
            {
                "name": agent.name,
                "short_name": agent.short_name,
                "color": agent.color,
                "bio": agent.bio,
                "expertise": agent.expertise,
                "speed_multiplier": agent.speed_multiplier,
                "provider": agent.provider,
                "model": agent.model
            }
            for agent in council
        ]
    }


@app.post("/api/ask", response_model=CouncilResponse)
async def ask_council(request: QuestionRequest):
    """
    Ask the AI Council a question

    This runs all agents in parallel and returns the voted best answer
    """
    start_time = datetime.now()

    # Run all agents in parallel
    tasks = [agent.think(request.question, api_client=api_client) for agent in council]
    responses = await asyncio.gather(*tasks)

    # Sort by confidence score (descending)
    responses_sorted = sorted(responses, key=lambda x: x["score"], reverse=True)

    # Apply voting
    voting_fn = get_voting_system(request.voting_method or "borda")
    winner_text, voting_scores = voting_fn(responses_sorted, request.weights)

    # Get winner score
    winner_score = max(voting_scores.values()) if voting_scores else 0.0

    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()

    return CouncilResponse(
        question=request.question,
        winner=winner_text,
        winner_score=winner_score,
        all_responses=responses_sorted,
        voting_scores=voting_scores,
        voting_method=request.voting_method or "borda",
        total_time_seconds=total_time,
        timestamp=datetime.now().isoformat()
    )


@app.websocket("/ws/ask")
async def websocket_ask(websocket: WebSocket):
    """
    WebSocket endpoint for real-time agent updates

    Client sends: {"question": "...", "weights": {...}, "voting_method": "..."}
    Server streams: agent status updates, responses, and final result
    """
    await manager.connect(websocket)

    try:
        # Wait for question
        data = await websocket.receive_json()
        question = data.get("question", "")
        weights = data.get("weights", {})
        voting_method = data.get("voting_method", "borda")

        if not question:
            await websocket.send_json({
                "type": "error",
                "message": "No question provided"
            })
            return

        # Send initial status
        await websocket.send_json({
            "type": "status",
            "phase": "thinking",
            "message": "AI Tanács gondolkodik..."
        })

        # Run agents and send updates
        start_time = datetime.now()

        # Create tasks with callbacks for progress updates
        async def run_agent_with_updates(agent):
            # Send thinking status
            await websocket.send_json({
                "type": "agent_update",
                "agent": agent.name,
                "status": "thinking",
                "progress": 0
            })

            # Run agent
            response = await agent.think(question, api_client=api_client)

            # Send completion status
            await websocket.send_json({
                "type": "agent_update",
                "agent": agent.name,
                "status": "complete",
                "progress": 100,
                "response": response
            })

            return response

        # Run all agents in parallel with progress updates
        tasks = [run_agent_with_updates(agent) for agent in council]
        responses = await asyncio.gather(*tasks)

        # Send responding phase
        await websocket.send_json({
            "type": "status",
            "phase": "responding",
            "message": "Válaszok érkeztek..."
        })

        await asyncio.sleep(0.5)

        # Send voting phase
        await websocket.send_json({
            "type": "status",
            "phase": "voting",
            "message": "Szavazás folyamatban..."
        })

        # Sort and vote
        responses_sorted = sorted(responses, key=lambda x: x["score"], reverse=True)
        voting_fn = get_voting_system(voting_method)
        winner_text, voting_scores = voting_fn(responses_sorted, weights)
        winner_score = max(voting_scores.values()) if voting_scores else 0.0

        await asyncio.sleep(0.5)

        # Send final result
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()

        await websocket.send_json({
            "type": "result",
            "phase": "complete",
            "question": question,
            "winner": winner_text,
            "winner_score": winner_score,
            "all_responses": responses_sorted,
            "voting_scores": voting_scores,
            "voting_method": voting_method,
            "total_time_seconds": total_time,
            "timestamp": datetime.now().isoformat()
        })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "message": str(e)
            })
        except:
            pass
        manager.disconnect(websocket)


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agents": len(council),
        "timestamp": datetime.now().isoformat()
    }


# Run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload
    )
