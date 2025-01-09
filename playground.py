import os
import json

def load_json_file(filepath):
    """Loads a JSON file into a Python list of dictionaries."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return data  # Return the list as is
        elif isinstance(data, dict):
            return [data]  # Wrap the dictionary in a list
        else:
            print(f"Error: Unexpected data format in {filepath}.  Expected list or dictionary.")
            return None
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data in {filepath}: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



# Example usage
filepath = os.path.join(os.getcwd(),"temporary", "total_test") # Replace with the actual path
loaded_data = load_json_file(filepath)

if loaded_data:
    print(len(loaded_data), "records loaded successfully.")
else:
    print("Failed to load the JSON file.")