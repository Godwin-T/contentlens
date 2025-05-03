# # app/main.py
# from fastapi import FastAPI
# from api.v1.routes import blog
# from api.db.database import Base, engine

# app = FastAPI(title="Blog API", description="Public blog viewing API", version="1.0.0")

# # Import and create all tables
# Base.metadata.create_all(bind=engine)

# # Include blog routes
# app.include_router(blog.router)


# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <--- add this line
from api.v1.routes import blog
from api.db.database import Base, engine

app = FastAPI(title="Blog API", description="Public blog viewing API", version="1.0.0")

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # <--- or specify your frontend URL, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and create all tables
Base.metadata.create_all(bind=engine)

# Include blog routes
app.include_router(blog.router)
