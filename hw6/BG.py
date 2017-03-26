import random, math, sys


class BG:
    def __init__(self, debt, estate):
        self.debt = debt
        self.estate = estate
        self.N = len(debt)
        self.valuations = []
        self.representations = []
        # we skip the empty coalition and the full because the complaint is always 0
        for x in range(1, int(math.pow(2, self.N) - 1)):
            debt_allocation_representation = k_nary(n=x, k=2, length=self.N)
            self.representations.append(debt_allocation_representation)
        self.compute_v()

    def compute_v(self):
        for coalition_representation in self.representations:
            debt_sum = 0.0
            for index, debt in enumerate(coalition_representation):
                if debt == 0:
                    debt_sum += self.debt[index]
            self.valuations.append(max(0, self.estate - debt_sum))

    def compute_complaints(self, imputation):
        complaints = []
        for coalition_index, coalition_representation in enumerate(self.representations):
            sum_imputations_in_coalition = 0.0
            for debt_index, debt in enumerate(coalition_representation):
                if debt == 1:
                    sum_imputations_in_coalition += imputation[debt_index]
            complaints.append(self.valuations[coalition_index] - sum_imputations_in_coalition)
        print(complaints)
        return complaints

    def look_ahead(self, imputations, complaints, adjustment_value):
        high_complaints = [i for i, x in enumerate(complaints) if x >= max(complaints) - adjustment_value]
        high_coalitions = [self.representations[i] for i in high_complaints]
        high_players = []
        for coalition in high_coalitions:
            for player_index, player_included in enumerate(coalition):
                if player_included == 1:
                    high_players.append(player_index)
        player_to_steal_from = -1
        for x in range(0, self.N):
            if x not in high_players:
                player_to_steal_from = x
                break
        if player_to_steal_from == -1:
            return imputations

        # now we are only interested in a single high coalition
        highest_coaltion = self.representations[complaints.index(max(complaints))]
        player_to_give_to = -1
        # we just grab a player from there
        for player_index, player_included in enumerate(highest_coaltion):
            if player_included == 1:
                player_to_give_to = player_index
        new_imputations = imputations.copy()
        new_imputations[player_to_steal_from] -= adjustment_value
        new_imputations[player_to_give_to] += adjustment_value
        return new_imputations


def k_nary(n, k, length, numbers=None):
    """
    Convert number to k-nary representation
    :param k: The base to convert to
    :param n: The number to convert
    :param length: The length of list to be returned. We pad with 0
    :return: A list of integers in k-nary representing n
    """
    if not numbers:
        numbers = []
    e = n // k
    q = n % k
    numbers.append(q)
    if e == 0:
        # we pad with 0
        while len(numbers) < length:
            numbers.append(0)
        # we reverse the list so we end up with:
        # 0 0 0 1  for k_nary(n=1, k=2, length=4)
        return numbers[::-1]
    else:
        return k_nary(n=e, k=k, length=length, numbers=numbers)


def main():
    bg = BG([30, 30, 30], 89)
    end_imputation = [89, 0, 0]
    end_imputation = use_look_ahead(bg, end_imputation, 0.5)
    print(end_imputation)


def use_look_ahead(bg, imputation, adjustment_value):
    complaints = bg.compute_complaints(imputation)
    new_imputation = bg.look_ahead(imputation, complaints, adjustment_value)
    while new_imputation != imputation:
        imputation = new_imputation
        complaints = bg.compute_complaints(imputation)
        new_imputation = bg.look_ahead(imputation, complaints, adjustment_value)
    return imputation


if __name__ == "__main__":
    main()
