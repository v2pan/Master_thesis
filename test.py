# import google.generativeai as genai

# with open("api_key.txt", "r") as file:
#     api_key = file.read().strip()  # Read the file and remove any surrounding whitespace
# genai.configure(api_key=api_key)

# model = genai.GenerativeModel("gemini-1.5-flash")
# chat = model.start_chat(
#     history=[
#         {"role": "user", "parts": "Hello. I am Vladimir"},
#         {"role": "model", "parts": "Hello Vladimir. What would you like to know?"},
#     ]
# )
# response = chat.send_message("I have 2 dogs in my house.", stream=False)
# for chunk in response:
#     print(chunk.text)
#     print("_" * 80)
# response = chat.send_message("What is my name?", stream=False)
# for chunk in response:
#     print(chunk.text)
#     print("_" * 80)

# print(chat.history)

print('Peter' in '("Peter",)')