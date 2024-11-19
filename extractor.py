from other_gemini import ask_gemini


#Extract some fragment form the response
def extract(response, start_marker="§-+",end_marker="§-+", multiple=False, inclusive=False):
    # Markers for identifying the updated query
    if multiple:
        if not inclusive:
            # Find all occurrences of the start marker
            start_indices = [i for i in range(len(response)) if response.startswith(start_marker, i)]
            
            # Extract the modified queries
            new_queries = []
            for start_index in start_indices:
                end_index = response.find(end_marker, start_index + len(start_marker))
                if end_index != -1:
                    new_queries.append(response[start_index + len(start_marker):end_index].strip())
            return new_queries
        else:
            # Find all occurrences of the start marker
            start_indices = [i for i in range(len(response)) if response.startswith(start_marker, i)]
            
            # Extract the modified queries
            new_queries = []
            for start_index in start_indices:
                end_index = response.find(end_marker, start_index + len(start_marker))
                if end_index != -1:
                    new_queries.append(response[start_index :end_index + 1].strip())
            return new_queries
    
    else:    
        # Find the start and end of the new query in the response
        if not inclusive:
            try:
                start_index = response.find(start_marker)
                end_index = response.find(end_marker, start_index + len(start_marker))
            except:
                return None        # Extract the modified query if it exists
            if start_index != -1 and end_index != -1:
                new_query = response[start_index + len(start_marker):end_index].strip()
            else:
                new_query=None
            
            return new_query
        else:
            try:
                start_index = response.find(start_marker)
                end_index = response.find(end_marker, start_index + len(start_marker))
            except:
                return None        # Extract the modified query if it exists
            if start_index != -1 and end_index != -1:
                new_query = response[start_index :end_index + 1].strip()
            else:
                new_query=None
            
            return new_query 