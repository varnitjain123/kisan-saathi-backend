import base64
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

def analyze_image(image_bytes: bytes) -> str:
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
                        "type": "text",
                        "text": """You are an agricultural expert examining a photo of a crop or plant.
Describe only what you see that is relevant to plant health:
- Visible symptoms (spots, discoloration, holes, wilting, lesions)
- Which parts are affected (leaves, stems, fruits, roots)
- Severity (mild, moderate, severe)
- Any visible pests or insects

Be specific and brief. Maximum 3 sentences.
If the image is not of a plant, say: NOT_A_PLANT"""
                    }
                ]
            }
        ]
    )
    
    description = response.choices[0].message.content.strip()
    
    if "NOT_A_PLANT" in description:
        return ""
    
    return f"Visual observation from farmer's photo: {description}"
