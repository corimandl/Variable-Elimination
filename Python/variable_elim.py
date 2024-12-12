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
        # remove observed and query variables from elim order
        elim_order = [i for i in elim_order if i not in observed.keys() and i != query]
        # TODO: Log elim order
        # construct a list of factors, one for each node in the network, reduce out the evidence variables
        factors = [Factor(p).reduce(observed) for p in self.network.probabilities.values()]
        # remove empty factor(s)
        factors = [f for f in factors if f.get_variables()]
        # TODO: log initial factor lost

        for var in elim_order:
            # TODO: log which variable we're eliminating next
            # gather all factors with var and remove them from the factors list
            factors_with_var = [f for f in factors if f.contains(var)]
            # TODO: log collection of all factors
            factors = [f for f in factors if f not in factors_with_var]
            # multiply factors_with_var together and then sum out var
            # Some factors might disappear, in which case we don't add them back to the factors list.
            f = Factor.multiply_list(factors_with_var)
            # TODO: log multiplication of the factors (result)
            f = f.sum_out(var)
            # TODO: log the marginalization
            if f: factors.append(f)

        # multiply final factors, which only have the query variable, and normalize.
        final = Factor.multiply_list(factors)
        # TODO: log final multiplication
        final.normalize()
        # TODO: log normalization and final result

        return final