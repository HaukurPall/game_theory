import random, math

#random.seed(673569)  # we set the seed for debugging


class VCG:
    def __init__(self, N, G):
        self.N = N
        self.G = [x for x in range(1, G + 1)]  # goods are lablelled 1, 2, ... G
        self.valuations = []
        self.bundles = [set() for x in range(0, N)]

    def reset(self):
        self.generate_bundles()
        self.generate_random_valuations()

    def generate_random_valuations(self):
        self.valuations = [random.randint(1, len(self.G)) for x in range(0, self.N)]

    def generate_bundles(self):
        """
        Generate random, disjoint bundles out of G for all N players
        """
        # we add one dummy player as "resource not with any player", he is player 0
        permutations = int(math.pow(self.N + 1, len(self.G)))
        number_of_set_to_use = random.randint(0, permutations - 1)
        set_representation = k_nary(n=number_of_set_to_use, k=self.N + 1, length=len(self.G))
        for index, number in enumerate(set_representation):
            # since now the indices are from 0 to N, we want 0 to N-1
            number -= 1
            if number == -1:
                continue
            self.bundles[number].add(self.G[index])

    def __str__(self):
        return "N: {}\n" \
               "G: {}\n" \
               "v: {}\n" \
               "bundles: {}".format(self.N, self.G, self.valuations, self.bundles)

    def get_valuation_of_player(self, index):
        return self.valuations[index]

    def set_valuation_of_player(self, index, value):
        self.valuations[index] = value

    def naive_allocation(self):
        # the number of bundle allocations possible
        permutations = int(math.pow(2, self.N))
        best_allocation = -1.0
        best_allocation_representation = None
        for x in range(0, permutations):
            allocation_representation = k_nary(n=x, k=2, length=self.N)
            # we check if allocation is legal
            if not self.is_legal_allocation(allocation_representation):
                continue
            allocation_outcome = self.compute_outcome(allocation_representation)
            if allocation_outcome > best_allocation:
                best_allocation = allocation_outcome
                best_allocation_representation = allocation_representation
        return best_allocation_representation

    def is_legal_allocation(self, binary_representation):
        bundle_unions = set()
        for index, bundle_included in enumerate(binary_representation):
            if bundle_included == 1:
                # the intersection always needs to be empty
                intersection = bundle_unions.intersection(self.bundles[index])
                if len(intersection) != 0:
                    return False
                bundle_unions.update(self.bundles[index])
        return True

    def compute_outcome(self, binary_representation, skip=None):
        """
        Compute social welfare outcome of allocation
        :param skip: An index of a player to be skipped in computation
        :param binary_representation: the binary representation of bundle allocation, f.ex. "001010"
        :return: The social welfare outcome of allocation
        """
        sum = 0.0
        # we flip the binary representation for this loop
        for index, bundle_included in enumerate(binary_representation):
            # we sometimes skip a player
            if bundle_included == 1 and skip != index:
                sum += self.valuations[index]
        return sum

    def compute_price(self, binary_representation):
        prices = []
        for index, bundle_included in enumerate(binary_representation):
            # first we compute the SW of all players but player_i under this allocation
            sw_of_all_but_i = self.compute_outcome(binary_representation, skip=index)
            # we set player_i valuation to 0 - but keep the old in temp storage
            old_valuation = self.get_valuation_of_player(index)
            self.set_valuation_of_player(index, 0)
            allocation_without_i = self.naive_allocation()
            sw_without_i_at_all = self.compute_outcome(allocation_without_i, skip=index)
            # and we set the old valuation again
            self.set_valuation_of_player(index, old_valuation)
            prices.append(sw_without_i_at_all - sw_of_all_but_i)

        return prices


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
    auction = VCG(3, 4)
    auction.reset()
    alloc_rep = auction.naive_allocation()
    value = auction.compute_outcome(alloc_rep)
    prices = auction.compute_price(alloc_rep)
    print(auction)
    print("Best SW: {}".format(value))
    print("with allocation: {}".format(alloc_rep))
    print("prices: {}".format(prices))


if __name__ == "__main__":
    main()
