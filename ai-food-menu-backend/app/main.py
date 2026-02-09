from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.menu import router as menu_router
from app.routes.feedback import router as feedback_router
from app.routes.insight import router as insight_router
from app.routes.chat import router as chat_router


app = FastAPI(title="AI Food Menu API")


# CORS — allow frontend (Vercel) + local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # use "*" for now (works for Vercel + local)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(menu_router)
app.include_router(feedback_router)
app.include_router(insight_router)
app.include_router(chat_router)


# Health check (optional but useful)
@app.get("/")
def root():
    return {"status": "AI Food Menu Backend Running"}
