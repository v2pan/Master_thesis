import google.generativeai as genai

with open("api_key.txt", "r") as file:
    api_key = file.read().strip()  # Read the file and remove any surrounding whitespace
genai.configure(api_key=api_key)
def ask_gemini(prompt):
    #genai.configure(api_key=api_key)
    # generation_config=genai.GenerationConfig(
    #     response_mime_type="application/json", response_schema=list[Recipe]
    # ),
    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content(prompt)
    return result.text

#ask_gemini("Are you there?")

# Function to get embeddings from OpenAI
def get_embedding(text,task_type="retrieval_document"):
    result = genai.embed_content(
    model="models/text-embedding-004",
    content=text,
    task_type=task_type,
    title="Embedding of single string")
    # 1 input > 1 vector output
    return result['embedding']


