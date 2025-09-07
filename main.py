from fastapi import FastAPI, UploadFile, Form
import subprocess
import uuid
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/convert")
async def convert(file: UploadFile, format: str = Form(...)):
    # Save uploaded file
    input_path = f"{UPLOAD_DIR}/{uuid.uuid4()}_{file.filename}"
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Output path
    output_filename = f"{uuid.uuid4()}.{format}"
    output_path = f"{OUTPUT_DIR}/{output_filename}"

    # Run ffmpeg
    command = ["ffmpeg", "-i", input_path, output_path]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return {"message": "Conversion complete", "output_file": output_filename}
