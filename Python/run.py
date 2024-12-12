"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Entry point for the creation of the variable elimination algorithm in Python 3.
Code to read in Bayesian Networks has been provided. We assume you have installed the pandas package.

"""
from read_bayesnet import BayesNet
from variable_elim import VariableElimination

if __name__ == '__main__':
    # The class BayesNet represents a Bayesian network from a .bif file in several variables
    net = BayesNet('survey.bif') # Format and other networks can be found on http://www.bnlearn.com/bnrepository/
    # These are the variables read from the network that should be used for variable elimination

    ve = VariableElimination(net)
    query = 'O'
    evidence = {'S': 'M', 'E': 'uni', 'T': 'car'}

    """heuristic:"""
    heuristic = 'ttt'
    if heuristic == 'lia': # least incoming arcs
        nodes = {node: len(net.parents[node]) for node in net.nodes}
        elim_order = sorted(net.nodes, key= lambda node: nodes[node])
    elif heuristic == 'fff': # fewest factors first
        nodes = {}
        for node in net.nodes:
            # each node has its own factor:
            factors = 1
            # for every set of parents, if the node is in there, it is also in this nodes factor
            for parents in net.parents.values():
                if node in parents: factors += 1
            nodes[node] = factors
        elim_order = sorted(nodes, key= lambda node: nodes[node])
    else:
        elim_order = net.nodes

    # Call the variable elimination function for the queried node given the evidence and the elimination ordering as follows:   
    print(ve.run(query, evidence, elim_order))
    # assign data