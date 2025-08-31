from fastapi import Header, HTTPException
from typing import Optional

async def x_api_key(x_api_key: Optional[str] = Header(None)):
# Optional: simple header-based auth you can turn on behind a proxy
 if False: # set to True to enforce and compare against env value
    if x_api_key != "CHANGE_ME":
         raise HTTPException(status_code=401, detail="Unauthorized")