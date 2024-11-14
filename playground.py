import google.generativeai as genai
from vertexai.generative_models import GenerationConfig, GenerativeModel, Part
from database import query_database
import vertexai
from vertexai.generative_models import GenerativeModel

# TODO(developer): Update and un-comment below line
# PROJECT_ID = "your-project-id"
with open("api_key.txt", "r") as file:
    api_key = file.read().strip()  # Read the file and remove any surrounding whitespace
genai.configure(api_key=api_key)


prompt='''
CREATE OR REPLACE FUNCTION normalize_category(category TEXT)
RETURNS TEXT AS $$
# Define a set of terms that mean "dog" in different languages
dog_terms = {'dog', 'chien', 'perro', 'Hund', 'cane'}
if category in dog_terms:
    return 'dog'
return category
$$ LANGUAGE plpython3u;

SELECT T1.name, T1.shares
FROM shareowner1row AS T1
INNER JOIN animalowner1row AS T2 ON T1.id = T2.owner_id
WHERE normalize_category(T2.category) = 'dog';
'''
query_database(prompt,True)

# Example response:
# **Emphasizing the Dried Aspect:**
# * Everlasting Blooms
# * Dried & Delightful
# * The Petal Preserve
# ...

# chat = model.start_chat(
#     history=[
#         {"role": "user", "parts": "Hi my name is Bob"},
#         {"role": "model", "parts": "Hi Bob!"},
#     ]
# )
# # Call `count_tokens` to get the input token count (`total_tokens`).
# print(model.count_tokens(chat.history))
# # ( total_tokens: 10 )

# response = chat.send_message(
#     "In one sentence, explain how a computer works to a young child."
# )

# print(response.text)
# print(response.usage_metadata)
# from google.generativeai.types.content_types import to_contents
# # You can call `count_tokens` on the combined history and content of the next turn.
# print(model.count_tokens(chat.history + to_contents("What is the meaning of life?")))

