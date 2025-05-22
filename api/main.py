# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routes import route
from api.db.database import Base, engine

app = FastAPI(title="Blog API", description="Public blog viewing API", version="1.0.0")

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and create all tables
Base.metadata.create_all(bind=engine)

# Include blog routes
app.include_router(route.router)
