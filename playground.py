dic1 = {"Peter": 1, "John": 2, "Mary": 3}
dic2 = {"Peter": 3, "John": 2, "Mary": 1}

dic3 = dic1.copy()  # Create a copy of dic1
dic3.update(dic2)  # Update the copy with dic2's values
print(dic3)
print(dic1)