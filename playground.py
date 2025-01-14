def compare_dictionaries_unordered(dict1, dict2):
    """Compares dictionaries, ignoring the order of elements in lists."""
    if dict1.keys() != dict2.keys():
        return False  # Different keys

    for key in dict1:
        if not isinstance(dict1[key], list) or not isinstance(dict2[key], list):
            if dict1[key] != dict2[key]: #check non-list items
              return False
        elif set(dict1[key]) != set(dict2[key]):  # Compare sets to ignore list order
            return False

    return True  # Dictionaries are equivalent (ignoring list order)

dict1 = {
                "makeuptutorial": [
                    "makeuptutorial"
                ],
                "outsideguy": [],
                "surviver1000": [
                    "surviver10",
                    "surviver1000"
                ],
                "princess": [
                    "princess"
                ]
            }
dict2 = {
                "makeuptutorial": [
                    "makeuptutorial"

                ],
                "princess": [
                    "princess"
                ],
                "outsideguy": [],
                "surviver1000": [
                    "surviver1000",
                    "surviver10"
                ]
                
            }

print(compare_dictionaries_unordered(dict1, dict2))

