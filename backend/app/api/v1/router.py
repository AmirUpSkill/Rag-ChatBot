from fastapi import APIRouter
from .endpoints import auth,documents, chat , system 

api_router = APIRouter(prefix="/v1")


# --- Include all the endpoints routers --- 
api_router.include_router(auth.router)
api_router.include_router(documents.router)
api_router.include_router(chat.router)  
api_router.include_router(system.router)