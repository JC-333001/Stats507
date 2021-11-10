import numpy as np
import pandas as pd
import math
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from pydataset import data
from scipy.stats import ttest_ind_from_stats
from IPython.core.display import display, HTML
from scipy.stats import norm

cohort_1 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/DEMO_G.XPT')
cohort_1['cohort'] = '2011-2012'

cohort_2 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2013-2014/DEMO_H.XPT')
cohort_2['cohort'] = '2013-2014'

cohort_3 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/DEMO_I.XPT')
cohort_3['cohort'] = '2015-2016'

cohort_4 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/DEMO_J.XPT')
cohort_4['cohort'] = '2017-2018'
# -

df = pd.concat([cohort_1, cohort_2, cohort_3, cohort_4])
df = df[['SEQN', 'RIDAGEYR', 'RIAGENDR', 'RIDRETH3', 'DMDEDUC2', 'DMDMARTL',
         'RIDSTATR','SDMVPSU', 'SDMVSTRA', 'WTMEC2YR', 'WTINT2YR', 'cohort']]
df1 = df.rename(columns={"SEQN": "id", "RIDAGEYR": "age",
                         "RIAGENDR" : "gender",
                         "RIDRETH3": "race_and_ethnicity",
                         "DMDEDUC2": "education",
                         "DMDMARTL": "marital_status",
                         "RIDSTATR": "exam_status",
                         "SDMVPSU": "masked_variance_PSU",
                         "SDMVSTRA": "masked_variance_stratum",
                         "WTMEC2YR": "interviewed_and_MEC_examined",
                         "WTINT2YR": "interviewed"})
# Convert all missing values to be -1
df1 = df1.fillna(-1)
# convert "id", "age", 'education', 'masked_variance_PSU',
# and 'masked_variance_stratum' to integer
df1[['id', 'age', 'education',
     'masked_variance_stratum',
     'masked_variance_PSU','exam_status']] = df1[["id", "age", 'education',
                                    'masked_variance_stratum',
                                    'masked_variance_PSU',
                                    'exam_status']].astype(int)
df1 = df1.set_index('id')
# Create categorical variable for race_and_ethnicity
replace_map = {'race_and_ethnicity': {1: 'Mexican_American',
                                      2: 'Other Hispanic',
                                      3: 'Non-Hispanic White',
                                      4: 'Non-Hispanic Black',
                                      6: 'Non-Hispanic Asian',
                                      7: 'Other Race'},
              'marital_status': {1: 'Married', 2: 'Widowed',
                                 3: 'Divoced', 4: 'Seperated',
                                 5: 'Never Married', 6: 'Living with partner',
                                 77: 'Refused', 99: "Don't know",
                                 -1: 'Missing'},
              'interview_exam_status': {1: 'Interviewed Only',
                                        2: 'Both interviewed and MEC examined',
                                        -1: 'Missing'},
              'gender': {1: 'male', 2: 'female'}}
df1_replace = df1.copy()
df1_replace.replace(replace_map, inplace=True)
df1_replace.head(10)

df1_replace.to_pickle("demographic.pkl")
df1_read = pd.read_pickle('demographic.pkl')

# ### part b)

# +
cohort_health_1 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/'\
                              'OHXDEN_G.XPT')
cohort_health_1['cohort'] = '2011-2012'

cohort_health_2 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2013-2014/'\
                              'OHXDEN_H.XPT')
cohort_health_2['cohort'] = '2013-2014'

cohort_health_3 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/'\
                              'OHXDEN_I.XPT')
cohort_health_3['cohort'] = '2015-2016'

cohort_health_4 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/'\
                              'OHXDEN_J.XPT')
cohort_health_4['cohort'] = '2017-2018'

# +
df_health = pd.concat([cohort_health_1, cohort_health_2,
                       cohort_health_3, cohort_health_4])
df1_health = df_health.rename(columns={"SEQN": "id",
                                       "OHDDESTS": "ohx_status"})
df1_health = df1_health.fillna(-1)
df1_health[['id']] = df1_health[["id"]].astype(int)
df1_health = df1_health.set_index('id')

df1_left = df1_read[['gender', 'age', 'exam_status', 'education']]
df1_left['under_20'] = np.where(df1_left['age'] < 20, True, False)
df1_left['college'] = ["some college/college graduate"
                       if (i == 4 or i == 5) and j == False
                       else "No college/<20"
                       for (i,j) in
                       zip(df1_left['education'],df1_left['under_20'])]
df1_right = df1_health['ohx_status']
df1_join = df1_left.join(df1_right, how='left')
df1_join = df1_join.fillna(-1)
df1_join['ohx_status'] = df1_join['ohx_status'].astype(int)

df1_join['ohx'] = ['complete' if i == 2 and j == 1
                   else 'missing'
                   for (i,j) in
                   zip(df1_join['exam_status'], df1_join['ohx_status'])]
df1_final = df1_join[['gender', 'age', 'under_20',
                      'college', 'exam_status',
                      'ohx_status', 'ohx']]
df1_final.to_pickle("dentition.pkl")
# -

df1_final

# ### part c)

df2 = pd.read_pickle('dentition.pkl')

# Number of rows needed to be dropped
dropped = df2.loc[df2['exam_status'] != 2]
print(dropped.shape[0])

# Number of rows remained
df2 = df2.loc[df2['exam_status'] == 2]
t_count = df2.shape[0]
print(t_count)

# ### part d)

df2_u = df2.groupby(['ohx', 'under_20']).size()
df2_g = df2.groupby(['ohx', 'gender']).size()
df2_c = df2.groupby(['ohx', 'college']).size()
df2_u_a = df2.groupby(['ohx', 'under_20'])['age'].agg(['mean','std'])
df2_u_g = df2.groupby(['ohx', 'gender'])['age'].agg(['mean','std'])
df2_u_c = df2.groupby(['ohx', 'college'])['age'].agg(['mean','std'])
df2_a = pd.concat([df2_u_a, df2_u_g, df2_u_c], keys = ['under_20', 'gender',
                                                       'college'])
df2_a = df2_a.unstack(level = 1)

cat = pd.concat([df2_u, df2_g, df2_c],
                keys = ['under_20', 'gender', 'college']).to_frame()
cat.columns= [*cat.columns[:-1], 'count']
cat = cat.unstack(level=1)
cat['complete%'] = round(cat.iloc[:, 0]/cat.sum(axis=1)*100,3)
cat['missing%'] = round(cat.iloc[:, 1]/cat.sum(axis=1)*100,3)
cat = cat.join(df2_a.reindex(df2_a.index, level=0))
cat = cat.rename({'mean': 'mean_age', 'std': 'std_age'}, axis=1)
cat['p-value(t-test)'] = cat.apply(lambda row :
                                   ttest_ind_from_stats(mean1=row[4],
                                                        std1=row[6],
                                                        nobs1=row[0],
                                                        mean2=row[5],
                                                        std2=row[7],
                                                        nobs2=row[1])[1]
                                   , axis = 1)
# cat

display(HTML(cat.to_html(index=True)))