import random, math, sys

class BG:

    def __init__(self, debt, estate):
        self.debt = debt
        self.estate= estate
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

    def adjust_imputation(self, imputations, complaints, adjustment_value):
        # get all highest values
        highest_complaint = complaints.index(max(complaints))
        lowest_complaints = [i for i, x in enumerate(complaints) if x == min(complaints)]
        highest_coalition = self.representations[highest_complaint]
        lowest_coalitions = [self.representations[i] for i in lowest_complaints]

        # we only consider coalitions in which actually lower the highest complaint
        valid_lowest_coalitions = []
        for coalition in lowest_coalitions:
            for index, player in enumerate(coalition):
                if highest_coalition[index] == 0 and player == 1:
                    lowest_coalition = coalition
                    break

        average_highest_complaint = []
        for index_of_highest_coalition_player, player in enumerate(highest_coalition):
            sum_complaints = 0.0
            if player == 1:
                for coalition_index, coalition in enumerate(self.representations):
                    if coalition[index_of_highest_coalition_player] == 1:
                        sum_complaints += complaints[coalition_index]
                average_highest_complaint.append((index_of_highest_coalition_player, sum_complaints/ int(math.pow(2, self.N - 1))))

        average_lowest_complaint = []
        for index_of_lowest_coalition_player, player in enumerate(lowest_coalition):
            sum_complaints = 0.0
            if player == 1:
                for coalition_index, coalition in enumerate(self.representations):
                    if coalition[index_of_lowest_coalition_player] == 1:
                        sum_complaints += complaints[coalition_index]
                average_lowest_complaint.append((index_of_lowest_coalition_player, sum_complaints/ int(math.pow(2, self.N - 1))))


        give_to_player_index, give_value = min(average_highest_complaint, key = lambda t: t[1])
        steal_from_player_index, steal_value = min(average_lowest_complaint, key = lambda t: t[1])

        while highest_coalition[steal_from_player_index] == 1:
            average_lowest_complaint.pop(average_lowest_complaint.index((steal_from_player_index, steal_value)))
            steal_from_player_index, value = min(average_lowest_complaint, key = lambda t: t[1])

        #if give_to_player_index == steal_from_player_index:
        #    if len(average_lowest_complaint) != 1:
        #        average_lowest_complaint.pop(average_lowest_complaint.index((steal_from_player_index, steal_value)))
        #        steal_from_player_index, value = min(average_lowest_complaint, key = lambda t: t[1])
        #    else:
        #        average_highest_complaint.pop(average_highest_complaint.index((give_to_player_index, give_value)))
        #        give_to_player_index, value = min(average_highest_complaint, key = lambda t: t[1])
        #        adjustment_value /= 2.0

        imputations[steal_from_player_index] -= adjustment_value
        imputations[give_to_player_index] += adjustment_value
        return imputations


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
    bg = BG([10, 20, 30], 36)
    end_imputation = [10, 10, 16]
    end_imputation = find_imputation(bg, end_imputation)
    print(end_imputation)


def find_imputation(bg, end_imputation):
    imputation = end_imputation.copy()
    old_complaints = bg.compute_complaints(imputation)
    new_complaints = old_complaints.copy()
    while max(new_complaints) <= max(old_complaints):
        end_imputation = imputation.copy()
        old_complaints = new_complaints.copy()
        new_imputation = bg.adjust_imputation(imputation, old_complaints, adjustment_value=1)
        new_complaints = bg.compute_complaints(new_imputation)
        imputation = new_imputation.copy()
    return end_imputation


if __name__ == "__main__":
    main()