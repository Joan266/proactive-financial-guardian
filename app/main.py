# app/main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse 
from starlette.middleware.sessions import SessionMiddleware
from .api import auth, tasks 

app = FastAPI(title="Proactive Financial Guardian API")

# Add middleware
app.add_middleware(SessionMiddleware, secret_key="YOUR_SECRET_KEY_HERE")

# Include routers from other files
app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/", tags=["Root"])
async def root():
    # Return an HTML response with a clickable link to start the login flow
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