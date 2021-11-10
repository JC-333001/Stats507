# Jiaxi Chen
# jxichen@umich.edu
#


# ## Data Cleaning
# Reference from: https://www.w3schools.com/python/pandas/pandas_cleaning.asp
# https://pandas.pydata.org/docs/reference/index.html
# ### Finding Duplicates
# - Duplicate rows are rows that have been registered more than one time.
#
# - `pandas.DataFrame.duplicated` returns boolean series denoting duplicate rows.
# - `keep` determines which duplicates (if any) to mark.
#     - `keep = False` : Mark all duplicates as True.
#     - `keep = first` : Mark duplicates as True except for the first occurrence.
#     - `keep = last` : Mark duplicates as True except for the last occurrence.

df = data('iris')
df.head()
print(df[df.duplicated(keep=False)])
print(df[df.duplicated(keep='first')])

# ### Removing Duplicates
# - We can use the `drop_duplicates()` method to remove duplicates
# - The `inplace = True` will make sure that the method does NOT return
# a new DataFrame, but it will remove all duplicates from the original
# DataFrame.

print(df.shape)
df.drop_duplicates(inplace = True)
print(df.shape)

# ### Finding NaN
# - Check for NaN under a single DataFrame column:
# `df['your column name'].isnull().values.any()`
# - Count the NaN under a single DataFrame column:
# `df['your column name'].isnull().sum()`
# - Check for NaN under an entire DataFrame: `df.isnull().values.any()`
# - Count the NaN under an entire DataFrame: `df.isnull().sum().sum()`

data = {'set_of_numbers': [1,2,3,4,5,np.nan,6,7,np.nan,8,9,10,np.nan]}
df = pd.DataFrame(data)
check_for_nan = df['set_of_numbers'].isnull()
print (check_for_nan)
nan_count = df['set_of_numbers'].isnull().sum()
print (nan_count)
nan_exist = df['set_of_numbers'].isnull().values.any()
print(nan_exist)

# ### Replacing NaN with mean, median or mode
# - A common way to replace empty cells, is to calculate the mean, median or mode value of the column.
# - Pandas uses the `mean()` `median()` and `mode()` methods to calculate the respective values for a specified column

x = df["set_of_numbers"].mean()
df["set_of_numbers"].fillna(x, inplace = True)
print(df)
nan_count = df['set_of_numbers'].isnull().sum()
print (nan_count)
