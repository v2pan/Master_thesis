#File reserved for testing purposes during development
from combined_pipeline import combined_pipeline

calculus='''∃id (children_table(id, >1) ∧ fathers(id, ))'''
combined_pipeline(calculus)