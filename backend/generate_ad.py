import openai
import os
from dotenv import load_dotenv
load_dotenv()

# Load OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_ad_script(product_data):
    title = product_data.get("title", "")
    features = product_data.get("features", [])

    features_text = "\n- " + "\n- ".join(features[:4])  # only use first 4 features
    prompt = f"""
Create a 15–30 second video ad script for a product titled:
"{title}"

Key features:{features_text}

Write in a short, energetic, and persuasive tone.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative marketing assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.8
        )
        ad_script = response["choices"][0]["message"]["content"]
        return ad_script
    except Exception as e:
        return f"Error generating ad: {e}"
