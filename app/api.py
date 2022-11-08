import os

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

description = Path("README.md").read_text(encoding='utf-8')
enroller = FastAPI(
    title="Government Agency",
    description=description,
    version="0.0.1"
)
templates = None

if os.path.exists("views"):
    views = Jinja2Templates(directory="views")
else:
    raise Exception("Could not find Views directory. Expecting 'views/'.")

@enroller.get("/")
async def read_root(request: Request):
    return views.TemplateResponse("warning/conforming.html", { "request": request })

@enroller.get("/bad")
async def read_root(request: Request):
    return views.TemplateResponse("warning/non_conforming.html", { "request": request })
