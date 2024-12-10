import pandas as pd


class Factor:
    __df = None

    def __init__(self, df: pd.DataFrame):
        self.__df = df

    @staticmethod
    def multiply(f1: 'Factor', f2: 'Factor') -> 'Factor':
        shared_vars = list(set(f1.get_variables()) & set(f2.get_variables()) )
        f_merged = pd.merge(f1.get_df(), f2.get_df(), on=shared_vars)
        f_merged['prob'] = f_merged['prob_x'] * f_merged['prob_y']
        return Factor(f_merged.drop(columns=['prob_x', 'prob_y']))

    @staticmethod
    def multiply_list(factors: list) -> 'Factor':
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
        for k, v in evidence.items():
            if k in self.__df.columns:
                self.__df = self.__df[self.__df[k] == v].drop(columns=[k])
        return self

    def marginalize(self, var: str) -> 'Factor':
        other_vars = self.get_variables()
        other_vars.remove(var)
        self.__df = self.__df.groupby(other_vars, as_index=False)['prob'].sum()
        return self

    def normalize(self) -> 'Factor':
        sum_values = self.__df['prob'].sum()
        self.__df['prob'] = self.__df['prob'] / sum_values
        return self