from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import io
import base64

# Initialize FastAPI app
app = FastAPI()

# Load the Stable Diffusion model pipeline
try:
    pipe = StableDiffusionPipeline.from_pretrained(
        "D:/Text-To-Image-Generation-Using-Stable-Diffusion/models", 
        torch_dtype=torch.float32
    ).to("cpu")
except Exception as e:
    raise RuntimeError(f"Failed to load the model: {e}")

# Static files and templates setup
# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Define a Pydantic model for request validation
class Prompt(BaseModel):
    prompt: str

# Main page route to serve HTML form
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint for generating images
@app.post("/generate-image")
async def generate_image(prompt: Prompt):
    try:
        # Generate the image based on the provided prompt
        with torch.no_grad():
            image = pipe(prompt.prompt).images[0]

        # Save image to a bytes buffer
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        
        # Encode the image as base64 to send it to the frontend
        image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        
        # Return the image as a data URI (inline base64)
        return {"image_url": f"data:image/png;base64,{image_base64}"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating image: {e}")
