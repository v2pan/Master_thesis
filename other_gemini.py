import google.generativeai as genai
import json
import typing_extensions as typing
from database import query_database
from google.api_core.exceptions import ResourceExhausted

class RessourceError(Exception):
    pass

with open("api_key.txt", "r") as file:
    api_key = file.read().strip()  # Read the file and remove any surrounding whitespace
genai.configure(api_key=api_key)

#For the model gemini-1.5-flash, the rate limits are
# 15 RPM
# 1 million TPM
# 1,500 RPD

def ask_gemini(prompt, return_metadata=False, temp=1.0, max_token=4096 ,model="gemini-1.5-flash-8b"):  # Add optional argument
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


# Function to get embeddings from OpenAI
def get_embedding(text,task_type="retrieval_document"):
    result = genai.embed_content(
    model="models/text-embedding-004",
    content=text,
    task_type=task_type,
    title="Embedding of single string")
    # 1 input > 1 vector output
    return result['embedding']



def gemini_json(prompt,response_type, model="gemini-1.5-flash", return_metadata=False):
    """
    Sends a prompt to the Gemini API and returns the response as JSON.

    Args:
        prompt (str): The prompt to send to the Gemini API.
        response_type (str): The expected type of the response. 
            Must be one of: "int", "float", "bool", "str".

    Returns:
        dict: The response from the Gemini API as a JSON dictionary.

    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
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
        print("Time exception has occured")
        raise RessourceError("API rate limit exceeded!")
#Define Filter class for ret
class QUERY(typing.TypedDict):
    query: str
class CATEGORY(typing.TypedDict):
    category: str
class Table(typing.TypedDict):
    category: str

#Function to update metadata
# def update_metadata(metadata, usage_metadata_total):
#     """
#     Updates the usage metadata with the values from the input metadata dictionary.

#     Args:
#     - metadata (dict): The metadata dictionary to update the usage metadata with.
#     """
#     usage_metadata_total["prompt_token_count"] += metadata["prompt_token_count"]
#     usage_metadata_total["candidates_token_count"] += metadata["candidates_token_count"]
#     usage_metadata_total["total_token_count"] += metadata["total_token_count"]
#     usage_metadata_total["total_calls"] += 1
#     return usage_metadata_total
    

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
    


# print(response)

# prompt='''Answer the following questions with True or False. If the units are different,
# rewrite all to the same unit and only then answer the question.
# The questions are 
#  \n '200 °F'  is greater than '200 °C' \n
# '400 °F'  is greater than '200 °C' \n 
# '350 °F'  is greater than '200 °C' \n
#  '200 °F'  is greater than '200 °C' \n'''

# prompt='''Answer the following questions with True or False. 
# The questions are 
#  \n '400 °C'  is greater than '200 °C' \n
# '100 °C'  is greater than '200 °C' \n 
# '50 °C'  is greater than '200 °C' \n
#  '800 °F'  is greater than '200 °C' \n'''
# prompt="Answer the following questions with True or False. Reason you thinking, especially considering the units, converting units to another and then answering the question.  \n '200 °F'  is greater than '200 °C' \n '400 °F'  is greater than '200 °C' \n '350 °F'  is greater than '200 °C' \n '200 °F'  is greater than '200 °C' \n"

# true_reponse=[False, True, False, False]

# models = ["gemini-1.5-flash", "gemini-1.5-flash-8b", ]
# num_tries = 3

# results = {}
# for model in models:
#     results[model] = []
#     for i in range(num_tries):
#         #response = gemini_json(prompt, response_type=list[bool])

#         answer=ask_gemini(prompt)
#         response = gemini_json(f"For this question \n{prompt} \n The following asnwer was given {answer}. Return the necessary answer whether this question is true or False", response_type=list[bool])  # Expect a list of booleans back

#         results[model].append(response)

# # Print the results in a table format
# print("| Try |", end="")
# for model in models:
#     print(f" {model} |", end="")
# print()
# print("|---|---|---|")
# for i in range(num_tries):
#     print(f"| {i+1} | {results[models[0]][i]} | {results[models[1]][i]} |")
