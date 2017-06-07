import fractions
import numpy as np
import sympy


class FactoringAlgorithm():
    def __init__(self, verbose):
        self._verbose = verbose

    def factor(self, n):
        """
            Returns a non trivial factor of n. Assumes n is composite

            Args:
                n: int number to factor

            Returns:
                a: int a non trivial factor of n
        """

        # Generate Base
        base = self._generate_base(n)

        # Generate relations
        relations = self._generate_relations(n, base, len(base) + 1)

        # Find congruence of squares a^2 b^2 using relations
        congruence = self._find_congruence(n, relations, base)

        # If congruence is None then no factors were found
        if congruence is None:
            return None

        a, b = congruence


        # Use a,b to find non trivial using gcd
        return fractions.gcd(a + b, n)

    def _get_linear_independent_indexes(self, exponent_vectors):
        """
            Returns list of rows of exponent vectors
            that are linearly independent from each other

            i.e. returns the indexes of the row space of the matrix

            Args:
                exponent_vectors: [[int]]

            Returns:
                [int] indexes of linearly independent rows
        """
        rref = sympy.Matrix(np.array(exponent_vectors).T).rref()
        print rref
        rref = rref[0].tolist()


        linearly_independent_indexes = []
        for row in rref:
            for j in xrange(len(row)):
                if row[j] == 1:
                    linearly_independent_indexes.append(j)
                    break

        print linearly_independent_indexes
        return linearly_independent_indexes

    def _find_congruence(self, n, relations, base):
        """
            Given relations finds a congruence of squares
        """
        x, exponent_vectors = zip(*relations)
        exponent_vectors = list(exponent_vectors)
        exponent_vectors = np.array(exponent_vectors)
        exponent_vectors = exponent_vectors % 2

        linearly_indpendent_indexes = self._get_linear_independent_indexes(exponent_vectors)
        linearly_dependent_indexes = [i for i in xrange(len(relations)) if i not in linearly_indpendent_indexes]

        # Fill in to make it square
        exponent_vectors = np.array(exponent_vectors)
        independent = np.concatenate((exponent_vectors[linearly_indpendent_indexes], np.zeros((len(base) - len(linearly_indpendent_indexes), len(base)))), axis=0)

        # Get linearly dependent vector
        for linearly_dependent_index in linearly_dependent_indexes:
            linearly_dependent_index = -1
            dependent = exponent_vectors[linearly_dependent_index]

            # Solve
            solution = np.linalg.lstsq(independent.T, dependent)[0]
            solution = solution[:len(linearly_indpendent_indexes)]

            # Extract a and b
            a = 1L
            a *= relations[linearly_dependent_index][0]
            exp = np.array(relations[linearly_dependent_index][1])

            for idx, sol in zip(linearly_indpendent_indexes, solution):
                sol = int(round(abs(sol))) % 2

                if sol > 0:

                    a *= relations[idx][0] * sol
                    exp += np.array(relations[idx][1]) * sol
            b = 1L
            for p, e in zip(base, exp):
                b *= (p ** (e / 2))


            # Check not n
            if not (a % n == (b % n)) or (a % n == (-b % n)):
                return (a, b)
            else:
                print "trying another dependent"

        print "No factors found."
        return None
