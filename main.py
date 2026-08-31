from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from ingest import ingest
from rag_pipeline import build_pipeline
import shutil

app = FastAPI()

class AskRequest(BaseModel):
    question: str
    
vectorstore = None
agent = None

@app.post("/ask")
def ask(request: AskRequest):
    result = agent.invoke({"question": request.question, "trials": 0})
    if agent is None:
        return {"your pdf hasnt uploaded yet. please upload your pdf"}
    else:
        return {"answer": result["answer"]}
@app.post("/upload")
def upload(file: UploadFile= File(...)):
    global vectorstore, agent
    pdf_path = "uploaded.pdf"
    with open(pdf_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    vectorstore = ingest(pdf_path)
    agent = build_pipeline(vectorstore)
    return {"message": "pdf uplodead succesfully and processed succesfully"}

    
    