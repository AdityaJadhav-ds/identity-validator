from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.validate import router as validate_router

app = FastAPI()

# -----------------------------
# CORS (IMPORTANT)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# ROUTES
# -----------------------------
app.include_router(validate_router, prefix="/api")


# -----------------------------
# ROOT
# -----------------------------
@app.get("/")
def root():
    return {"message": "API is running"}