from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.db import Base
from app.deps import engine
from app.features.identity.router import router as identity_router
from app.features.jobs.public import router as public_router
from app.features.jobs.router import router as jobs_router
from app.features.keys.router import router as keys_router
from app.features.webhooks.router import router as webhooks_router
from app.features.workers.router import router as worker_router
from app.kernel.errors import DomainError
app = FastAPI(title="Queue API", version="0.1.0", redirect_slashes=False)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
@app.exception_handler(DomainError)
async def domain_error(_, exc: DomainError):
    return JSONResponse({"code": exc.code, "message": exc.message}, status_code=exc.status)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
@app.get("/health")
def health():
    return {"status": "ok"}
app.include_router(identity_router)
app.include_router(keys_router)
app.include_router(jobs_router)
app.include_router(worker_router)
app.include_router(webhooks_router)
app.include_router(public_router)
