import requests
import re

with open("api_key.txt", "r") as file:
    api_key = file.read().strip()  # Read the file and remove any surrounding whitespace

#print(api_key)  # Use the API key as needed

# Set the endpoint
url_gem = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

#cypher_code = '''MATCH (n)'''

def post_gemini(text, values=False):

    # Define the headers and payload
    headers = {
        'Content-Type': 'application/json',
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": text
                    }
                ]
            }
        ]
    }

    # Send the POST request
    response = requests.post(url_gem, headers=headers, json=payload)

    # Check the status and output the response
    if response.status_code == 200:
        #print("Success!")
        response=response.json()
        # Extract the text
        text = response['candidates'][0]['content']['parts'][0]['text']
        if values:
            query = re.search(r"```sql\n(.*?)\n```", text, re.DOTALL)
            if query:
                query = query.group(1)
                print(query)
            else:
                print("No match found")
            return query
        else:
            #print(text)
            return text

    else:
        print(f"Error: {response.status_code}")
        print(response.text)

#post_gemini('''What is 2+2?''')
#post_gemini('''What is the result of the last value multiplied with itself?''')


