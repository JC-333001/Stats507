import numpy as np
import pandas as pd
from IPython.core.display import display, Markdown
import time

# ## Question 3

# ### a.

# +
cohort_1 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/DEMO_G.XPT')
cohort_1['cohort'] = '2011-2012'

cohort_2 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2013-2014/DEMO_H.XPT')
cohort_2['cohort'] = '2013-2014'

cohort_3 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/DEMO_I.XPT')
cohort_3['cohort'] = '2015-2016'

cohort_4 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/DEMO_J.XPT')
cohort_4['cohort'] = '2017-2018'

df = pd.concat([cohort_1, cohort_2, cohort_3, cohort_4])
df = df[['SEQN', 'RIDAGEYR', 'RIDRETH3', 'DMDEDUC2', 'DMDMARTL', 'RIDSTATR',
                    'SDMVPSU', 'SDMVSTRA', 'WTMEC2YR', 'WTINT2YR', 'cohort']]
# -

df1 = df.rename(columns={"SEQN": "id", "RIDAGEYR": "age",
                         "RIDRETH3": "race_and_ethnicity",
                         "DMDEDUC2": "education",
                         "DMDMARTL": "marital_status",
                         "RIDSTATR": "interview_exam_status",
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
     'masked_variance_PSU']] = df1[["id", "age", 'education',
                                    'masked_variance_stratum',
                                    'masked_variance_PSU']].astype(int)
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
                                        -1: 'Missing'}}
df1_replace = df1.copy()
df1_replace.replace(replace_map, inplace=True)
df1_replace.head(10)


df1_replace.to_pickle("/Users/jiaxichen/Desktop/STATS507/HW/demographic.pkl")

# ### b.

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
var_names = list(df_health)
var_names = [var for var in var_names
             if var[0:3] == 'OHX' and (var[-3:] == 'CTC'
                                       or (var[-2:] == 'TC'
                                           and var[-3] != 'R'))]
var_names.extend(['SEQN', 'OHDDESTS', 'cohort'])

df_health = df_health[var_names]

# +
df1_health = df_health.rename(columns={"SEQN": "id"})
# Convert all missing values to be -1
df1_health = df1_health.fillna(-1)
#convert "id", "age", 'education', 'masked_variance_PSU', and
# 'masked_variance_stratum' to integer
df1_health[['id']] = df1_health[["id"]].astype(int)
df1_health = df1_health.set_index('id')
# Create categorical variable for race_and_ethnicity
replace_map1 = {1: 'Primary Tooth', 2: 'Permanent tooth present',
                3: 'Dental implant', 4: 'Tooth not present',
                5: 'Permanent dental root fragment present',
                9: 'Could not assess', -1: 'Missing'}
replace_map2 = {1: 'Complete', 2:'Partial', 3:'Not Done', -1: 'Missing'}
df1_health_replace = df1_health.copy()
TC_replace = df1_health_replace[[var for var in var_names
                                 if var[0:3] == 'OHX'
                                 and (var[-3] != 'C'
                                      and var[-2:] == 'TC')]].replace(
    replace_map1, inplace=False)
CTC_replace = df1_health_replace[[var for var in var_names
                                  if var[0:3] == 'OHX'
                                  and var[-3:] == 'CTC']]
CTC_replace = CTC_replace.applymap(lambda x: x.decode("utf-8"))
CTC_replace = CTC_replace.applymap(lambda x: 'Missing' if x == '' else x)

TS_replace = df1_health_replace[['OHDDESTS', 'cohort']].replace(
    replace_map2, inplace=False)
df1_health_concat = pd.concat([TC_replace, CTC_replace, TS_replace], axis = 1)

# +
df1_health_rename = df1_health_concat.copy()
for i in range(0,32):
    df1_health_rename.columns.values[i] = 'tooth_count_{}'.format(i+1)

for i in range(32,60):
    df1_health_rename.columns.values[i] = 'coronal_caries_{}'.format(i-28)

df1_health_rename.columns.values[-2] = 'dentition_status'

df1_health_rename.head(10)
# -

df1_health_concat.to_pickle("/Users/jiaxichen/Desktop/STATS507/HW/"\
                            "dentition.pkl")

# ### c.

print("shape of demographic data in part a: ", df1_replace.shape)
print("shape of dentition data in part b: ", df1_health_concat.shape)

# - The demographic dataset in part(a) has 39156 cases
# - The dentition dataset in part(b) has 35909 cases




