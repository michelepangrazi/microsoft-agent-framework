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
        name="HelpfulAssistant",
        instructions="You are a helpful assistant that extracts person information from text."
    )
    
from pydantic import BaseModel

class PersonInfo(BaseModel):
    """Information about a person."""
    name: str | None = None
    age: int | None = None
    occupation: str | None = None
    
async def main():    
    response = await agent.run(
        "Please provide information about John Smith, who is a 35-year-old software engineer.", 
        response_format=PersonInfo
    )
    if response.value:
        person_info = response.value
        print(f"Name: {person_info.name}, Age: {person_info.age}, Occupation: {person_info.occupation}")
    else:
        print("No structured data found in response")
        
asyncio.run(main())