import collections, math
import numpy as np
import hw2.NE_solver as hw2
import matplotlib.pyplot as plt


def best_response(our_utility, opponent_mixed_strategy):
    if hw2.utility_increases(our_utility, (1.0, 0), opponent_mixed_strategy, (0.0, 1.0), opponent_mixed_strategy):
        # tie breaker is implied in "utility_increases" to be (1,0)
        return (0, 1)
    else:
        return (1, 0)


def play_strategy(p_1_a, p_2_a, history):
    if p_1_a[0] == 1:
        history["p1"].update("1")
    else:
        history["p1"].update("2")
    if p_2_a[0] == 1:
        history["p2"].update("1")
    else:
        history["p2"].update("2")


def distance_between(last_emperical_mixed_strategies, emperical_mixed_strategies):
    '''
    Compute distance between last strategy and current one
    :param last_emperical_mixed_strategies: ((p, 1-p),(q, 1-q))
    :param emperical_mixed_strategies: ((p, 1-p),(q, 1-q))
    :return:
    '''
    distance_for_p_1 = math.fabs(last_emperical_mixed_strategies[0][0] - emperical_mixed_strategies[0][0])
    distance_for_p_2 = math.fabs(last_emperical_mixed_strategies[1][0] - emperical_mixed_strategies[1][0])
    return distance_for_p_1, distance_for_p_2


def fictious_game_play(game, epsilon):
    history = {"p1": collections.Counter(), "p2": collections.Counter()}
    p_1_a = (1, 0)
    p_2_a = (1, 0)
    play_strategy(p_1_a, p_2_a, history)
    converged = False
    last_emperical_mixed_strategies = None
    steps = 1
    while not converged:
        total_actions = history["p1"]["1"] + history["p1"]["2"]
        emperical_mixed_strategies = ((history["p1"]["1"] / total_actions, history["p1"]["2"] / total_actions),
                                      (history["p2"]["1"] / total_actions, history["p2"]["2"] / total_actions)
                                      )
        if last_emperical_mixed_strategies is None:
            distance = (100, 100)
        else:
            distance = distance_between(last_emperical_mixed_strategies, emperical_mixed_strategies)

        if distance[0] > epsilon or distance[1] > epsilon:
            converged = False
            p_1_a = best_response(game["p1"], emperical_mixed_strategies[1])
            p_2_a = best_response(game["p2"], emperical_mixed_strategies[0])
            play_strategy(p_1_a, p_2_a, history)
            steps += 1
            last_emperical_mixed_strategies = emperical_mixed_strategies
        else:
            converged = True

    return steps


def print_strategy(emperical_mixed_strategies):
    print("emp_str: (({},{}),({},{}))".format(emperical_mixed_strategies[0][0], emperical_mixed_strategies[0][1],
                                              emperical_mixed_strategies[1][0], emperical_mixed_strategies[1][1]))


def binary_rep_mapping(index):
    if index == 0:
        return (1,1)
    elif index == 1:
        return (0,1)
    elif index == 2:
        return (1,0)
    else:
        return (0,0)


def generate_utility(dimension, binary_representation, multiplier):
    utilities = np.zeros(dimension)
    number_to_use = 1.0
    if binary_representation[0] == '1':
        number_to_use = -1.0
    number_to_use *= multiplier
    for index, representation in enumerate(binary_representation[1:]):
        if representation == '1':
            mapping = binary_rep_mapping(index)
            utilities[mapping[0]][mapping[1]] = number_to_use
    return utilities


def generate_zero_sum_game(utility):
    p_2_utilities = np.zeros(utility.shape)
    for column in range(0, utility.shape[1]):
        for row in range(0, utility.shape[0]):
            p_2_utilities[row][column] = -utility[row][column]
    return p_2_utilities


def generate_all_zero_sum_games(multiplier):
    games = []
    for x in range(0, int(math.pow(2,5))):
        p_1 = generate_utility((2,2), "{0:05b}".format(x), multiplier)
        p_2 = generate_zero_sum_game(p_1)
        game = {"p1": p_1, "p2": p_2}
        games.append(game)
    return games


def print_game(game):
    print(game["p1"])
    print(game["p2"])


def plot_line_graph(x, y, y_name, x_name):
    plt.plot(x, y)
    plt.ylabel(y_name)
    plt.xlabel(x_name)
    plt.xscale('log')
    plt.savefig(x_name+y_name+'.png')
    plt.clf()


def plot_bar_graph(x, y, name):
    width = 1/2.0
    plt.bar(x, y, width, color="blue")
    plt.ylabel(name)
    plt.xlabel('#game')
    plt.savefig(name+'.png')
    plt.clf()


def run_all_games(games, epsilon):
    steps = []
    for game in games:
        game_steps = fictious_game_play(game, epsilon)
        steps.append(game_steps)
    return steps


def find_pure_nash(games):
    missing_ne = []
    for game in games:
        strategies = hw2.find_pure_NE(game["p1"], game["p2"])
        if strategies:
            missing_ne.append(False)
        else:
            missing_ne.append(True)
    return missing_ne

def main():
    games = generate_all_zero_sum_games(3)
    x = [y+1 for y, item in enumerate(games)]
    pure_nash_markers = find_pure_nash(games)
    plot_bar_graph(x, pure_nash_markers, 'pure nash')

    worst_runs = []
    epsilons = [math.pow(10, -x) for x in range(1, 6)]
    for epsilon in epsilons:
        steps = run_all_games(games, epsilon)
        plot_bar_graph(x, steps, 'steps-'+str(epsilon))
        worst_runs.append(max(steps))
    print(worst_runs)
    plot_line_graph(epsilons, worst_runs, "steps", "epsilon")


if __name__ == "__main__":
    main()
