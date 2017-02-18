import numpy as np


def find_pure_NE(p_1, p_2):
    number_columns = p_1.shape[1]
    number_rows = p_1.shape[0]
    p_1_nash = np.zeros((number_rows, number_columns))
    p_2_nash = np.zeros((number_rows, number_columns))
    for column in range(0, number_columns):
        for row in range(0, number_rows):
            comparison_column = column + 1
            if comparison_column >= number_columns:
                comparison_column -= 2

            # does column player want to change?
            if p_2[row][column] >= p_2[row][comparison_column]:
                # no
                pass
            else:
                # yes
                p_2_nash[row][column] = 1

            comparison_row = row + 1
            if comparison_row >= number_rows:
                comparison_row -= 2

            # does row player want to change?
            if p_1[row][column] >= p_1[comparison_row][column]:
                # no
                pass
            else:
                # yes
                p_1_nash[row][column] = 1
    result = np.add(p_1_nash, p_2_nash)
    return result


def find_mixed_NE(p_1, p_2):
    epislon = 0.00001
    p_1_coefficients = np.array([[p_1[0][0] - p_1[0][1] - p_1[1][0] + p_1[1][1]]])
    p_2_coefficients = np.array([[p_2[0][0] - p_2[1][0] - p_2[0][1] + p_2[1][1]]])

    p_1_c = np.array([p_1[1][1] - p_1[0][1]])
    p_2_c = np.array([p_2[1][1] - p_2[1][0]])
    try:
        q = np.linalg.solve(p_1_coefficients, p_1_c)
        p = np.linalg.solve(p_2_coefficients, p_2_c)
    except:
        print("All combinations of strategies are solutions")
        return

    # array to number
    p_1_probabilities = (p[0], 1-p[0])
    p_2_probabilities = (q[0], 1-q[0])
    # if p_1 is either 0 or 1 and p_2 is not
    if (p_1_probabilities[0] == 0.0 or p_1_probabilities[0] == 1.0) and (p_2_probabilities[0] != 0.0 and p_2_probabilities[0] != 1.0):
        p_1_expc_utility = expected_utility(p_1, p_1_probabilities, p_2_probabilities)
        p_1_expc_util_adjust = expected_utility(p_1, p_1_probabilities, (p_2_probabilities[0]-epislon, p_2_probabilities[1]+epislon))
        if p_1_expc_utility <= p_1_expc_util_adjust:
            # q - epsilon is also a solution
            print("(({},{}),(q,1-q)) and everything below q={} is also a solution".format(p_1_probabilities[0], p_1_probabilities[1], p_2_probabilities[0]))
        p_1_expc_util_adjust = expected_utility(p_1, p_1_probabilities, (p_2_probabilities[0]+epislon, p_2_probabilities[1]-epislon))
        if p_1_expc_utility <= p_1_expc_util_adjust:
            # q - epsilon is also a solution
            print("(({},{}),(q,1-q)) and everything above q={} is also a solution".format(p_1_probabilities[0], p_1_probabilities[1], p_2_probabilities[0]))
    # if p_2 is either 0 or 1 and p_2 is not
    elif (p_2_probabilities[0] == 0.0 or p_2_probabilities[0] == 1.0) and (p_1_probabilities[0] != 0.0 and p_1_probabilities[0] != 1.0):
        p_2_expc_utility = expected_utility(p_2, p_1_probabilities, p_2_probabilities)
        p_2_expc_util_adjust = expected_utility(p_2, (p_1_probabilities[0]-epislon, p_1_probabilities[1]+epislon), p_2_probabilities)
        if p_2_expc_utility <= p_2_expc_util_adjust:
            # p - epsilon is also a solution
            print("((p,1-p),({},{})) and everything below p={} is also a solution".format(p_2_probabilities[0], p_2_probabilities[1], p_1_probabilities[0]))
        p_2_expc_util_adjust = expected_utility(p_2, (p_1_probabilities[0]+epislon, p_1_probabilities[1]-epislon), p_2_probabilities)
        if p_2_expc_utility <= p_2_expc_util_adjust:
            # p - epsilon is also a solution
            print("((p,1-p),({},{})) and everything above p={} is also a solution".format(p_2_probabilities[0], p_2_probabilities[1], p_1_probabilities[0]))
    else:
        print("(({},{}),({},{})) are mixed equilibria".format(p_1_probabilities[0], p_1_probabilities[1], p_2_probabilities[0], p_2_probabilities[1]))

    return (p_1_probabilities, p_2_probabilities)


def expected_utility(player_utilities, p_1_prob, p_2_prob):
    utility = 0
    for column in range(0, player_utilities.shape[1]):
        for row in range(0, player_utilities.shape[0]):
            utility += player_utilities[row][column]*p_1_prob[row]*p_2_prob[column]
    return utility

def a_1():
    import math
    for n in range(1, 201):
        sum = 0
        for k in range(0, 200-n):
            sum += math.sqrt(k)
        p = 10*n + sum
        print("n={}: {}".format(n,p))

def main():
    # Prisoner's dilemma
    #p_1 = np.array([[-10, -25],[0, -20]])
    #p_2 = np.array([[-10, 0],[-25, -20]])
    # single mix nash
    #p_1 = np.array([[1, 0],[0, 1]])
    #p_2 = np.array([[1, 0],[0, 1]])
    # many mixed nash eq
    #p_1 = np.array([[2, 5],[5, 3]])
    #p_2 = np.array([[3, 3],[4, 3]])
    # all strategies are nash
    p_1 = np.array([[0, 0],[0, 0]])
    p_2 = np.array([[0, 0],[0, 0]])
    p_1 = np.array([[2, 2],[2, 2]])
    p_2 = np.array([[2, 2],[2, 2]])
    result = find_pure_NE(p_1, p_2)
    for column in range(0, result.shape[1]):
        for row in range(0, result.shape[0]):
            if result[row][column] == 0.0:
                row_prob = np.zeros(2)
                row_prob[row] = 1
                column_prob = np.zeros(2)
                column_prob[column] = 1
                print("(({},{}),({},{})) is a pure Nash eq.".format(row_prob[0], row_prob[1], column_prob[0], column_prob[1]))
    result = find_mixed_NE(p_1, p_2)


if __name__ == "__main__":
    main()


