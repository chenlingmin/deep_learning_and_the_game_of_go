import numpy as np

counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
for i in range(100):
    choice = np.random.choice(
        [1, 2, 3, 4, 5],
        p=[0.2, 0.2, 0.2, 0.2, 0.2]
    )
    counts[choice] += 1
print(counts)


def simulate_game(policy):
    player_1_choices = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    player_1_total = 0
    player_2_choices = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    player_2_total = 0

    for i in range(100):
        player_1_choice = np.random.choice([1, 2, 3, 4, 5], p=policy)
        player_1_choices[player_1_choice] += 1
        player_1_total += player_1_choice
        player_2_choice = np.random.choice([1, 2, 3, 4, 5], p=policy)
        player_2_choices[player_2_choice] += 1
        player_2_total += player_2_choice

    if player_1_total > player_2_total:
        winner_choices = player_1_choices
        loser_choices = player_2_choices
    else:
        winner_choices = player_2_choices
        loser_choices = player_1_choices
    return (winner_choices, loser_choices)


# policy = [0.2, 0.2, 0.2, 0.2, 0.2]
# print(simulate_game(policy))
# print(simulate_game(policy))
# print(simulate_game(policy))
# print(simulate_game(policy))
# print(simulate_game(policy))

def normalize(policy):
    policy = np.clip(policy, 0, 1)
    return policy / np.sum(policy)

num_games = 200

choices = [1, 2, 3, 4, 5]
policy = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
learning_rate = 0.001
for i in range(num_games):
    win_counts, lose_counts = simulate_game(policy)
    for j, choice in enumerate(choices):
        net_wins = win_counts[choice] - lose_counts[choice]
        policy[j] += learning_rate * net_wins
    policy = normalize(policy)
    print('%d: %s' % (i, policy))
