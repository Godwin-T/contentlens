# app/main.py
from fastapi import FastAPI
from api.v1.routes import blog
from api.db.database import Base, engine

app = FastAPI(title="Blog API", description="Public blog viewing API", version="1.0.0")

# Import and create all tables
Base.metadata.create_all(bind=engine)

# Include blog routes
app.include_router(blog.router)
