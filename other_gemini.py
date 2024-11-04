import google.generativeai as genai

with open("api_key.txt", "r") as file:
    api_key = file.read().strip()  # Read the file and remove any surrounding whitespace

def ask_gemini(prompt):
    genai.configure(api_key=api_key)
    # generation_config=genai.GenerationConfig(
    #     response_mime_type="application/json", response_schema=list[Recipe]
    # ),
    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content(prompt)
    return result.text

#ask_gemini("Are you there?")