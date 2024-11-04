from other_gemini import ask_gemini

#Extract some fragment form the response
def extract(response, start_marker="§-+",end_marker="§-+"):
    # Markers for identifying the updated query

    # Find the start and end of the new query in the response
    start_index = response.find(start_marker)
    end_index = response.find(end_marker, start_index + len(start_marker))

    # Extract the modified query if it exists
    if start_index != -1 and end_index != -1:
        new_query = response[start_index + len(start_marker):end_index].strip()
    # else:
    #     print("Could not extract an updated query. Reattempting to obtain a more accurate query...")
    #     # Re-attempt to obtain a refined query
    #     reattempted_response = ask_gemini(f"Can you provide a more accurate version of the query? {query}. Please enclose the updated query in natural language in {start_marker} and {end_marker}.")
    #     # Attempt extraction again with reattempted response
    #     start_index = reattempted_response.find(start_marker)
    #     end_index = reattempted_response.find(end_marker, start_index + len(start_marker))
        
    #     if start_index != -1 and end_index != -1:
    #         new_query = reattempted_response[start_index + len(start_marker):end_index].strip()
    #     else:
    #         # If extraction still fails, fallback to the original query
    #         new_query = query
    #         print("No refined query was provided. Using the original query.")
    
    return new_query