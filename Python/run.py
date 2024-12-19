"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Entry point for the creation of the variable elimination algorithm in Python 3.
Code to read in Bayesian Networks has been provided. We assume you have installed the pandas package.

"""
from read_bayesnet import BayesNet
from variable_elim import VariableElimination
import logging

if __name__ == '__main__':
    # Our logger is called henry
    logging.basicConfig(level=logging.INFO, filename='results.txt', filemode='w',
                        format='@ %(asctime)s - from %(name)s:\n%(message)s\n'
                               '--------------------------------------------------')
    henry = logging.getLogger("Henry the logger")

    # The class BayesNet represents a Bayesian network from a .bif file in several variables
    net = BayesNet('earthquake.bif') # Format and other networks can be found on http://www.bnlearn.com/bnrepository/

    ve = VariableElimination(net, henry)
    query = 'Burglary'
    evidence = {'JohnCalls': 'True', 'Earthquake': 'False'}

    heuristic = 'fff' # 'lia' for least incoming arcs, 'fff' for fewest factors first, anything else for no heuristic
    if heuristic == 'lia': # least incoming arcs => sort by amount of parents
        nodes = {node: len(net.parents[node]) for node in net.nodes}
        elim_order = sorted(net.nodes, key= lambda node: nodes[node])
    elif heuristic == 'fff': # fewest factors first => sort by amount of factors, which is the same as children + 1
        nodes = {}
        for node in net.nodes:
            # each node has its own factor:
            num_factors = 1
            # for every set of parents, if the node is in there, it is also in this child's factor
            for parents in net.parents.values():
                if node in parents: num_factors += 1
            nodes[node] = num_factors
        elim_order = sorted(nodes, key= lambda node: nodes[node])
    else:
        # No heuristic
        elim_order = net.nodes

    ve.run(query, evidence, elim_order)