import pandas as pd
from minimization import minimize_dfa

# Create the transition table
transition_table = pd.DataFrame({
    'Estados': ['S0', 'S1', 'S2', 'S3'],
    'a': ['S1', 'S0', 'S3', 'S2'],
    'b': ['S3', 'S2', 'S1', 'S0']
})

# Define the acceptance states
acceptance_states = ['S1', 'S3']

# Minimize the DFA
minimized_table = minimize_dfa(transition_table, acceptance_states)

# Print the minimized table
print(minimized_table)
