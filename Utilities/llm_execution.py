import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import google.generativeai as genai
import json
import typing_extensions as typing
from Utilities.database import query_database
from google.api_core.exceptions import ResourceExhausted
from ollama import chat
from ollama import ChatResponse
from ollama import ResponseError
import ollama
from typing import List
from llm_generation import TextLLM





instruction_prompt='''You are a validator. You have to access whether the following articles are the same. Think about the context of this article. If you think they have any connection answer with \"yes\". Validate the following statement using \"no\" and \"yes\" only!'''

textllm=TextLLM()

def ask_llm(prompt, return_metadata=False, temp=1.0, max_token=4096 ):  # Add optional argument
    if not return_metadata:
        answer= textllm(prompt, instruction_prompt=instruction_prompt)
        return answer
    else:
        answer,metadata=textllm(prompt, return_metadata=True , instruction_prompt=instruction_prompt)
        return answer, metadata




def llm_json(prompt,response_type, return_metadata=False):
    """
    Sends a prompt to the LLM and returns the response as JSON.

    Args:
        prompt (str): The prompt to send to the LLM.
        response_type (str): The expected type of the response. 
            Must be one of: "int", "float", "bool", "str".

    Returns:
        dict: The response from the LLM as a JSON dictionary.
        (metadata): The metadata from the LLM as a JSON dictionary.

    """
    json_metadata={'candidates_token_count': 0, 'prompt_token_count': 0, 'total_calls': 0, 'total_token_count': 0}
        
    if response_type == list[bool]:
        output = []
        
        # Define the batch size
        batch_size = 1

        # Loop through the prompt list in batches
        for i in range(0, len(prompt), batch_size):
            # Get the current batch of questions
            batch = prompt[i:i + batch_size]
            
            # Process the batch of questions
            response, metadata = textllm(batch[0].replace("\n", ""), return_metadata=True, boolean=True, instruction_prompt=instruction_prompt)

            for i in metadata.keys():
                json_metadata[i]+=metadata[i]
            
            # Append the responses from the batch to the output list
            output.append(response)
    if response_type==bool:
        output, metadata=textllm(prompt, return_metadata=True, boolean=True, instruction_prompt=instruction_prompt)

        for i in metadata.keys():
            json_metadata[i] += metadata[i]
    
    if not return_metadata:
        return output

    else:
        return output, json_metadata





# Function to get embeddings from OpenAI
def get_embedding(text):
    return textllm.get_embedding(text)


#Define Filter class for ret
class QUERY(typing.TypedDict):
    query: str
class CATEGORY(typing.TypedDict):
    category: str
class Table(typing.TypedDict):
    category: str

#Function to update metadata
def add_metadata(metadata, usage_metadata_total):
    """
    Updates the usage metadata with the values from the input metadata dictionary.

    Args:
    - metadata (dict): The metadata dictionary to update the usage metadata with.
    """
    usage_metadata_total["prompt_token_count"] += metadata["prompt_token_count"]
    usage_metadata_total["candidates_token_count"] += metadata["candidates_token_count"]
    usage_metadata_total["total_token_count"] += metadata["total_token_count"]
    usage_metadata_total["total_calls"] += metadata["total_calls"]
    return usage_metadata_total
         

    


# answer,metadata=llm_json("Is Berlin the capital of Germany?", response_type=bool, return_metadata=True)
# print(answer)
# print(metadata)

