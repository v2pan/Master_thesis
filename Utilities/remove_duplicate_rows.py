# from Main.combined_pipeline import combined_pipeline
# answer=combined_pipeline('''∃id ∃shares ∃name (shareowner(id, name, shares) ∧ animalowner(id, _, 'dog'))''')
# print(answer)

def remove_duplicate_rows(output, total_dic):
    cleaned_rows = []
    seen_rows = set()
    if output is not None:
        for row in output:
            row_list = list(row)  # Convert tuple to list for modification
            modified_versions = set()

            # Generate all possible versions of the row using the dictionary
            for i, value in enumerate(row_list):
                if value in total_dic:
                    for synonym in total_dic[value]:
                        temp_row = row_list[:]
                        temp_row[i] = synonym
                        modified_versions.add(frozenset(temp_row))

            # Check if the row or any of its modified versions is already seen
            if any(variant in seen_rows for variant in modified_versions) or frozenset(row) in seen_rows or row in seen_rows:
                continue  # Skip this row if a duplicate exists

            # Otherwise, add the row and its variants to seen_rows
            cleaned_rows.append(row)
            seen_rows.add(tuple(row))
            seen_rows.update(modified_versions)  # Mark modified versions as seen

    return cleaned_rows
        

    

