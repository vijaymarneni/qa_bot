import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from .qa_bot import process_file, answer_question
from .config import UPLOAD_DIR
from .vector_store import load_store
import shutil

app = FastAPI()
load_store()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <body>
            <h2>Upload a file or ask a question</h2>
            <form action="/upload" method="post" enctype="multipart/form-data">
                File:<input type="file" name="file">
                <input type="submit" value="Upload File">
            </form>
            <form action="/ask" method="post">
                Question: <input type="text" name="query_text" placeholder="Ask a question">
                <input type="submit" value="Ask">
            </form>
        </body>
    </html>
    """

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR,file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": process_file(file_path)}

@app.post("/ask")
async def ask_question(query_text: str = Form(...)):
    answer = answer_question(query_text)
    return {"Question": query_text, "Answer": answer}




