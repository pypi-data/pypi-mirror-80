import pandas as pd
from .preprocess import Preprocess
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.api.types import is_numeric_dtype,is_object_dtype,is_datetime64_any_dtype


class Plotter(object):
    
    def __init__(self):
        pass

    def pairplot(self,df,columns):
        sns.pairplot(df[columns].sample(100));

    def plot(self,df,x,y):
        Prep = Preprocess()
        type_x = Prep.get_col_type(df,x)
        type_y = Prep.get_col_type(df,y)
        
        if (type_x == 'numeric') and (type_y=='numeric'):
            self.scatterplot(df,x,y)
            
        if type_x == 'categoric' and type_y == 'categoric':
            print(pd.crosstab(df[x],df[y],margins=True))
                  
        if type_x == 'numeric' and type_y == 'categoric':
            self.countplot(df,x,y)
                  
        if type_x == 'categoric' and type_y == 'numeric':
            self.lmplot(df,x,y)
                  
    def boxplot(self,df,columns):
        try:
            for column in columns:
                if not is_numeric_dtype(df[column]):
                    print(column,' is not a numeric type')
                    continue
                plt.figure()
                plt.title(column)
                sns.boxplot(x=column, data=df)
                plt.show()
        except:
            print('Error in Plotting ',column)
            
    def barplot(self,df,columns):
        try:
            for column in columns:
                if is_numeric_dtype(df[column]):
                    print(column,' is not a object type')
                    continue
                plt.figure()
                plt.title(column)
                sns.countplot(x = column,data = df)
        except:
            print('Error in Plotting ',column)
    def histogram(self,df,columns):
        try:
            for column in columns:
                plt.figure()
                plt.title(column)
                df[column].hist()
        except:
            print('Error in Plotting ',column)
            
    def scatterplot(self,df,xcol,ycol):
        try:
            sns.jointplot(x=xcol,y=ycol,data=df, kind='scatter')
        except:
            print('Problem with Columns')
            
    def countplot(self,df,xcol,ycol):
        sns.countplot(x=xcol, hue=ycol, data=df);
        
    def lmplot(self,df,xcol,ycol):
        sns.boxplot(x=xcol, y = ycol,data=df);