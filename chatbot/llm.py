# from groq import Groq
# import os
# from dotenv import load_dotenv

# load_dotenv()

# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY")
# )

# def get_response(user_input):

#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[
#             {
#                 "role": "user",
#                 "content": user_input
#             }
#         ]
#     )

#     return response.choices[0].message.content
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def get_response(user_input):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    return response.choices[0].message.content