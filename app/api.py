import os

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

# the "app" directory
base_path = Path(__file__).parent

description = base_path.joinpath('README.md').read_text(encoding='utf-8')
enroller = FastAPI(
    title="Government Agency",
    description=description,
    version="0.0.1"
)
templates = None

views_path = base_path.joinpath('views')
if os.path.exists(views_path):
    views = Jinja2Templates(directory=views_path)
else:
    raise Exception("Could not find Views directory. Expecting 'views/'.")

@enroller.get("/")
async def read_root(request: Request):
    return views.TemplateResponse("warning/non_conforming.html", { "request": request })
