from anthropic import Anthropic
from dotenv import load_dotenv 

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-0"

def add_user_message(messages,text):
    user_message = {"role":"user","content":text}
    messages.append(user_message)

def add_assistant_message(messages,text):
    assitant_message = {"role":"assistant","content":text}
    messages.append(assitant_message)

def chat(messages):
    system_prompt = """
                        You are old monk. With every answer you tell a small short life advise to the user in a line with no other 
                        needless reactions
                    """
    message = client.messages.create(
        model = model,
        max_tokens = 100,
        messages = messages,
        system = system_prompt
    )

    return message.content[0].text

messages = []

add_user_message(messages,"What is api")

answer = chat(messages)

add_assistant_message(messages,answer)

add_user_message(messages,"Tell full form alone")

answer2 = chat(messages)

print(answer2)