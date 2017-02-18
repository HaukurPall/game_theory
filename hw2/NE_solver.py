import numpy as np
import sys

from numpy.linalg import LinAlgError


def find_pure_NE(p_1_utilities, p_2_utilities):
    """
    Compute pure Nash equilibria
    :param p_1_utilities: 2x2 matrix of utilities
    :param p_2_utilities: 2x2 matrix of utilities
    :return: list of strategies which are pure Nash equilibria
    """
    number_columns = p_1_utilities.shape[1]
    number_rows = p_1_utilities.shape[0]
    # for each player, we construct a matrix. If cell = 0 then that player does not want to change strategy, 1 otherwise
    # we start with all strategies as Nash equilibria
    p_1_nash = np.zeros((number_rows, number_columns))
    p_2_nash = np.zeros((number_rows, number_columns))
    for column in range(0, number_columns):
        for row in range(0, number_rows):
            comparison_column = column + 1
            if comparison_column >= number_columns:
                comparison_column -= 2

            # does column player want to change?
            if p_2_utilities[row][column] >= p_2_utilities[row][comparison_column]:
                # no
                pass
            else:
                # yes
                p_2_nash[row][column] = 1

            comparison_row = row + 1
            if comparison_row >= number_rows:
                comparison_row -= 2

            # does row player want to change?
            if p_1_utilities[row][column] >= p_1_utilities[comparison_row][column]:
                # no
                pass
            else:
                # yes
                p_1_nash[row][column] = 1
    # we add the matrices together, if a cell = 0 then it is a pure Nash eq.
    result = np.add(p_1_nash, p_2_nash)
    strategies = []
    for column in range(0, number_columns):
        for row in range(0, number_rows):
            if result[row][column] == 0.0:
                row_prob = np.zeros(number_rows)
                row_prob[row] = 1
                column_prob = np.zeros(number_columns)
                column_prob[column] = 1
                strategies.append((row_prob, column_prob))
    return strategies


def find_mixed_NE(p_1_utilities, p_2_utilities):
    """
    Compute mixed Nash equilibrium
    :param p_1_utilities: 2x2 matrix of utilities
    :param p_2_utilities: 2x2 matrix of utilities
    :return: Return a strategy which is a mixed Nash equilibrium
    """
    # now we solve the linear equation: ax=b
    # as we derived the coefficient a in report for ax=b
    p_1_a = np.array([[p_1_utilities[0][0] - p_1_utilities[0][1] - p_1_utilities[1][0] + p_1_utilities[1][1]]])
    p_2_a = np.array([[p_2_utilities[0][0] - p_2_utilities[1][0] - p_2_utilities[0][1] + p_2_utilities[1][1]]])

    # as we derived the constant b in report
    p_1_b = np.array([p_1_utilities[1][1] - p_1_utilities[0][1]])
    p_2_b = np.array([p_2_utilities[1][1] - p_2_utilities[1][0]])
    try:
        q = np.linalg.solve(p_1_a, p_1_b)
        p = np.linalg.solve(p_2_a, p_2_b)
    except LinAlgError:
        # we catch LinAlgError in case there is no inverse, for us this means that all strategies are mixed Nash eq.
        print("All strategies are solutions")
        return

    # array to tuple
    p = (p[0], 1 - p[0])
    q = (q[0], 1 - q[0])
    # if these are not probabilities, we throw the solution away
    if p[0] > 1.0001 or p[0] < 0.0001 or p[1] > 1.0001 or p[1] < 0.0001 or q[0] > 1.0001 or q[0] < 0.0001 or q[1] > 1.0001 or q[1] < 0.0001:
        return
    return p, q


def is_interval_contained(p_utility, p, q, epsilon=0.00001):
    """
    Is utility of player the same when p=p-epsilon?
    :param p_utility: 2x2 matrix of utilities
    :param p: probabilities of player 1
    :param q: probabilities of player 2
    :param epsilon: epsilon +-small number
    :return:
    """
    # if p_1 is either 0 or 1 and p_2 is not
    if (p[0] == 0.0 or p[0] == 1.0) and (q[0] != 0.0 and q[0] != 1.0):
        if utility_increases(p_utility, p, q, p, (q[0] + epsilon, q[1] - epsilon)):
            return True
        else:
            return False


def utility_increases(p_utility, p, q, p_new, q_new):
    start_utility = expected_utility(p_utility, p, q)
    new_utility = expected_utility(p_utility, p_new, q_new)
    return new_utility >= start_utility


def expected_utility(player_utilities, p_1_prob, p_2_prob):
    utility = 0
    for column in range(0, player_utilities.shape[1]):
        for row in range(0, player_utilities.shape[0]):
            # as per definition of expected utility: sum(util_p * prob_p1 * prob_p2)
            utility += player_utilities[row][column] * p_1_prob[row] * p_2_prob[column]
    return utility


def read_game(file_path):
    game = {}
    tmp = []
    with open(file_path, 'r') as file:
        for line in file:
            tmp.append(line)
    game["name"] = tmp[0]
    game["p1"] = np.array([[int(x) for x in tmp[1].split(",")], [int(x) for x in tmp[2].split(",")]])
    game["p2"] = np.array([[int(x) for x in tmp[3].split(",")], [int(x) for x in tmp[4].split(",")]])
    return game


def format_strategy(prob_1, prob_2, prob_3, prob_4):
    return "(({},{}),({},{}))".format(prob_1, prob_2, prob_3, prob_4)


def main():
    game = read_game(sys.argv[1])
    strategies = find_pure_NE(game["p1"], game["p2"])
    for strategy in strategies:
        print(format_strategy(strategy[0][0], strategy[0][1], strategy[1][0], strategy[1][1]))
    mixed_strategy = find_mixed_NE(game["p1"], game["p2"])
    if mixed_strategy is None:
        return
    print(format_strategy(mixed_strategy[0][0], mixed_strategy[0][1], mixed_strategy[1][0], mixed_strategy[1][1]))
    if is_interval_contained(game["p1"], mixed_strategy[0], mixed_strategy[1], +0.00001):
        print(format_strategy(mixed_strategy[0][0], mixed_strategy[0][1], str(mixed_strategy[1][0])+"+e",
                              str(mixed_strategy[1][1])+"-e"))
    if is_interval_contained(game["p1"], mixed_strategy[0], mixed_strategy[1], -0.00001):
        print(format_strategy(mixed_strategy[0][0], mixed_strategy[0][1], str(mixed_strategy[1][0])+"-e",
                              str(mixed_strategy[1][1])+"+e"))
    if is_interval_contained(game["p2"], mixed_strategy[1], mixed_strategy[0], +0.00001):
        print(format_strategy(str(mixed_strategy[0][0])+"+e", str(mixed_strategy[0][1])+"-e", mixed_strategy[1][0],
                              mixed_strategy[1][1]))
    if is_interval_contained(game["p2"], mixed_strategy[1], mixed_strategy[0], -0.00001):
        print(format_strategy(str(mixed_strategy[0][0])+"-e", str(mixed_strategy[0][1])+"+e", mixed_strategy[1][0],
                              mixed_strategy[1][1]))


if __name__ == "__main__":
    main()
