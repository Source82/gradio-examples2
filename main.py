from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import os
import shutil

app = FastAPI()

# Mount the static directory to serve CSS, fonts, and other static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Ensure data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload(files: list[UploadFile] = File(...), mode: str = Form(...), question: str = Form(...)):
    file_paths = []
    for file in files:
        # Rename the file to remove spaces
        filename = file.filename.replace(" ", "_")
        file_path = os.path.join("data", filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_paths.append(file_path)
    root_directory = os.path.abspath("data")
    output = f"Processed with PDF files: {file_paths}\nRoot Directory: {root_directory}\nMode: {mode}\nUser's Question: {question}"
    return {"output": output}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
