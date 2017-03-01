# Authors: Greg and Haukur
# Date: 25th of February
import collections, math
import numpy as np
import hw2.NE_solver as hw2
import matplotlib.pyplot as plt


def best_pure_response(our_utility, opponent_mixed_strategy):
    """
    Compute best pure response for player
    :param our_utility: utility matrix for player
    :param opponent_mixed_strategy: the opponent mixed strategy
    :return:
    """
    # if the utility increases by using mixed strategy (0.0, 1.0) rather than  (1.0, 0)
    if hw2.utility_increases(our_utility, (1.0, 0), opponent_mixed_strategy, (0.0, 1.0), opponent_mixed_strategy):
        # we use (0.0, 1.0)
        return (0, 1)
    else:
        return (1, 0)


def store_actions(p_1_a, p_2_a, history):
    """
    Store actions done by players
    :param p_1_a: p1 action
    :param p_2_a: p2 action
    :param history: previous history
    """
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
    :param last_emperical_mixed_strategies: ((p_old, 1-p_old),(q_old, 1-q_old))
    :param emperical_mixed_strategies: ((p, 1-p),(q, 1-q))
    :return: (a,b) where a is distance for p and b distance for q
    '''
    distance_for_p_1 = math.fabs(last_emperical_mixed_strategies[0][0] - emperical_mixed_strategies[0][0])
    distance_for_p_2 = math.fabs(last_emperical_mixed_strategies[1][0] - emperical_mixed_strategies[1][0])
    return distance_for_p_1, distance_for_p_2


def fictitious_game_play(game, epsilon):
    """
    Play a fictitious game until convergence
    :param game: The game to play
    :param epsilon: parameter used to decide convergence within epsilon
    :return: The number of steps taken to solve
    """
    history = {"p1": collections.Counter(), "p2": collections.Counter()}
    p_1_a = (1, 0)
    p_2_a = (1, 0)
    store_actions(p_1_a, p_2_a, history)
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
            p_1_a = best_pure_response(game["p1"], emperical_mixed_strategies[1])
            p_2_a = best_pure_response(game["p2"], emperical_mixed_strategies[0])
            store_actions(p_1_a, p_2_a, history)
            steps += 1
            last_emperical_mixed_strategies = emperical_mixed_strategies
        else:
            converged = True

    return steps


def map_to_strategy_profile(index):
    """
    Map from index to pure action profile
    :param index: the index
    :return: the action profile
    """
    if index == 0:
        return (1, 1)
    elif index == 1:
        return (0, 1)
    elif index == 2:
        return (1, 0)
    else:
        return (0, 0)


def ternary(n):
    """
    Convert number to ternary representation
    :param n: The number to convert
    :return: A ternary representation of the number
    """
    e = n // 3
    q = n % 3
    if e == 0:
        return str(q)
    else:
        return ternary(e) + str(q)


def generate_utility(ternary_represenation, multiplier=1):
    """
    Generate utility matrix for player given a representation
    :param ternary_represenation: the representation
    :param multiplier: a multiplier for utility
    :return:
    """
    utilities = np.zeros((int(len(ternary_represenation) / 2), int(len(ternary_represenation) / 2)))
    for index, representation in enumerate(ternary_represenation):
        # mapping from index in representation to a strategy profile
        strategy_profile = map_to_strategy_profile(index)
        if representation == '0':
            number_to_use = 0.0
        elif representation == '1':
            number_to_use = multiplier * 1.0
        # we assume other cases are '2'
        else:
            number_to_use = multiplier * -1.0
        utilities[strategy_profile[0]][strategy_profile[1]] = number_to_use
    return utilities


def generate_zero_sum_game(utility):
    """
    Generate player zero sum utility matrix
    :param utility: the opposing player matrix, p_1
    :return: a utility matrix s.t. p_1 + p_2 = 0
    """
    p_2_utilities = np.zeros(utility.shape)
    for column in range(0, utility.shape[1]):
        for row in range(0, utility.shape[0]):
            p_2_utilities[row][column] = -utility[row][column]
    return p_2_utilities


def generate_zero_sum_games(multiplier):
    """
    Generate zero sum games
    :param multiplier: a multiplier for utility
    :return: a list of zero sum games
    """
    games = []
    for x in range(0, int(math.pow(3, 4))):
        p_1 = generate_utility(ternary(x).rjust(4, '0'), multiplier)
        p_2 = generate_zero_sum_game(p_1)
        game = {"p1": p_1, "p2": p_2}
        games.append(game)
    return games


def print_strategy(emperical_mixed_strategies):
    """
    Helper function
    """
    print("emp_str: (({},{}),({},{}))".format(emperical_mixed_strategies[0][0], emperical_mixed_strategies[0][1],
                                              emperical_mixed_strategies[1][0], emperical_mixed_strategies[1][1]))


def print_game(game):
    """
    Helper function
    """
    print(game["p1"])
    print(game["p2"])


def plot_line_graph(x, y, y_name, x_name):
    """
    Helper function
    """
    plt.plot(x, y)
    plt.ylabel(y_name)
    plt.xlabel(x_name)
    plt.xscale('log')
    plt.savefig(x_name + y_name + '.png')
    plt.clf()


def plot_bar_graph(x, y, name):
    """
    Helper function
    """
    width = 1 / 2.0
    plt.bar(x, y, width, color="blue")
    plt.ylabel(name)
    plt.xlabel('#game')
    plt.savefig(name + '.png')
    plt.clf()


def run_all_games(games, epsilon):
    """
    Run all games with a given epsilon and return the steps
    :param games: The fictious games to be played
    :param epsilon: The epsilon to be used
    :return: The steps it took to run each game
    """
    steps = []
    for game in games:
        game_steps = fictitious_game_play(game, epsilon)
        steps.append(game_steps)
    return steps


def has_dominant_strategy(utilities):
    """
    Check if row player has a dominant strategy (strict, weak, very weak)
    :param utilities: row player utilities
    :return: True if row player has a dominant strategy
    """
    # we assume row player is playing
    # lots of cases seems to be the quickest way to go
    if utilities[0][0] >= utilities[1][0] and utilities[0][1] >= utilities[1][1]:
        return True
    if utilities[1][0] >= utilities[0][0] and utilities[1][1] >= utilities[0][1]:
        return True
    return False


def is_there_no_dominant_strategy(game, index):
    """
    Returns true if a game has a dominant strategy (strict, weak, very weak)
    :param game: The game
    :param index: help number, to print number of game
    :return: True if game has a dominant strategy
    """
    #print("Game number: {}".format(index + 1))
    #print_game(game)
    if not has_dominant_strategy(game["p1"]):
        return True
    # we transpose to treat colin as rowena
    if not has_dominant_strategy(game["p2"].T):
        return True
    return False


def main():
    games = generate_zero_sum_games(3)
    # for graphs
    x = [y + 1 for y, item in enumerate(games)]
    dominant_players = [is_there_no_dominant_strategy(game, index) for index, game in enumerate(games)]
    plot_bar_graph(x, dominant_players, 'missing dominant strategy')

    worst_runs = []
    # we run all games with a few different epsilons
    epsilons = [math.pow(10, -x) for x in range(1, 6)]
    for epsilon in epsilons:
        steps = run_all_games(games, epsilon)
        plot_bar_graph(x, steps, 'steps-' + str(epsilon))
        worst_runs.append(max(steps))
    plot_line_graph(epsilons, worst_runs, "steps", "epsilon")


if __name__ == "__main__":
    main()
