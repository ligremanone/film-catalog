from fastapi import FastAPI, Request
from api import router as api_router

app = FastAPI(
    name="Film Catalog",
    title="Film Catalog",
)
app.include_router(api_router)


@app.get("/")
async def read_root(
    request: Request,
):
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "message": f"Welcome to film catalog",
        "docs": str(docs_url),
    }
