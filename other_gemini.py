import google.generativeai as genai
import json
# import base64
# import vertexai
# from vertexai.generative_models import GenerationConfig, GenerativeModel, Part
import typing_extensions as typing
with open("api_key.txt", "r") as file:
    api_key = file.read().strip()  # Read the file and remove any surrounding whitespace
genai.configure(api_key=api_key)

def ask_gemini(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content(contents=prompt)
    return result.text


# Function to get embeddings from OpenAI
def get_embedding(text,task_type="retrieval_document"):
    result = genai.embed_content(
    model="models/text-embedding-004",
    content=text,
    task_type=task_type,
    title="Embedding of single string")
    # 1 input > 1 vector output
    return result['embedding']



def gemini_json(prompt,response_type):
    """
    Sends a prompt to the Gemini API and returns the response as JSON.

    Args:
        prompt (str): The prompt to send to the Gemini API.
        response_type (str): The expected type of the response. 
            Must be one of: "int", "float", "bool", "str".

    Returns:
        dict: The response from the Gemini API as a JSON dictionary.

    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content(
        #"Answer the following questions [Does 'dog' and 'chien' have the same semantic meaning?, Does 'dog' and 'chat have the same semantic meaning?, Does dog and cat have the same semantic meaning?]",
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=response_type
        ),
    )
    print(f"The result text is {result.text}")
    json_data=json.loads(result.text)
    return json_data
#Define Filter class for ret
class QUERY(typing.TypedDict):
    query: str
class CATEGORY(typing.TypedDict):
    category: str


# Create an instance of the FILTER class


# Access and modify attributes using dot notation
#  # Output: {'query': 'SELECT region FROM customerdetails', 'category': 'west'}