import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.auth_service.router import router as auth_router

app = FastAPI(
    debug=os.getenv("DEBUG", False),
    title="MIWA Backend",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, tags=["Authentication"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
