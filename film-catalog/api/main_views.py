from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
async def read_root(
    request: Request,
    name: str = "World",
) -> dict[str, str]:
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "message": f"Hello {name}! Welcome to film catalog!",
        "docs": str(docs_url),
    }
