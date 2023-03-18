import pandas as pd

def minimize_dfa(transition_table, acceptance_states):
    # Remove unreachable states
    reachable_states = set('S0') # Start with the initial state
    old_size = 0
    while len(reachable_states) != old_size:
        old_size = len(reachable_states)
        for state in reachable_states.copy():
            for symbol in transition_table.columns[1:]:
                next_state = transition_table.loc[transition_table['Estados'] == state, symbol].values[0]
                reachable_states.add(next_state)
    reachable_states = list(reachable_states)
    reachable_table = transition_table.loc[transition_table['Estados'].isin(reachable_states)].reset_index(drop=True)

    # Initialize the table of distinguishable states
    partition = [set(acceptance_states), set(reachable_states) - set(acceptance_states)]
    table = pd.DataFrame(index=range(len(partition)), columns=transition_table.columns[1:], dtype=object)

    # Find distinguishable states
    while True:
        new_partition = []
        for i, group in enumerate(partition):
            for symbol in transition_table.columns[1:]:
                partition_dict = {}
                for state in group:
                    next_state = reachable_table.loc[reachable_table['Estados'] == state, symbol].values[0]
                    for j, subgroup in enumerate(partition):
                        if next_state in subgroup:
                            partition_dict[j] = partition_dict.get(j, set()) | set([state])
                new_partition.extend(partition_dict.values())
                table.loc[i, symbol] = list(partition_dict.keys())
        if new_partition == partition:
            break
        partition = new_partition

    # Merge equivalent states
    new_states = [f'S{i}' for i in range(len(partition))]
    state_map = dict(sum([[(state, new_states[i]) for state in group] for i, group in enumerate(partition)], []))
    minimized_table = reachable_table.replace(state_map).replace({'Estados': state_map})
    
    return minimized_table
