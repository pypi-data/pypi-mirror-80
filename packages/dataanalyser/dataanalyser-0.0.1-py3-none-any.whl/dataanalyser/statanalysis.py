from .preprocess import Preprocess

import pandas as pd
import seaborn as sns
from pandas.api.types import is_numeric_dtype,is_object_dtype,is_datetime64_any_dtype

class StatAnalysis(object):
    def __init__(self):
        pass
    def correlation(self,df):
        try:
            sns.heatmap(df.corr())
        except:
            pass
    def anova(self,df,target,**kwargs):
        import scipy.stats as stats
        #Check whether the target is a categorical type
        columns=None
        if 'columns' in kwargs:
            columns = kwargs['columns']
        else:
            columns = Preprocess().num_col_types(df)['categoric']
        if columns==None:
            print('No Categoric columns to perform One-Way ANOVA')
            return
        #make a new dataframe
        print('Target Variable: ',target)
        fscores = []
        pvalues = []
        for column in columns:
            li = [df[df[column]==x][target] for x in df[column].unique()]
            fscore,pvalue=stats.f_oneway(*li)
            fscores.append(fscore)
            pvalues.append(pvalue)
        result_df = pd.DataFrame({'F-Score': fscores,'p-value':pvalues},index=columns)
        display(result_df)