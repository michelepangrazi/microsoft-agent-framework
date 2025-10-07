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
        instructions="You are good at telling jokes.",
        name="Joker"
    )

thread = agent.get_new_thread()

async def main():
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["/exit", "/quit", "/q"]:
            print("Exiting the conversation.")
            break
        result = await agent.run(user_input, thread=thread)
        print(result.text)    

asyncio.run(main())