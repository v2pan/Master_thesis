import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Sample data (your penguins_example DataFrame)
data = {
    "island": ["Biscoe", "Biscoe", "Dream", "Dream", "Torgersen", "Torgersen", "Biscoe", "Dream", "Torgersen"],
    "body_mass_g": [3750, 3800, 3600, 3500, 3900, 4000, 3700, 3400, 4100],
    "species": ['Adelie', 'Adelie', 'Gentoo', 'Gentoo', 'Chinstrap', 'Chinstrap', 'Adelie', 'Gentoo', 'Chinstrap'],
    "bill_length_mm":[39, 38, 47, 46, 46, 45, 37, 49, 44],
    "bill_depth_mm":[18, 19, 14, 15, 15, 17, 17, 13, 16],
    "flipper_length_mm":[181, 185, 217, 220, 197, 195, 190, 215, 200],
    "sex": ['Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Female', 'Male', 'Female']
}

penguins_example = pd.DataFrame(data)


#Seaborn barplot
plt.figure(figsize=(8, 6))
sns.barplot(x="island", y="body_mass_g", data=penguins_example, estimator=sum, ci=None) #ci=None removes confidence intervals
plt.xlabel("Island")
plt.ylabel("Mean Body Mass (g)")
plt.title("Penguin Body Mass by Island (Example Data)")
plt.show()