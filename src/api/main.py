from fastapi import FastAPI
from api.routes import parser

app = FastAPI(
    title="Prefab Smart Parser",
    description="AI-powered tool for parsing prefab product data",
    version="1.0.0"
)

app.include_router(parser.router) 