from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))# System prompt - chatbot ke rules
system_prompt = """Tumhara naam Sneha hai. Tum Ali's Restaurant ke liye chatbot ho.
Menu:
- Biryani: Rs 450
- Butter Chicken: Rs 600
- Paneer Tikka Masala: Rs 500
- Daal Makhni: Rs 200
Agar 5 ya usse zyada items order hon, to 10% discount do.
Sirf menu, order, aur timings se related sawalon ka jawab do."""

# Conversation history store karne ke liye
conversation = [
    {"role": "system", "content": system_prompt}
]

# Ye batata hai ke /chat endpoint kaisa data expect karega
class Message(BaseModel):
    user_message: str

@app.get("/")
def home():
    return {"message": "Mera chatbot server chal raha hai!"}

@app.post("/chat")
def chat(msg: Message):
    # User ka message history mein add karo
    conversation.append({"role": "user", "content": msg.user_message})

    # OpenAI ko poori conversation bhejo
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation
    )

    bot_reply = response.choices[0].message.content

    # Bot ka jawab bhi history mein add karo
    conversation.append({"role": "assistant", "content": bot_reply})

    return {"bot_reply": bot_reply}