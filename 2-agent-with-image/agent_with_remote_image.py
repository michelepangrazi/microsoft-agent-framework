import asyncio, os
from agent_framework.azure import AzureOpenAIChatClient

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION")
ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT_NAME = os.environ.get("AZURE_OPENAI_MODEL")

agent = AzureOpenAIChatClient(
        api_key=API_KEY,
        deployment_name=DEPLOYMENT_NAME,
        api_version=API_VERSION,
        endpoint=ENDPOINT,
    ).create_agent(
        instructions="You are a helpful agent that can analyze images",
        name="VisionAgent"
    )

from agent_framework import ChatMessage, TextContent, UriContent, Role

#From uri
image_url = "https://cdn.jetphotos.com/full/5/1492996_1699008046.jpg"
message = ChatMessage(
    role=Role.USER, 
    contents=[
        TextContent(text="What do you see in this image?"),
        UriContent(uri=image_url, media_type="image/jpeg")
    ]
)

async def main():
    async for update in agent.run_stream(message):
        if update.text:
            print(update.text, end="", flush=True)
    print()

asyncio.run(main())