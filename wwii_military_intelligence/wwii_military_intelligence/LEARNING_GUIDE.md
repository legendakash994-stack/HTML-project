# Learning guide

## Pandas concepts
- `read_csv()` loads CSV data into DataFrames.
- `groupby()` groups records by country or alliance.
- `pivot_table()` reshapes long-format production data.
- `sort_values()` ranks countries.
- `sum()` and `mean()` summarize columns.
- `to_csv()` exports analysis results.

## NumPy concepts
- `np.mean()` calculates the average.
- `np.std()` measures spread/variation.
- `np.array()` converts a Pandas Series to a NumPy array.
- `.max()` and `.min()` find extreme values.

## Important data-analysis idea
A blank value is not the same as zero. Blank means the source does not provide a figure for that country-year. The code therefore uses `min_count=1` in relevant sums so an all-missing group does not silently become zero.
