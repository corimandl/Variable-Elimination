"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Class for the implementation of the variable elimination algorithm.

"""
from factor import Factor
import logging

class VariableElimination:

    def __init__(self, network):
        """
        Initialize the variable elimination algorithm with the specified network.
        Add more initializations if necessary.

        """
        self.network = network

    def run(self, query, observed, elim_order):
        """
        Use the variable elimination algorithm to find out the probability
        distribution of the query variable given the observed variables

        Input:
            query:      The query variable
            observed:   A dictionary of the observed variables {variable: value}
            elim_order: Either a list specifying the elimination ordering
                        or a function that will determine an elimination ordering
                        given the network during the run

        Output: A variable holding the probability distribution
                for the query variable

        """
        # remove observed and query variables from elim
        elim_order = [i for i in elim_order if i not in observed.keys() and i != query]

        # construct a list of factors, one for each node in the network, reduce out the evidence variables
        factors = [Factor(p).reduce(observed) for p in self.network.probabilities.values()]
        # remove empty factor(s)
        factors = [f for f in factors if f.get_variables()]

        for var in elim_order:
            # gather all factors with var and remove them from the factors list
            factors_with_var = [f for f in factors if f.contains(var)]
            factors = [f for f in factors if f not in factors_with_var]
            # multiply factors_with_var together and then sum out var
            f = Factor.multiply_list(factors_with_var).sum_out(var)
            if f: factors.append(f)

        # multiply final factors, which just have the query variable, and normalize.
        final = Factor.multiply_list(factors)
        final.normalize()

        return final

        # Log everything on the way!
        # henry = logging.getLogger('Henry')
        # henry.log()