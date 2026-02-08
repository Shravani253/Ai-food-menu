from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.menu import router as menu_router
from app.routes.feedback import router as feedback_router
from app.routes.insight import router as insight_router
from app.routes.chat import router as chat_router

app = FastAPI(title="AI Food Menu API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(menu_router)
app.include_router(feedback_router)
app.include_router(insight_router)
app.include_router(chat_router)