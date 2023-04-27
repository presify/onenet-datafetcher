from fastapi import Depends, FastAPI
from app import routers
import uvicorn

app = FastAPI()
app.include_router(routers.router)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
