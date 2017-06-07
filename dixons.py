import math
from utils import *
from factoring_algorithm import FactoringAlgorithm


class DixonsFactoringAlgorithm(FactoringAlgorithm):
    def _generate_relations(self, n, base, num_relations):
        """
            Generates NUM_RELATIONS relations of the form
            (x, [e1, e2, ... ]) such that

            x^2 = b1^e1 * b2^e2 ... (mod n) for each base bi and exponent ei

            Such a relation is called "b-smooth"

            Constructed using repeated trial division

            Args:
                n: int number we are factoring
                base: [int] prime factor base
                num_relations: int number of relations to generate

            Returns:
                relations: [(int, [int])] list of tuples each with an int
                            and exponent list that determines a relation
        """
        relations = []
        floor_sqrt_n = int(math.ceil(math.sqrt(n)))

        for x in xrange(floor_sqrt_n, n):
            if len(relations) >= num_relations:
                break

            exponents = is_b_smooth((x ** 2) % n, base)

            if exponents:
                relations.append((x, exponents))

        return relations

    def _generate_base(self, n):
        """
            Generates a factor base of prime numbers with the maximum prime
            having value less than _initialize_bound(n)

            Args:
                n: int the number we are factoring

            Returns:
                base: [int] prime factor base
        """

        bound = self._initialize_bound(n)

        base = []
        for prime in PRIMES:
            if prime > bound:
                break
            base.append(prime)

        return base

    def _initialize_bound(self, n):
        """
            Returns the optimal bound for n which is

            exp(sqrt(log n * log log n * c))

            For some c less than 1. Here we arbitrarily choose 1/2

            Args:
                n: int we are factoring

            Returns:
                bound: int optimal factor base bound for factoring n
        """
        bound = math.floor(math.exp(math.sqrt(math.log(n) * math.log(math.log(n))) / 2))
        return int(bound)


def main():
    import random
    factoring_algorithm = DixonsFactoringAlgorithm(1)
    a = random.choice(LARGER_PRIMES)
    b = random.choice(LARGER_PRIMES)
    print a, b
    y = a * b
    y = 4099 * 4111
    #102071 * 102077 #237375311 * 10000223
    x = factoring_algorithm.factor(y)
    print "%d can be factored to %d and %d" % (y, x, y / x)


if __name__ == '__main__':
    main()
