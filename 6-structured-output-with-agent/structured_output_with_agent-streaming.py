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
    from agent_framework import AgentRunResponse

    # Get structured response from streaming agent using AgentRunResponse.from_agent_response_generator
    # This method collects all streaming updates and combines them into a single AgentRunResponse
    final_response = await AgentRunResponse.from_agent_response_generator(
        agent.run_stream("Please provide information about John Smith, who is a 35-year-old software engineer.", response_format=PersonInfo),
        output_format_type=PersonInfo,
    )

    if final_response.value:
        person_info = final_response.value
        print(f"Name: {person_info.name}, Age: {person_info.age}, Occupation: {person_info.occupation}")
        
asyncio.run(main())