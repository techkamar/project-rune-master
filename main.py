from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from admin_controller import admin
from slave_controller import slave

app = FastAPI()

origins = [
    "https://rune-master-ui.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return "HELLO WORLD"
    
app.include_router(admin, prefix="/api")
app.include_router(slave, prefix="/api")
