import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()
client=Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

#sending a request

response=client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "Explain what a movie and its affect is is in two sentences."
        },
        {
            "role":"system",
            "content":"You are Talking Tomatoes, a friendly entertainment companion who recommends movies and TV shows. Keep your responses conversational and concise."
        }
    ]
)


#print(response.choices[0].message.content)
print("Response:", response.choices[0].message.content)
print("Model:", response.model)
print("Tokens used:", response.usage.total_tokens)
