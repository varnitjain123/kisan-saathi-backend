import base64
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

class ImageNotUsableError(Exception):
    """Raised when the image is blurry, unclear, or not useful for diagnosis."""
    pass

def analyze_image(image_bytes: bytes) -> str:
    """
    Analyze a plant/crop image and return a text description of visible symptoms.
    Raises ImageNotUsableError if the image is blurry, unclear, or not a crop.
    """
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        }
                    },
                    {
                        "type":
