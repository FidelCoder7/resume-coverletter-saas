from fastapi import FastAPI

app = FastAPI(
    title="Resume Coverletter-SaaS API",
    description="Production-ready AI Resume & Cover Letter SaaS",
    version="1.0.0",
) 


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message":"Welcome to AI Resume & Coverletter SaaS API" }