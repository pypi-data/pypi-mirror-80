import pandas as pd
import numpy as np
import pingouin as pg
from scipy.stats import pearsonr
from scipy.stats import spearmanr

from prettytable import PrettyTable




def cronbach_alpha_scale_if_deleted(df):
    gca = pg.cronbach_alpha(df)
    result = pd.DataFrame(columns=["Item", "Scale Mean if Item Deleted", "Scale Variance if Item Deleted",
                                   "Corrected Item-Total Correlation", "Cronbach's Alpha if Item Deleted"])
    for column in df:
        sub_df = df.drop([column], axis=1)
        ac = pg.cronbach_alpha(sub_df)
        scale_mean = sub_df.mean().sum()
        variance = sub_df.sum(axis=1).var()
        pr = pearsonr(sub_df.mean(axis=1), df[column])
        result = result.append({'Item': column, "Scale Mean if Item Deleted": scale_mean, "Scale Variance if Item Deleted": variance,
                                "Corrected Item-Total Correlation": pr[0], "Cronbach's Alpha if Item Deleted": ac[0]}, ignore_index=True)
    return [gca, result]

def split_half_reliability(df):

    split_num = int((int(len(df.columns)) if ((int(len(df.columns)) % 2) == 0) else int(len(df.columns)+1) ) / 2 )
    dfs = np.split(df, [split_num], axis=1)
    pearson = pearsonr(dfs[0].mean(axis=1),dfs[1].mean(axis=1))[0]
    spearman_brown = (2*pearson)/(1+pearson)
    a_croncha_1 = round(pg.cronbach_alpha(data=dfs[0])[0],3)
    a_croncha_2 = round(pg.cronbach_alpha(data=dfs[1])[0],3)


    t = PrettyTable(['a','b','c','d'],header=False)
    t.align = "l"
    t.align['d']='r'
    t.add_row(["Cronbach's Alpha", "Part 1","Value",str(a_croncha_1).strip("0")])
    t.add_row(["", "","N of Items",str(len(dfs[0].columns))])
    t.add_row(["", "Part 2","Value",str(a_croncha_2).strip("0")])
    t.add_row(["", "","N of Items",str(len(dfs[1].columns))])
    t.add_row(["", "","Total N of Items",str(len(df.columns))])
    t.add_row(["", "","Correlation Between\nForms",str(round(pearson,3)).strip("0")])
    t.add_row(["Spearman-Brown\nCoefficient", "","Equal Length",str(round(spearman_brown,3)).strip("0")])

    #print(t)
    return [pearson,spearman_brown,a_croncha_1,a_croncha_2,t]
   