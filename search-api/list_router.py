from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from deps import user_role
from typing import Any
import httpx


router = APIRouter()

@router.get("/list")
async def list_tasks(id: int | None = None, limit: int | None = None, offset: int = 0,
                     user_role = Depends(user_role)):
    if user_role != "ROLE_USER":
        raise HTTPException(status_code=403, detail="Forbidden.")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://tasks-api:8000/task/list?{f"id={id}&" if id else ""}{f"limit={limit}&" if limit else ""}offset={offset}")
    return response.json()