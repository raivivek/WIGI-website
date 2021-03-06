from __future__ import print_function

import pandas as pd
from bokeh._legacy_charts import Bar
from bokeh.models import NumeralTickFormatter
from numpy import round

from .utils import write_plot, read_data, fix_nan_inf


@write_plot('culture')
def plot(newest_changes):
    df, date_range = read_data(newest_changes, 'culture')

    # remove nan genders and nan rows
    del df['nan']
    df = df[list(map(lambda x: not pd.isnull(x), df.index))]

    has_changes = df.abs().sum().sum() != 0

    if not has_changes:
        return None, None, None, False

    df['total'] = df.sum(axis=1)
    df['nonbin'] = df['total'] - df['male'] - df['female']
    df['fem_per'] = df['female'] / (df['total']) * 100
    df['nonbin_per'] = df['nonbin'] / df['total'] * 100
    df['fem_per_million'] = df['fem_per'] * 10000
    df['nonbin_per_million'] = df['nonbin_per'] * 10000

    fix_nan_inf(df['fem_per'])
    fix_nan_inf(df['nonbin_per'])
    fix_nan_inf(df['fem_per_million'])
    fix_nan_inf(df['nonbin_per_million'])

    # sort, process
    dfs = df.sort_values('female')
    dfs = round(dfs, decimals=2)

    interesante = ['female', 'male', 'nonbin', 'total', 'fem_per']

    p = Bar(dfs[['female', 'male']],
            stacked=True,
            xlabel="Culture",
            ylabel="Total gendered biographies",
            width=800,
            height=500,
            legend='top_left')

    p._yaxis.formatter = NumeralTickFormatter(format='0,0')
    htmltable = dfs[interesante].sort_values('female', ascending=False)
    htmltable.columns = ['Female', 'Male', 'Non Binary', 'Total', 'Female (%)']
    top_rows = htmltable.head(10)
    bottom_rows = htmltable[::-1].head(10)
    table = [top_rows, bottom_rows]

    return p, date_range, table, True

if __name__ == "__main__":
    print(plot('newest'))
    print(plot('newest-changes'))
