import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

results = pd.read_csv('testingResults.csv')

results['lia'] = results['lia'] - 1
results['fff'] = results['fff'] - 1
results['no_heuristic'] = results['no_heuristic'] - 1


results_long = results.melt(id_vars=['BN_name'],
                            value_vars=['lia', 'fff', 'no_heuristic'],
                            var_name='Heuristic',
                            value_name='avg #Variables in largest factor')

plt.figure(figsize=(8, 6))
sns.pointplot(data=results_long, x='BN_name', y='avg #Variables in largest factor', hue='Heuristic', dodge=True, errorbar='pi')
plt.ylim(0, 10)
plt.show()