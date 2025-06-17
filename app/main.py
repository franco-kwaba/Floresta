from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Ajuda a montar caminhos a partir do app/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Templates
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Arquivos estáticos (se precisar)
STATIC_DIR = os.path.join(BASE_DIR, "web", "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
