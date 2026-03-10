from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

messages = [{"role":"user","content":"Tell about claude"}]

with client.messages.stream(
    model = "claude-haiku-4-5-20251001",
    max_tokens = 100,
    temperature = 0.1,
    messages = messages
) as stream:
    for text in stream.text_stream:
        print(text,end="",flush=True)

# print(stream.get_final_message())