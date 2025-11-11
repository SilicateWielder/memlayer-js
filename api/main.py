from fastapi import FastAPI
from api.status import router as status_router
from api.chat import router as chat_router # <-- Add this import

app = FastAPI(title="Memory Layer API")

@app.get("/")
def read_root():
    return {"message": "Memory Layer API is running."}

# Include routers
app.include_router(status_router)
app.include_router(chat_router) # <-- Add this line