# app/main.py
import os 
from fastapi import FastAPI
from fastapi.responses import HTMLResponse 
from starlette.middleware.sessions import SessionMiddleware
from .api import auth, tasks 
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

app = FastAPI(title="Proactive Financial Guardian API")
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

SESSION_KEY = os.environ.get("SESSION_SECRET_KEY", "a_default_fallback_key_for_local_dev")
app.add_middleware(SessionMiddleware, secret_key=SESSION_KEY)

app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/health", tags=["Health Check"])
async def health_check():
    """A simple endpoint for the GKE Ingress health checker."""
    return {"status": "ok"}

@app.get("/", tags=["Root"])
async def root():
    html_content = """
    <html>
        <head>
            <title>Proactive Financial Guardian</title>
        </head>
        <body>
            <h1>Welcome to the Proactive Financial Guardian API</h1>
            <p>Click the link below to authenticate with Google.</p>
            <a href="/login/google">Log In with Google</a>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)