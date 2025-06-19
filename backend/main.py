from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from scrape import scrape_product_data
from generate_ad import generate_ad_script
from generate_video import create_video_ad
from fastapi.staticfiles import StaticFiles


# Serve the 'generated' folder at the '/generated' URL path

from fastapi.responses import FileResponse
import os



app = FastAPI()

# Enable CORS so frontend can call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with frontend origin if deployed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/generated/{video_filename}")
def get_video_file(video_filename: str):
    video_path = os.path.join("generated", video_filename)
    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename=video_filename,
    )


class URLRequest(BaseModel):
    url: str

@app.post("/generate")
async def generate_video_from_url(request: URLRequest):
    url = request.url

    # 1. Scrape product info
    product_data = scrape_product_data(url)

    # 2. Generate ad script
    ad_script = generate_ad_script(product_data)

    # 3. Generate video
    video_path = create_video_ad(product_data, ad_script)

    return {"video_url": f"http://localhost:8000/{video_path}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
