from fastapi import FastAPI, HTTPException, Form
import cloudinary
from cloudinary import api
from fastapi.middleware.cors import CORSMiddleware
import cloudinary.utils
from pydantic import BaseModel, EmailStr, Field
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os
from dotenv import load_dotenv 

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)




cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

# class ContactForm(BaseModel):
#     first_name: str = Field(..., min_length=3, max_length=20)
#     last_name: str = Field(..., min_length=3, max_length=20)
#     email: EmailStr
#     phone: str = Field(..., min_length=10, max_length=11)
#     event_date: str
#     venue: str = Field(min_length=10, max_length=40)
#     message: str = Field(min_length=10, max_length=40)

@app.get("/images")
def fetch_images():
    images = cloudinary.api.resources(type="upload", resource_type="image", max_results=70)
    # Get secure URL for each image
    signed_image_url = []
    for image in images.get("resources", []):
        signed_url, options = cloudinary.utils.cloudinary_url(
            image["public_id"],
            sign_url=True,
            transformation=[{"fetch_format": "auto", "quality": "auto", "width": 800, "crop": "limit"}],
            expire=10
        )
        signed_image_url.append(signed_url)
    return {"images": signed_image_url}



