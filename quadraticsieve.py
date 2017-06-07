import math
from utils import *
from factoring_algorithm import FactoringAlgorithm
import numpy as np


class QuadraticSieveFactoringAlgorithm(FactoringAlgorithm):
    def _generate_base(self, n):
        base_len = 30
        base = []
        for prime in PRIMES:
            if len(base) == base_len:
                break
            if is_quadratic_residue(n, prime):
                base.append(prime)
        print len(base)
        return base

    def _generate_relations(self, n, base, num_relations):
        sieve_length = int(math.floor(math.sqrt(3 * n)))
        floor_sqrt_n = int(math.ceil(math.sqrt(n)))

        # Initialize Sieve to (X + ceil(sqrt(N)))^2 - N
        sieve = np.array([((i + floor_sqrt_n) ** 2) - n for i in xrange(sieve_length)])

        # Perform Sieve
        for prime in base:
            # Solve (X + ceil(sqrt(N)))^2 - N = 0 mod p
            N_mod_p = n % prime

            for i in xrange(prime):
                if (i ** 2) % prime == N_mod_p:
                    break

            # print (i - (floor_sqrt_n % prime)) % prime
            # print ((prime - i) - (floor_sqrt_n % prime)) % prime

            mask = np.arange(sieve_length) % prime
            mask_1 = mask == (i - (floor_sqrt_n % prime)) % prime
            mask_2 = mask == ((prime - i) - (floor_sqrt_n % prime)) % prime
            mask = np.logical_or(mask_1, mask_2)
            sieve = np.where(mask, sieve / prime, sieve)

            for i in xrange(sieve_length):
                if mask[i]:
                    while sieve[i] % prime == 0:
                        sieve[i] /= prime

        # If it's a 1 in sieve means it is smooth and (index + floor_sqrt_n)^2 = y^2 mod n
        candidates = np.where(sieve == 1)[0] + floor_sqrt_n

        relations = []
        for x in candidates:
            if len(relations) >= num_relations:
                break

            exponents = is_b_smooth((x ** 2) - n, base)

            if exponents:
                relations.append((x, exponents))

        print num_relations
        print len(relations)
        return relations


def main():
    factoring_algorithm = QuadraticSieveFactoringAlgorithm(1)
    # y = 237375311 * 10000223
    y = 102071 * 102077
    x = factoring_algorithm.factor(y)
    # y = 237375311 * 10000223 #102071 * 102077  #145379239
    print "%d can be factored to %d and %d" % (y, x, y / x)


if __name__ == '__main__':
    main()
