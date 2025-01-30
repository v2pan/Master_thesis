from other_gemini import ask_gemini

response,temp_meta = ask_gemini("What is the capital of France?", return_metadata=True)

print(response,temp_meta)