# app/llm/generator.py (نسخه به‌روز)
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv('.envv')

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    default_headers={
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "RAG Banking Assistant"
    }
)

def generate_answer(prompt: str) -> str:
 
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500,
            top_p=0.9
        )
        
        answer = completion.choices[0].message.content
        return answer.strip()
    
    except Exception as e:
        print(f"❌ خطا در ارتباط با OpenRouter: {e}")
        return "متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید."