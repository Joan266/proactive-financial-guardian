# app/main.py
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from .api import auth  # Import our new auth router

app = FastAPI(title="Proactive Financial Guardian API")

# Add middleware
app.add_middleware(SessionMiddleware, secret_key="YOUR_SECRET_KEY_HERE")

# Include routers
app.include_router(auth.router)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the Proactive Financial Guardian API"}