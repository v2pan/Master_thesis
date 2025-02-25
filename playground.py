from Main.combined_pipeline import combined_pipeline
from Utilities.database import query_database

combined_pipeline('''∃x ∃y ∃z (children_table(x, y) ∧ fathers(x, z))''')
