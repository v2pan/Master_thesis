import sys
import os
sys.path.insert(0, '/home/vlapan/Documents/Masterarbeit/Relational')
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


class RessourceError(Exception):
    pass

script_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(script_dir, "api_key.txt"), "r") as file:
    api_key = file.read().strip()  # Read the file and remove any surrounding whitespace

genai.configure(api_key=api_key)


#For the model gemini-1.5-flash, the rate limits are
# 15 RPM
# 1 million TPM
# 1,500 RPD

MODEL="gemini-1.5-flash"
# "gemini-1.5-flash"
# "gemini-2.0-flash"
#"deepseek-r1:1.5b"
#"llama3.2"
def ask_llm(prompt, return_metadata=False, temp=1.0, max_token=4096 ,model=MODEL):  # Add optional argument
    """
    Return the answer to the question

    Args:
        prompt: The input prompt.

    Returns:
        The answer as text.  Raises exception if error occurs
        (Metadata): The metadata from the LLM call.
    """
    if "gemini" in model:
        model = genai.GenerativeModel(model)
        try:
            result = model.generate_content(contents=prompt,
            generation_config=genai.types.GenerationConfig(
            # Only one candidate for now.
            max_output_tokens=max_token,
            temperature=temp,
        ),)
        except ResourceExhausted as e:
            print("Time exception has occured")
            raise RessourceError("API rate limit exceeded!")
        
        if return_metadata:
            usage_metadata = {
                "prompt_token_count": result.usage_metadata.prompt_token_count,
                "candidates_token_count": result.usage_metadata.candidates_token_count,
                "total_token_count": result.usage_metadata.total_token_count,
                "total_token_count": result.usage_metadata.total_token_count,
                "total_calls": 1
            }
            return result.text, usage_metadata
            
        else:
            return result.text  # Return only text if metadata not requested
    else:
        
        try:
            response: ChatResponse = chat(model=model, messages=[
            {
                'role': 'user',
                'content': prompt,
            }])
            output = response.message.content
            if not return_metadata:
                return output
            else:
                metadata={"prompt_token_count": response.prompt_eval_count,
                "candidates_token_count": response.eval_count,
                "total_token_count": response.prompt_eval_count + response.eval_count,
                "total_calls": 1}
                return output, metadata
        except ResponseError as e:
            print('Error:', e.error)
            if e.status_code == 404:
                print('Model not found')
    







def llm_json(prompt,response_type, model=MODEL, return_metadata=False):
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
    if "gemini" in model:
        try:
            model = genai.GenerativeModel(model)
            result = model.generate_content(
                #"Answer the following questions [Does 'dog' and 'chien' have the same semantic meaning?, Does 'dog' and 'chat have the same semantic meaning?, Does dog and cat have the same semantic meaning?]",
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json", response_schema=response_type
                ),
            )
            #print(f"The result text is {result.text}")
            json_data=json.loads(result.text)
            if return_metadata:
                usage_metadata = {
                    "prompt_token_count": result.usage_metadata.prompt_token_count,
                    "candidates_token_count": result.usage_metadata.candidates_token_count,
                    "total_token_count": result.usage_metadata.total_token_count,
                    "total_calls": 1
                }
                return json_data, usage_metadata
            else:
                return json_data
        except ResourceExhausted as e:
            print("Time exception has occured in JSOn")
            raise RessourceError("API rate limit exceeded!")
        
    else:
       
        try:
            if response_type==list[bool]:
                format={"type": "object", "properties":{"answer": {"type": "array", "items": {"type": "boolean"}}} }
            if response_type==bool:
                format={"type": "object", "properties":{"answer": {"type": "boolean"}} }
            output=None
            while output is None:
                response: ChatResponse = chat(model=model, messages=[
                {
                    'role': 'user',
                    'content': prompt,
                }], format=format)

                output = response.message.content
                output= extract_boolean_values(output)
            if not return_metadata:
                return output

            else:
                metadata={"prompt_token_count": response.prompt_eval_count,
                "candidates_token_count": response.eval_count,
                "total_token_count": response.prompt_eval_count + response.eval_count,
                "total_calls": 1}
                return output, metadata
        except ResponseError as e:
            print('Error:', e.error)
            if e.status_code == 404:
                print('Model not found')




# Function to get embeddings from OpenAI
def get_embedding(text,task_type="retrieval_document"):
    result = genai.embed_content(
    model="models/text-embedding-004",
    content=text,
    task_type=task_type,
    title="Embedding of single string")
    # 1 input > 1 vector output
    return result['embedding']


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

def extract_boolean_values(response_string):
    """
    Extracts the boolean value from a JSON string.

    Args:
        response_string: The JSON string containing the answer.

    Returns:
        The boolean value if found and the string is valid JSON, otherwise None.  Raises exception if input is not a string.
    """

    if not isinstance(response_string, str):
        raise TypeError("Input must be a string.")

    try:
        response_dict = json.loads(response_string)
        answer = response_dict.get("answer")
        if answer is not None and isinstance(answer, list):
            for a in answer:
                if not isinstance(a, bool):
                    raise ValueError("The output of the model is not a list of booleans.")
            return answer
        elif answer is not None and isinstance(answer, bool):
            return answer
        else:
          print("The output of the model is nor a list nor a boolean")  # Or raise a more specific exception
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None  # Or raise a more specific exception
         

    


print(llm_json("Is Berlin the capital of Germany?", response_type=bool))
