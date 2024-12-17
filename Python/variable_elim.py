"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk, Cori Mandl, Linor legene

Class for the implementation of the variable elimination algorithm.

"""
from factor import Factor

class VariableElimination:

    def __init__(self, network, logger):
        """
        Initialize the variable elimination algorithm with the specified network.
        initialize a basic list of factors, which is simply the network probability tables turned into factor objects.

        @param network: a BayesNet object
        @param logger: a logging.Logger object
        """
        self.network = network
        self.factors = [Factor(p) for p in network.probabilities.values()]
        self.logger = logger
        self.logger.info("Initial factor list inferred from the network structure "
                         "and its conditional probability tables:\n"
                         f"{'\n*****\n'.join(map(str, self.factors))}")
        self.complexity = 0

    def run(self, query: str, observed: dict, elim_order: list) -> 'Factor':
        """
        Use the variable elimination algorithm to find out the probability
        distribution of the query variable given the observed variables

        @param query:      The query variable
        @param observed:   A dictionary of the observed variables {variable: value}
        @param elim_order: Either a list specifying the elimination ordering
                        or a function that will determine an elimination ordering
                        given the network during the run

        @return: A variable holding the probability distribution
                for the query variable given the evidence
        """
        # remove observed and query variables from elim order
        elim_order = [i for i in elim_order if i not in observed.keys() and i != query]
        self.logger.info("RUNNING THE VARIABLE ELIMINATION ALGORITHM\n"
                         f"The query variable is: {query}\n"
                         f"The observed variables are: {observed}\n"
                         "The variable elimination order of the remaining variables (given by heuristic) is: "
                         f"{'->'.join(elim_order)}\n"
                         "We reduce out the observed variables and start to loop over the variables to be eliminated:")

        # reduce out observed variables
        factors = [f.reduce(observed) for f in self.factors]
        # remove empty factor(s) which might occur if there was one with only observed variables
        factors = [f for f in factors if f.get_variables()]

        for var in elim_order:
            self.logger.info("The remaining factors:\n"
                             f"{'\n*****\n'.join(map(str, factors))}\n\n"
                             f"The next variable to be eliminated: {var}")

            factors_with_var = [f for f in factors if f.contains(var)]
            factors = [f for f in factors if f not in factors_with_var]
            self.logger.info(f"Gather all the factors that contain {var}:\n"
                             f"{'\n\n'.join(map(str, factors_with_var))}")

            # multiply factors_with_var together and then sum out var
            # Some factors might disappear, in which case we don't add them back to the factors list.
            f = Factor.multiply_list(factors_with_var)
            #
            self.complexity = max(f.get_num_variables(),self.complexity)

            self.logger.info(f"Multiply them together and get as result:\n{f}")
            f = f.sum_out(var)
            self.logger.info(f"Sum out {var} from the remaining factor and get:\n{f}\n"
                             "add this factor back to the list.")
            if f: factors.append(f)

        self.logger.info("All variables except the query have been eliminated. The remaining factors:\n"
                         f"{'\n*****\n'.join(map(str, factors))}")
        final = Factor.multiply_list(factors)
        self.logger.info(f"Multiply them:\n{final}")
        final = final.normalize()
        self.logger.info("Lastly, normalize the final factor, "
                         "resulting in a probability distribution of the query variable.\n"
                         f"given {observed}:\n"
                         f"{final}")
        self.logger.info(f"The complexity is: {self.complexity}")
        return final