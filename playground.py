from Main.combined_pipeline import combined_pipeline

output,metadata=combined_pipeline('''∃id ∃shares ∃name (shareowner(id, name, shares) ∧ animalowner(id, _, 'dog'))''')
print(output)