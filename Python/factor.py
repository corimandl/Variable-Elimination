"""
@Author: Cori Mandl, Linor Legene

Factor representation for use in variable elimination
"""

import pandas as pd
from typing import Optional

class Factor:
    def __init__(self, df: pd.DataFrame):
        self.__df = df

    def __str__(self) -> str:
        return self.__df.to_string()

    @staticmethod
    def multiply(f1: 'Factor', f2: 'Factor') -> 'Factor':
        """
        Multiply two factors.
        @param f1: first factor.
        @param f2: second factor.
        @return: new factor which is the product of the two factors.
        """
        shared_vars = list(set(f1.get_variables()) & set(f2.get_variables())) # The variables that the new factor will contain
        f_merged = pd.merge(f1.get_df(), f2.get_df(), on=shared_vars)
        f_merged['prob'] = f_merged['prob_x'] * f_merged['prob_y'] # multiply the probability values
        return Factor(f_merged.drop(columns=['prob_x', 'prob_y']))

    @staticmethod
    def multiply_list(factors: list) -> 'Factor':
        """
        Multiply a list of factors
        @param factors: list of Factor objects
        @return: new factor which is the product of all the factors in the list.
        """
        while len(factors) > 1:
            f1 = factors.pop()
            f2 = factors.pop()
            factors.append(Factor.multiply(f1, f2))
        return factors[0]

    def get_df(self) -> pd.DataFrame:
        return self.__df

    def get_variables(self) -> list:
        return list(self.__df.columns.drop('prob'))

    def contains(self, var: str) -> bool:
        return var in self.__df.columns

    def reduce(self, evidence: dict) -> 'Factor':
        """
        Remove the rows from the factor that don't align with the evidence.
        @param evidence: a dictionary of variable names (str) and their observed values (str)
        @return: the reduced factor
        """
        for k, v in evidence.items():
            if k in self.__df.columns:
                self.__df = self.__df[self.__df[k] == v].drop(columns=[k])
        return self

    def sum_out(self, var: str) -> Optional['Factor']:
        """
        sum out the variable var from the factor. If var is the only variable, None is returned.
        @param var: The variable to sum out.
        @return: None if var was the only variable in the factor, else the remaining factor after var was summed out.
        """
        other_vars = self.get_variables()
        other_vars.remove(var)
        if not other_vars: return None
        self.__df = self.__df.groupby(other_vars, as_index=False)['prob'].sum()
        return self

    def normalize(self) -> 'Factor':
        """
        normalize the factor, making sure that the probability values add up to 1, making the factor into a prob distribution.
        @return: normalized probability distribution
        """
        sum_values = self.__df['prob'].sum()
        self.__df['prob'] = self.__df['prob'] / sum_values
        return self

    def get_num_variables(self):
        return len(self.__df.columns)

