from fastapi import Header, HTTPException
from typing import Optional

async def get_token_header(x_token: Optional[str] = Header(None)):
    if x_token is None:
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token
