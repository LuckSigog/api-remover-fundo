from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import numpy as np
import io

app = FastAPI()

@app.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    try:
        input_file = await file.read()
        input_image = Image.open(io.BytesIO(input_file))
        input_array = np.array(input_image)
        output_array = remove(input_array)
        output_image = Image.fromarray(output_array)
        buffer = io.BytesIO()
        output_image.save(buffer, format="PNG")
        buffer.seek(0)
        return StreamingResponse(buffer, media_type="image/png")
    except Exception as e:
        return {"error": str(e)}
