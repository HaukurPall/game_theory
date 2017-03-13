import random, math

random.seed(673567)  # we set the seed for debugging


class VCG:
    def __init__(self, N, G):
        self.N = N
        self.G = [x for x in range(1, G + 1)]  # goods are lablelled 1, 2, ... G
        self.valuations = []
        self.bundles = []
        self.best_allocation = None

    def generate_random_valuations(self):
        self.valuations = [random.randint(1, len(self.G)) for x in range(0, self.N)]

    def generate_bundles(self):
        """
        Generate disjoint bundles for players
        """
        permutations = int(math.pow(self.N, len(self.G)))
        self.bundles = [self.G[x] for x in range(0, self.N)]

    def __str__(self):
        return "N: {}\n" \
               "G: {}\n" \
               "v: {}\n" \
               "bundles: {}".format(self.N, self.G, self.valuations, self.bundles)

    def naive_allocation(self):
        permutations = int(math.pow(2, self.N))
        best_allocation = -1.0
        best_allocation_representation = None
        for x in range(0, permutations):
            allocation_representation = "{0:b}".format(x).rjust(self.N, '0')
            allocation_outcome = self.compute_outcome(allocation_representation)
            if allocation_outcome > best_allocation:
                best_allocation = allocation_outcome
                best_allocation_representation = allocation_representation
        return best_allocation_representation, best_allocation

    def is_legal_allocation(self, binary_representation):


    def compute_outcome(self, binary_representation):
        """
        Compute social welfare outcome of allocation
        :param binary_representation: the binary representation of bundle allocation, f.ex. "001010"
        :return: The social welfare outcome of allocation
        """
        sum = 0.0
        # we flip the binary representation for this loop
        for index, character in enumerate(binary_representation[::-1]):
            if character == '1':
                sum += self.valuations[index]
        return sum


def main():
    auction = VCG(3, 4)
    auction.generate_random_valuations()
    auction.generate_bundles()
    alloc_rep, value = auction.naive_allocation()
    print(auction)
    print("Best SW: {}".format(value))
    print("with allocation: {}".format(alloc_rep))


if __name__ == "__main__":
    main()
